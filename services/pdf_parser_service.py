import pandas as pd
import pdfplumber
from io import BytesIO
from google import genai
from core.config import settings
import json
import re
import time
from typing import Optional, List, Tuple

REQUIRED_COLUMNS = [
    "transaction date",
    "descriptions",
    "debit",
    "credit",
    "transaction amount",
]


def _normalize_column_name(col: str) -> str:
    if not isinstance(col, str):
        return ""
    return col.strip().lower()


def _map_columns(columns):
    """Map found columns into the canonical required columns."""
    mapping = {}
    for col in columns:
        norm = _normalize_column_name(col)
        if not norm:
            continue

        if "date" in norm and ("transaction" in norm or "txn" in norm or norm == "date"):
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


def _coerce_numeric(val):
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return val
    try:
        return float(str(val).replace(",", ""))
    except Exception:
        return None


def _is_valid_transaction_data(df: pd.DataFrame, col_map: dict) -> bool:
    """Validate that DataFrame contains actual transaction data, not metadata/legends."""
    print("[TRANSACTION VALIDATION] Checking if extracted data is valid transaction data...")
    
    # Check if any columns were successfully mapped to required transaction fields
    mapped_required = [col for col in REQUIRED_COLUMNS if col in col_map.values()]
    print(f"[TRANSACTION VALIDATION] Successfully mapped required columns: {mapped_required}")
    
    if not mapped_required:
        print(f"[TRANSACTION VALIDATION] ✗ INVALID: No required transaction columns found")
        print(f"[TRANSACTION VALIDATION]   Columns in data: {df.columns.tolist()}")
        return False
    
    # Check if we have at least 2 of the key fields: date, description, amount
    key_fields = ['transaction date', 'descriptions', 'transaction amount', 'debit', 'credit']
    found_key_fields = [col for col in key_fields if col in mapped_required]
    print(f"[TRANSACTION VALIDATION] Key transaction fields found: {found_key_fields}")
    
    if len(found_key_fields) < 2:
        print(f"[TRANSACTION VALIDATION] ✗ INVALID: Not enough key transaction fields (need >=2, got {len(found_key_fields)})")
        return False
    
    # Check if data contains actual transaction indicators
    # Look for numeric values in amount columns
    amount_cols = [col for col in ['transaction amount', 'debit', 'credit'] if col in mapped_required]
    
    if amount_cols:
        # Check if at least some rows have numeric amounts
        has_amounts = False
        for col in amount_cols:
            if col in df.columns:
                numeric_count = df[col].apply(lambda x: pd.notna(x) and isinstance(x, (int, float))).sum()
                print(f"[TRANSACTION VALIDATION] Column '{col}': {numeric_count}/{len(df)} rows have numeric values")
                if numeric_count > 0:
                    has_amounts = True
        
        if not has_amounts:
            print(f"[TRANSACTION VALIDATION] ✗ INVALID: No amount columns have numeric values")
            return False
    
    # Check for suspicious metadata patterns
    if 'Legends' in str(df.columns[0] if len(df.columns) > 0 else ''):
        print(f"[TRANSACTION VALIDATION] ✗ INVALID: Data contains 'Legends' - likely metadata, not transactions")
        return False
    
    print(f"[TRANSACTION VALIDATION] ✓ VALID: Data appears to be actual transaction data")
    return True


def _clean_llm_json_response(text: str) -> str:
    """Clean LLM response by removing markdown wrappers and extracting JSON.
    
    Args:
        text: Raw response text from LLM
        
    Returns:
        Clean JSON string
    """
    cleaned = text.strip()
    
    # Remove code fence wrappers (```json ... ```)
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"```\s*$", "", cleaned).strip()
    
    # Find the JSON array start
    start_idx = cleaned.find("[")
    if start_idx != -1:
        cleaned = cleaned[start_idx:]
    
    # If JSON is truncated, try to close it gracefully
    if cleaned and not cleaned.rstrip().endswith("]"):
        # Find the last complete object
        last_obj_close = cleaned.rfind("}")
        if last_obj_close != -1:
            cleaned = cleaned[:last_obj_close + 1] + "]"
        else:
            cleaned = cleaned + "]"
    
    # Remove trailing commas before closing bracket
    cleaned = re.sub(r",\s*]", "]", cleaned)
    
    return cleaned


