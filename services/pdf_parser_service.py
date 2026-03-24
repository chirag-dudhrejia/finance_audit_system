import pandas as pd
import pdfplumber
from io import BytesIO
from core.llm_provider import llm
import json
import re
import time
from typing import Optional, List

REQUIRED_COLUMNS = [
    "transaction date",
    "descriptions",
    "debit",
    "credit",
    "transaction amount",
]


def _coerce_numeric(val):
    import math

    if val is None:
        return None
    if isinstance(val, float):
        if math.isnan(val) or math.isinf(val):
            return None
        return val
    if isinstance(val, int):
        return val
    try:
        result = float(str(val).replace(",", "").strip())
        if math.isnan(result) or math.isinf(result):
            return None
        return result
    except Exception:
        return None


def _map_columns(columns):
    mapping = {}
    for col in columns:
        norm = col.strip().lower() if isinstance(col, str) else ""
        if not norm:
            continue
        if "date" in norm and (
            "transaction" in norm or "txn" in norm or norm == "date"
        ):
            mapping[col] = "transaction date"
        elif "descr" in norm or "narr" in norm or "detail" in norm:
            mapping[col] = "descriptions"
        elif norm in ("debit", "debits", "dr"):
            mapping[col] = "debit"
        elif norm in ("credit", "credits", "cr"):
            mapping[col] = "credit"
        elif "transaction" in norm and "amount" in norm:
            mapping[col] = "transaction amount"
        elif norm == "amount":
            mapping[col] = "transaction amount"
    return mapping


def _clean_llm_json_response(text: str) -> str:
    """Remove markdown wrappers and extract JSON array."""
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"```\s*$", "", cleaned).strip()
    start_idx = cleaned.find("[")
    if start_idx != -1:
        cleaned = cleaned[start_idx:]
    if cleaned and not cleaned.rstrip().endswith("]"):
        last_obj_close = cleaned.rfind("}")
        if last_obj_close != -1:
            cleaned = cleaned[: last_obj_close + 1] + "]"
        else:
            cleaned = cleaned + "]"
    cleaned = re.sub(r",\s*]", "]", cleaned)
    return cleaned


def _extract_json_objects(text: str) -> List[dict]:
    """Extract valid JSON objects from broken/truncated JSON using bracket counting."""
    objects = []
    depth = 0
    start = None
    in_string = False
    escape = False

    for i, ch in enumerate(text):
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"' and not escape:
            in_string = not in_string
            continue
        if in_string:
            continue

        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                try:
                    obj = json.loads(text[start : i + 1])
                    if isinstance(obj, dict):
                        objects.append(obj)
                except json.JSONDecodeError:
                    pass
                start = None

    return objects


def _count_serial_numbers(page_text: str) -> int:
    """Count expected transactions by finding serial number patterns.

    Tries multiple patterns to handle varying PDF text extraction formatting.
    """
    count = 0
    for line in page_text.split("\n"):
        line = line.strip()
        if not line:
            continue
        # Pattern 1: "1  14.03.2026 ..." or "12 17/03/2026 ..."
        if re.match(r"^(\d{1,4})\s+\d{2}[./-]\d{2}[./-]\d{4}", line):
            count += 1
        # Pattern 2: "1. 14.03.2026 ..." or "12) 17.03.2026 ..."
        elif re.match(r"^(\d{1,4})[.)]\s*\d{2}[./-]\d{2}[./-]\d{4}", line):
            count += 1
        # Pattern 3: serial and date on same line separated by pipes or multiple spaces
        elif re.match(r"^(\d{1,4})\s*[|]\s*\d{2}[./-]\d{2}[./-]\d{4}", line):
            count += 1
        # Pattern 4: date appears anywhere after a short serial number at start
        elif re.match(r"^(\d{1,4})\s{1,5}\S+\s+\d{2}[./-]\d{2}[./-]\d{4}", line):
            count += 1
    return count


