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
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return val
    try:
        return float(str(val).replace(",", "").strip())
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


def _call_llm_with_retry(
    prompt: str, retries: int = 3, page_num: int = 0
) -> Optional[str]:
    for attempt in range(retries):
        try:
            response = llm.generate_content(
                prompt=prompt,
                max_output_tokens=6000,
                temperature=0,
            )
            if response:
                return response
        except Exception as e:
            error_str = str(e)
            is_retryable = any(
                code in error_str for code in ["429", "503", "timeout", "deadline"]
            )
            if is_retryable and attempt < retries - 1:
                time.sleep(2**attempt)
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

            print(f"[LLM PARSER] Page {page_num}: {len(page_text)} chars")
            print(f"[LLM PARSER] Page {page_num}: raw response:\n{page_text}")

            prompt = f"""Extract ALL transactions from this bank statement page.

OUTPUT: Return ONLY a valid JSON array. No markdown, no explanation.

Each object:
- "transaction_date": "DD.MM.YYYY" format (keep original format from statement)
- "description": full transaction description/narration
- "debit": withdrawal amount as number (null if none)
- "credit": deposit amount as number (null if none)
- "amount": net amount as number (debit positive, credit negative)

Include EVERY transaction row. Do not skip any.

Bank Statement Page:
{page_text}"""

            response_text = _call_llm_with_retry(
                prompt=prompt, retries=3, page_num=page_num
            )

            if not response_text:
                print(f"[LLM PARSER] Page {page_num}: no response")
                continue

            print(
                f"[LLM PARSER] Page {page_num}: got {len(response_text)} chars response"
            )

            cleaned_json = _clean_llm_json_response(response_text)

            try:
                transactions = json.loads(cleaned_json)
            except json.JSONDecodeError:
                print(
                    f"[LLM PARSER] Page {page_num}: JSON parse failed, trying fallback extraction"
                )
                transactions = _extract_json_objects(cleaned_json)

            if not isinstance(transactions, list):
                print(f"[LLM PARSER] Page {page_num}: response is not a list, skipping")
                continue

            for txn in transactions:
                if isinstance(txn, dict):
                    all_transactions.append(txn)

            print(
                f"[LLM PARSER] Page {page_num}: extracted {len(transactions)} transactions"
            )
            print(pd.DataFrame(transactions))

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