def _extract_json_objects(text: str) -> List[dict]:
    """Extract valid JSON objects from possibly broken JSON array."""
    objects = []
    
    # Find all {...} blocks
    matches = re.findall(r"\{.*?\}", text, re.DOTALL)
    
    for m in matches:
        try:
            obj = json.loads(m)
            objects.append(obj)
        except:
            continue
    
    return objects


def _call_gemini_with_retry(
    client,
    prompt: str,
    retries: int = 3,
    page_num: int = 0
) -> Optional[str]:
    """Call Gemini API with exponential backoff retry logic.
    
    Args:
        client: Gemini API client
        prompt: Prompt to send to Gemini
        retries: Number of retry attempts
        page_num: Page number for logging
        
    Returns:
        Response text or None if all retries failed
    """
    for attempt in range(retries):
        try:
            print(f"[RETRY] Page {page_num} - Attempt {attempt + 1}/{retries}...")
            
            response = client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=prompt,
                config={
                    "max_output_tokens": 3000,
                    "temperature": 0
                }
            )
            
            if response and response.text:
                print(f"[RETRY] Page {page_num} - ✓ Success on attempt {attempt + 1}")
                return response.text
            else:
                print(f"[RETRY] Page {page_num} - Empty response, retrying...")
                
        except Exception as e:
            error_str = str(e)
            is_retryable = any(code in error_str for code in ["429", "503", "timeout", "deadline"])
            
            if is_retryable and attempt < retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                print(f"[RETRY] Page {page_num} - Retryable error ({type(e).__name__}), waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"[RETRY] Page {page_num} - Non-retryable error or max retries: {type(e).__name__}: {e}")
                return None
    
    print(f"[RETRY] Page {page_num} - Failed after {retries} retries")
    return None


def parse_pdf(file) -> tuple[pd.DataFrame, str]:
    """Parse a bank statement PDF and return a DataFrame with normalized columns.

    Uses hybrid approach: table extraction first, LLM fallback for scanned PDFs.

    Args:
        file: bytes, file-like object, or path-like object.

    Returns:
        Tuple of (DataFrame, parsing_method) where parsing_method is "table" or "llm"
    """
    print("\n" + "="*60)
    print("[PDF PARSER] Starting PDF parsing...")
    
    # Read data bytes (pdfplumber accepts bytes buffer)
    if hasattr(file, "read"):
        data = file.read()
    elif isinstance(file, (bytes, bytearray)):
        data = file
    else:
        raise TypeError("Unsupported file type. Expected bytes or file-like object.")

    print(f"[PDF PARSER] File size: {len(data)} bytes")

    # First try: Table extraction (fast for structured PDFs)
    print("[PDF PARSER] Attempting table extraction...")
    try:
        df, method = _extract_tables_from_pdf(data)
        if len(df) > 0:
            print(f"[PDF PARSER] ✓ Table extraction returned {len(df)} rows")
            print(f"[PDF PARSER] ✓ Columns: {df.columns.tolist()}")
            print("="*60 + "\n")
            return df, "table"
        else:
            print(f"[PDF PARSER] ✗ Table extraction returned empty DataFrame")
    except ValueError as e:
        # ValueError is raised when validation fails - this is expected, proceed to LLM
        print(f"[PDF PARSER] ✗ Table extraction validation failed: {e}")
    except Exception as e:
        print(f"[PDF PARSER] ✗ Table extraction failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

    # Fallback: LLM parsing for scanned PDFs
    print("[PDF PARSER] Falling back to LLM parsing for scanned/unstructured PDF...")
    try:
        df, method = _parse_pdf_with_llm(data)
        print(f"[PDF PARSER] ✓ LLM parsing successful! Rows: {len(df)}")
        print("="*60 + "\n")
        return df, "llm"
    except Exception as e:
        print(f"[PDF PARSER] ✗ LLM parsing failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise ValueError(f"Failed to parse PDF with both table extraction and LLM: {e}")


def _extract_tables_from_pdf(data: bytes) -> tuple[pd.DataFrame, str]:
    """Extract tables from PDF using pdfplumber."""
    all_rows = []
    page_count = 0
    table_count = 0
    
    print("[TABLE EXTRACTION] Opening PDF...")
    with pdfplumber.open(BytesIO(data)) as pdf:
        print(f"[TABLE EXTRACTION] Total pages: {len(pdf.pages)}")
        
        for page_idx, page in enumerate(pdf.pages):
            print(f"\n[TABLE EXTRACTION] Processing page {page_idx + 1}...")
            page_tables = page.extract_tables()
            
            if not page_tables:
                print(f"[TABLE EXTRACTION]   No tables found on this page")
                continue
            
            print(f"[TABLE EXTRACTION]   Found {len(page_tables)} table(s)")
            
            for table_idx, table in enumerate(page_tables):
                print(f"[TABLE EXTRACTION]   Table {table_idx + 1}:")
                
                if not table or len(table) < 2:
                    print(f"[TABLE EXTRACTION]     Skipping - invalid table (rows: {len(table) if table else 0})")
                    continue
                
                # Get header from first row
                header = table[0]
                print(f"[TABLE EXTRACTION]     Raw header: {header}")
                print(f"[TABLE EXTRACTION]     Header count: {len(header)}")
                
                # Filter out None/empty headers
                header = [h for h in header if h]
                print(f"[TABLE EXTRACTION]     Filtered header: {header}")
                print(f"[TABLE EXTRACTION]     Filtered header count: {len(header)}")
                
                if not header:
                    print(f"[TABLE EXTRACTION]     Skipping - no valid headers after filtering")
                    continue
                
                # Check for duplicate headers
                if len(header) != len(set(header)):
                    print(f"[TABLE EXTRACTION]     ⚠️  WARNING: Duplicate headers detected!")
                    print(f"[TABLE EXTRACTION]        Before dedup: {header}")
                    unique_headers = []
                    seen = set()
                    for h in header:
                        if h not in seen:
                            unique_headers.append(h)
                            seen.add(h)
                    header = unique_headers
                    print(f"[TABLE EXTRACTION]        After dedup: {header}")
                
                # Process data rows
                row_count = 0
                for row_idx, row_data in enumerate(table[1:]):
                    if not row_data or all(v is None for v in row_data):
                        continue
                    
                    # Create row dict with first N values matching header length
                    row_dict = {}
                    for i, col_name in enumerate(header):
                        if i < len(row_data):
                            row_dict[col_name] = row_data[i]
                        else:
                            row_dict[col_name] = None
                    
                    all_rows.append(row_dict)
                    row_count += 1
                
                print(f"[TABLE EXTRACTION]     Processed {row_count} data rows")
                table_count += 1
    
    print(f"\n[TABLE EXTRACTION] Total tables extracted: {table_count}")
    print(f"[TABLE EXTRACTION] Total rows collected: {len(all_rows)}")
    
    if not all_rows:
        raise ValueError("No tables found in PDF.")
    
    # Validate row structure before DataFrame creation
    print(f"\n[ROW VALIDATION] Validating row structure...")
    row_keys_list = [set(row.keys()) for row in all_rows]
    all_keys = set().union(*row_keys_list) if row_keys_list else set()
    print(f"[ROW VALIDATION] All unique keys across rows: {all_keys}")
    print(f"[ROW VALIDATION] Number of unique keys: {len(all_keys)}")
    
    # Check if keys vary across rows
    keys_vary = len(set(frozenset(row.keys()) for row in all_rows)) > 1
    print(f"[ROW VALIDATION] Keys vary across rows: {keys_vary}")
    
    if keys_vary:
        print(f"[ROW VALIDATION] ⚠️  Different rows have different columns!")
        print(f"[ROW VALIDATION] Standardizing all rows to have all keys...")
        # Ensure every row has all keys
        for row in all_rows:
            for key in all_keys:
                if key not in row:
                    row[key] = None
        print(f"[ROW VALIDATION] ✓ All rows standardized")
    
    # Build DataFrame with explicit columns to avoid pandas concat issues
    print(f"\n[DATAFRAME BUILDING] Creating DataFrame with {len(all_rows)} rows and {len(all_keys)} columns...")
    try:
        df = pd.DataFrame(all_rows, columns=sorted(all_keys))
        print(f"[DATAFRAME BUILDING] ✓ DataFrame created successfully")
    except Exception as e:
        print(f"[DATAFRAME BUILDING] ✗ Failed to create DataFrame: {type(e).__name__}: {e}")
        print(f"[DATAFRAME BUILDING] Sample rows:")
        for i, row in enumerate(all_rows[:3]):
            print(f"[DATAFRAME BUILDING]   Row {i}: {row}")
        raise
    
    print(f"[DATAFRAME BUILDING] Initial DataFrame shape: {df.shape}")
    print(f"[DATAFRAME BUILDING] Initial columns: {df.columns.tolist()}")
    print(f"[DATAFRAME BUILDING] Duplicate columns check: {len(df.columns) != len(set(df.columns))}")
    
    # Map columns to standard names
    print(f"\n[COLUMN MAPPING] Mapping columns to required schema...")
    col_map = _map_columns(df.columns)
    print(f"[COLUMN MAPPING] Found mappings: {col_map}")
    
    # Check if mapping will create duplicates
    mapped_cols = list(col_map.values())
    if len(mapped_cols) != len(set(mapped_cols)):
        print(f"[COLUMN MAPPING] ⚠️  Mapping creates duplicate columns!")
        print(f"[COLUMN MAPPING] Mapped columns: {mapped_cols}")
    
    df = df.rename(columns=col_map)
    print(f"[COLUMN MAPPING] Columns after mapping: {df.columns.tolist()}")
    print(f"[COLUMN MAPPING] Has duplicate columns: {len(df.columns) != len(set(df.columns))}")
    
    if len(df.columns) != len(set(df.columns)):
        print(f"[COLUMN MAPPING] ✗ ERROR: Duplicate columns after mapping!")
        print(f"[COLUMN MAPPING] Removing duplicate columns...")
        df = df.loc[:, ~df.columns.duplicated(keep='first')]
        print(f"[COLUMN MAPPING] Columns after dedup: {df.columns.tolist()}")
    
    # Ensure all required columns exist
    print(f"\n[COLUMN VALIDATION] Ensuring required columns exist...")
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        print(f"[COLUMN VALIDATION] Missing columns: {missing_cols}")
        for col in missing_cols:
            print(f"[COLUMN VALIDATION]   Adding missing column: {col}")
            df[col] = None
    else:
        print(f"[COLUMN VALIDATION] All required columns present")
    
    print(f"[COLUMN VALIDATION] Final columns before numeric conversion: {df.columns.tolist()}")
    
    # Normalize numeric columns
    print(f"\n[NUMERIC CONVERSION] Converting numeric columns...")
    try:
        df["debit"] = df["debit"].apply(_coerce_numeric)
        df["credit"] = df["credit"].apply(_coerce_numeric)
        df["transaction amount"] = df["transaction amount"].apply(_coerce_numeric)
        print(f"[NUMERIC CONVERSION] ✓ Conversion successful")
    except Exception as e:
        print(f"[NUMERIC CONVERSION] ✗ Conversion failed: {type(e).__name__}: {e}")
        raise
    
    # Compute transaction amount if missing
    print(f"\n[AMOUNT COMPUTATION] Computing transaction amounts...")
    try:
        df["transaction amount"] = df.apply(
            lambda row: (
                row["transaction amount"] if pd.notna(row["transaction amount"])
                else (row["debit"] if pd.notna(row["debit"])
                      else (-row["credit"] if pd.notna(row["credit"]) else None))
            ),
            axis=1
        )
        print(f"[AMOUNT COMPUTATION] ✓ Done")
    except Exception as e:
        print(f"[AMOUNT COMPUTATION] ✗ Failed: {type(e).__name__}: {e}")
        raise
    
    # VALIDATE: Check if this is actually transaction data before returning
    print(f"\n[VALIDATION] Validating extracted data...")
    col_map_for_validation = _map_columns(df.columns)
    if not _is_valid_transaction_data(df, col_map_for_validation):
        raise ValueError("Extracted table does not contain valid transaction data - likely metadata/legend. Falling back to LLM parsing.")
    
    # Final selection
    print(f"\n[FINAL SELECTION] Selecting required columns: {REQUIRED_COLUMNS}")
    print(f"[FINAL SELECTION] Available columns in df: {df.columns.tolist()}")
    
    # Check which required columns are missing in df
    missing_in_df = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_in_df:
        print(f"[FINAL SELECTION] ⚠️  Required columns not in DataFrame: {missing_in_df}")
        print(f"[FINAL SELECTION] Creating with available columns")
        available_cols = [col for col in REQUIRED_COLUMNS if col in df.columns]
        result_df = df[available_cols]
    else:
        result_df = df[REQUIRED_COLUMNS]
    
    print(f"[FINAL SELECTION] ✓ Final shape: {result_df.shape}")
    print(f"[FINAL SELECTION] ✓ Final columns: {result_df.columns.tolist()}")
    
    return result_df, "table"


def _parse_pdf_with_llm(data: bytes) -> tuple[pd.DataFrame, str]:
    """
    Parse PDF using page-wise Gemini LLM extraction with retry logic.
    
    Features:
    - Processes PDF page by page to avoid token limits
    - Uses exponential backoff for API retries
    - Handles malformed JSON gracefully
    - Returns empty DataFrame instead of failing
    
    Args:
        data: PDF file bytes
        
    Returns:
        Tuple[DataFrame, "llm" or "llm_failed"]
    """
    print("\n" + "="*60)
    print("[LLM PARSER] Starting page-wise LLM parsing...")
    
    try:
        # Initialize Gemini client
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        print("[LLM PARSER] ✓ Gemini client initialized")
        
        all_transactions: List[dict] = []
        
        # Process PDF page by page
        print("[LLM PARSER] Opening PDF for page-wise extraction...")
        with pdfplumber.open(BytesIO(data)) as pdf:
            total_pages = len(pdf.pages)
            print(f"[LLM PARSER] Total pages: {total_pages}")
            
            for page_idx, page in enumerate(pdf.pages):
                page_num = page_idx + 1
                print(f"\n[PAGE] Processing page {page_num}/{total_pages}...")
                
                # Extract text from page
                page_text = page.extract_text()
                
                if not page_text or not page_text.strip():
                    print(f"[PAGE] Page {page_num}: Skipped (empty)")
                    continue
                
                print(f"[PAGE] Page {page_num}: Extracted {len(page_text)} chars")
                print(f"Page text : {page_text}")

                # Build page-specific prompt
                prompt = f"""Extract all transaction data from this bank statement page.

    OUTPUT FORMAT (MANDATORY):
    - Return ONLY a valid JSON array
    - Do NOT wrap in markdown (no ``` or ```json)
    - Do NOT add explanations or extra text
    - Output must start with [ and end with ]
    - Ensure the JSON is COMPLETE and NOT truncated

    Each object must have EXACTLY these fields:
    - transaction_date (YYYY-MM-DD)
    - description (string)
    - debit (number or null)
    - credit (number or null)
    - amount (number: debit positive, credit negative)

    STRICT RULES:
    - Do not skip valid transactions
    - Do not include headers, summaries, or totals
    - Convert all numbers to numeric (no commas, no currency symbols)
    - If only one amount column exists → use "amount"
    - If debit exists → amount = positive
    - If credit exists → amount = negative
    - If both missing → amount = null
    - Dates MUST be converted to YYYY-MM-DD

    VALIDATION BEFORE OUTPUT:
    - Ensure JSON is syntactically correct
    - Ensure no trailing commas
    - Ensure no missing brackets
    - Ensure no truncation

Bank Statement Text:
{page_text}"""
                
                # Call Gemini with retry
                response_text = _call_gemini_with_retry(
                    client=client,
                    prompt=prompt,
                    retries=3,
                    page_num=page_num
                )
                
                if not response_text:
                    print(f"[PAGE] Page {page_num}: ✗ Failed to get response after retries")
                    continue
                
                # Clean and parse response
                cleaned_json = _clean_llm_json_response(response_text)
                
                try:
                    # transactions = json.loads(cleaned_json)
                    try:
                        transactions = json.loads(cleaned_json)
                    except json.JSONDecodeError:
                        print(f"[PAGE] Page {page_num}: ⚠️ Falling back to partial extraction")
                        transactions = _extract_json_objects(cleaned_json)
                    
                    if not isinstance(transactions, list):
                        print(f"[PAGE] Page {page_num}: ✗ Response is not an array")
                        continue
                    
                    valid_count = 0
                    for txn in transactions:
                        if isinstance(txn, dict):
                            all_transactions.append(txn)
                            valid_count += 1
                    
                    print(f"[PAGE] Page {page_num}: ✓ Parsed {valid_count} transactions")
                    
                except json.JSONDecodeError as e:
                    print(f"[PAGE] Page {page_num}: ✗ JSON parse error: {e}")
                    print(f"[PAGE] Response preview: {response_text[:200]}")
                    continue
        
        print(f"\n[LLM PARSER] Total transactions extracted: {len(all_transactions)}")
        
        # If no transactions found, return empty DataFrame with fail status
        if not all_transactions:
            print("[LLM PARSER] ⚠️  No transactions extracted from any page")
            empty_df = pd.DataFrame(columns=REQUIRED_COLUMNS)
            print("="*60 + "\n")
            return empty_df, "llm_failed"
        
        # Create DataFrame from all transactions
        print("[LLM PARSER] Creating DataFrame from all transactions...")
        df = pd.DataFrame(all_transactions)
        
        # Ensure required columns exist
        for col in REQUIRED_COLUMNS:
            if col not in df.columns:
                df[col] = None
        
        # Normalize column names
        df = df.rename(columns={
            "transaction_date": "transaction date",
            "description": "descriptions",
            "amount": "transaction amount"
        })
        
        # Ensure numeric columns are properly typed
        print("[LLM PARSER] Converting numeric columns...")

        def _safe_to_number(x):
            if isinstance(x, (int, float)):
                return x
            if isinstance(x, str):
                try:
                    # remove commas, currency symbols, spaces
                    x = x.replace(",", "").replace("₹", "").strip()
                    return float(x)
                except:
                    return None
            return None  # handles dict, list, etc.

        try:
            for col in ["debit", "credit", "transaction amount"]:
                if col in df.columns:
                    df[col] = df[col].apply(_safe_to_number)

            print("[LLM PARSER] ✓ Numeric conversion successful")

        except Exception as e:
            print(f"[LLM PARSER] ✗ Numeric conversion failed: {type(e).__name__}: {e}")
        
        # Select only required columns
        result_df = df[REQUIRED_COLUMNS]
        
        print(f"[LLM PARSER] ✓ Final DataFrame: {result_df.shape[0]} rows, {result_df.shape[1]} columns")
        print("="*60 + "\n")
        
        return result_df, "llm"
        
    except Exception as e:
        print(f"[LLM PARSER] ✗ Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        
        # Fail-safe: return empty DataFrame instead of crashing
        empty_df = pd.DataFrame(columns=REQUIRED_COLUMNS)
        print("="*60 + "\n")
        return empty_df, "llm_failed"