def _call_llm_with_retry(
    prompt: str, retries: int = 3, page_num: int = 0
) -> Optional[str]:
    for attempt in range(retries):
        try:
            start = time.time()
            response = llm.generate_content(
                prompt=prompt,
                max_output_tokens=8000,
                temperature=0,
            )
            elapsed = time.time() - start
            print(f"[LLM PARSER] Page {page_num}: response in {elapsed:.1f}s")
            if response is not None:
                return response
        except Exception as e:
            error_str = str(e)
            print(
                f"[LLM PARSER] Page {page_num}: attempt {attempt + 1} error: {error_str[:200]}"
            )
            is_retryable = any(
                code in error_str.lower()
                for code in ["429", "503", "timeout", "deadline", "rate", "overloaded"]
            )
            if is_retryable and attempt < retries - 1:
                wait = 2 ** (attempt + 1)
                print(f"[LLM PARSER] Page {page_num}: retrying in {wait}s...")
                time.sleep(wait)
            else:
                return None
    return None


def parse_pdf(file) -> tuple[pd.DataFrame, str]:
    """Parse a bank statement PDF. Returns (DataFrame, method)."""
    if hasattr(file, "read"):
        data = file.read()
    elif isinstance(file, (bytes, bytearray)):
        data = bytes(file)
    else:
        raise TypeError("Unsupported file type. Expected bytes or file-like object.")

    print(f"[PDF PARSER] File size: {len(data)} bytes")

    # Try table extraction first
    try:
        df, method = _extract_tables_from_pdf(data)
        if len(df) > 0:
            print(f"[PDF PARSER] Table extraction: {len(df)} rows")
            return df, "table"
    except ValueError:
        print("[PDF PARSER] Table extraction failed, falling back to LLM")
    except Exception as e:
        print(f"[PDF PARSER] Table extraction error: {e}, falling back to LLM")

    # Fallback: LLM parsing
    df, method = _parse_pdf_with_llm(data)
    print(f"[PDF PARSER] LLM extraction: {len(df)} rows")
    return df, "llm"


def _extract_tables_from_pdf(data: bytes) -> tuple[pd.DataFrame, str]:
    """Extract tables from PDF using pdfplumber."""
    all_rows = []

    with pdfplumber.open(BytesIO(data)) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables() or []:
                if not table or len(table) < 2:
                    continue

                header = [h for h in table[0] if h]
                if len(header) < 3:
                    continue

                # Skip non-transaction tables (legends, metadata)
                header_lower = " ".join(h.lower() for h in header)
                if "legend" in header_lower or "remark" in header_lower:
                    continue

                for row_data in table[1:]:
                    if not row_data or all(v is None for v in row_data):
                        continue
                    row_dict = {}
                    for i, col_name in enumerate(header):
                        row_dict[col_name] = row_data[i] if i < len(row_data) else None
                    all_rows.append(row_dict)

    if not all_rows:
        raise ValueError("No tables found in PDF.")

    df = pd.DataFrame(all_rows)
    col_map = _map_columns(df.columns)
    df = df.rename(columns=col_map)

    # Ensure required columns
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = None

    # Convert numeric
    for col in ["debit", "credit", "transaction amount"]:
        df[col] = df[col].apply(_coerce_numeric)

    # Validate: at least some rows must have numeric amounts
    has_amounts = any(
        df[col].apply(lambda x: pd.notna(x) and isinstance(x, (int, float))).sum() > 0
        for col in ["debit", "credit", "transaction amount"]
        if col in df.columns
    )
    if not has_amounts:
        raise ValueError("No numeric amounts found in extracted table.")

    return df[REQUIRED_COLUMNS], "table"


def _parse_pdf_with_llm(data: bytes) -> tuple[pd.DataFrame, str]:
    """Parse PDF page-by-page using LLM."""
    print("[LLM PARSER] Starting LLM parsing...")

    all_transactions: List[dict] = []

    with pdfplumber.open(BytesIO(data)) as pdf:
        total_pages = len(pdf.pages)
        print(f"[LLM PARSER] Total pages: {total_pages}")

        for page_idx, page in enumerate(pdf.pages):
            page_num = page_idx + 1
            page_text = page.extract_text()

            if not page_text or not page_text.strip():
                print(f"[LLM PARSER] Page {page_num}: empty, skipping")
                continue

            # Count expected transactions from serial numbers
            expected_count = _count_serial_numbers(page_text)
            print(
                f"[LLM PARSER] Page {page_num}: {len(page_text)} chars, "
                f"~{expected_count} transactions expected"
            )

            count_hint = ""
            if expected_count > 0:
                count_hint = (
                    f"\nThis page contains approximately {expected_count} transactions. "
                    f"Extract ALL of them."
                )

            prompt = f"""
Extract ONLY bank transaction rows from the text below.

STRICT RULES:
- A valid transaction MUST start with a serial number AND a date (e.g. "1 14.03.2026")
- Ignore EVERYTHING before the first such row
- Ignore EVERYTHING after the last such row
- Ignore sections like Legends, Abbreviations, Notes, Disclaimers completely
- Ignore any lines that do NOT contain a date in format DD.MM.YYYY
- Merge multi-line descriptions into a single line
- Each transaction must include: date, description, debit/credit/amount

OUTPUT FORMAT:
Return ONLY a valid JSON array. No markdown, no explanation.

Each object:
{{
  "transaction_date": "YYYY-MM-DD",
  "description": "clean single-line text",
  "debit": number or null,
  "credit": number or null,
  "amount": number
}}

IMPORTANT:
- Remove line breaks inside description
- Remove extra spaces
- Do NOT include balance column
- Do NOT include legends or metadata
- If unsure → SKIP the row

TEXT:
{page_text}
"""

            response_text = _call_llm_with_retry(
                prompt=prompt, retries=3, page_num=page_num
            )

            if not response_text:
                print(f"[LLM PARSER] Page {page_num}: no response")
                continue

            # Check for truncation (response near max output length)
            if len(response_text) > 7000:
                print(
                    f"[LLM PARSER] Page {page_num}: response may be truncated "
                    f"({len(response_text)} chars)"
                )

            cleaned_json = _clean_llm_json_response(response_text)

            try:
                transactions = json.loads(cleaned_json)
            except json.JSONDecodeError:
                transactions = _extract_json_objects(cleaned_json)

            if not isinstance(transactions, list):
                print(f"[LLM PARSER] Page {page_num}: response is not a list, skipping")
                continue

            # Basic sanity filter: must have description + at least one amount
            valid = []
            for txn in transactions:
                if not isinstance(txn, dict):
                    continue
                desc = str(txn.get("description", "")).strip()
                has_amount = any(
                    isinstance(txn.get(k), (int, float)) and txn.get(k, 0) != 0
                    for k in ("debit", "credit", "amount")
                )
                if desc and has_amount:
                    valid.append(txn)

            if not valid:
                print(
                    f"[LLM PARSER] Page {page_num}: 0 valid transactions "
                    f"(raw: {len(transactions)})"
                )
                continue

            # Sanity check: warn if count deviates significantly from expected
            if (
                expected_count > 0
                and abs(len(valid) - expected_count) > expected_count * 0.5
            ):
                print(
                    f"[LLM PARSER] Page {page_num}: count mismatch "
                    f"(expected ~{expected_count}, got {len(valid)})"
                )

            all_transactions.extend(valid)
            print(f"[LLM PARSER] Page {page_num}: {len(valid)} transactions")

    print(f"[LLM PARSER] Total transactions: {len(all_transactions)}")

    if not all_transactions:
        return pd.DataFrame(columns=REQUIRED_COLUMNS), "llm_failed"

    df = pd.DataFrame(all_transactions)

    # Normalize column names
    df = df.rename(
        columns={
            "transaction_date": "transaction date",
            "description": "descriptions",
            "amount": "transaction amount",
        }
    )

    # Ensure required columns
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = None

    # Convert numeric
    def _safe_to_number(x):
        if isinstance(x, (int, float)):
            return x
        if isinstance(x, str):
            try:
                return float(x.replace(",", "").replace("₹", "").strip())
            except ValueError:
                return None
        return None

    for col in ["debit", "credit", "transaction amount"]:
        if col in df.columns:
            df[col] = df[col].apply(_safe_to_number)

    return df[REQUIRED_COLUMNS], "llm"
