# PDF Ingestion Feature Integration Guide

## Overview

The finance audit system now seamlessly supports ingesting transaction data from both **CSV** and **PDF** bank statements. This document explains the implementation details and architecture.

---

## Architectural Changes

### 1. **PDF Parser Service** → Already Implemented
**File:** [services/pdf_parser_service.py](services/pdf_parser_service.py)

The PDF parser extracts tables from bank statement PDFs:
- Normalizes column names (maps "Txn Date" → "transaction date", "Narration" → "descriptions", etc.)
- Handles debit/credit vs. net amount variants
- Applies numeric coercion with comma removal
- Returns a properly formatted DataFrame matching CSV schema

---

### 2. **Enhanced Ingestion Service**
**File:** [services/ingestion_service.py](services/ingestion_service.py)

**Key Changes:**

```python
def ingest_file(self, file, user_id: str) -> int:
    """Unified entry point for CSV & PDF files."""
    # Auto-detect file type
    ext = os.path.splitext(filename)[1].lower()
    
    if ext == ".pdf":
        df = parse_pdf(file)  # Uses pdfplumber
    else:
        df = pd.read_csv(file)
    
    return self._normalize_dataframe(df, user_id)

def _normalize_dataframe(self, df: pd.DataFrame, user_id: str) -> int:
    """Unified normalization pipeline."""
    # 1. Insert raw unparsed data
    # 2. Normalize with date parsing, numeric coercion
    # 3. Upsert to clean_transactions (idempotent via txn_hash)
    # 4. Return count of processed records
```

**Benefits:**
- ✅ Single normalization pipeline for both file types
- ✅ Date parsing with fallback handling
- ✅ Numeric coercion with error resilience
- ✅ Idempotent insertion via `txn_hash` upsert

---

### 3. **Repository Update**
**File:** [data/repositories/transaction_repo.py](data/repositories/transaction_repo.py)

**Change:** From `insert()` → `upsert()` with `on_conflict="txn_hash"`

```python
def bulk_insert_clean(self, records):
    """Prevents duplicate transactions if same file is re-processed."""
    self.client.table("bank_statements.clean_transactions").upsert(
        records, on_conflict="txn_hash"
    ).execute()
```

**Why:** Ensures re-uploading the same statement doesn't create duplicates (idempotency key).

---

### 4. **Streamlit UI Update**
**File:** [app/main.py](app/main.py)

**Before:**
```python
uploaded_file = st.file_uploader("Upload CSV")
service.ingest_csv(uploaded_file, user_id="demo")
```

**After:**
```python
uploaded_file = st.file_uploader(
    "Upload CSV or PDF bank statement", 
    type=["csv", "pdf"]
)
processed = service.ingest_file(uploaded_file, user_id="demo")
st.success(f"Uploaded & processed {processed} transactions.")
```

---

## Database Schema (No Changes Required)

The existing schema already supports PDF ingestion:

```sql
-- raw_transactions: Stores unparsed PDF/CSV data as JSONB
CREATE TABLE bank_statements.raw_transactions (
    id UUID PRIMARY KEY,
    user_id UUID,
    raw_data JSONB,  -- Tables extracted from PDFs stored here
    uploaded_at TIMESTAMP
);

-- clean_transactions: Normalized transactions
CREATE TABLE bank_statements.clean_transactions (
    id UUID PRIMARY KEY,
    user_id UUID,
    txn_date DATE,
    description TEXT,
    debit NUMERIC,
    credit NUMERIC,
    amount NUMERIC,
    txn_hash TEXT UNIQUE,  -- Idempotency key
    processed_flag BOOLEAN DEFAULT FALSE,
    ...
);
```

---

## Data Flow Diagram

```
┌─────────────────────┐
│  CSV or PDF File    │
└──────────┬──────────┘
           │
           v
    ┌──────────────┐
    │ File Upload  │
    │ (main.py)    │
    └──────┬───────┘
           │
           v
    ┌──────────────────────────┐
    │ IngestionService.        │
    │ ingest_file()            │
    └──────┬───────────────────┘
           │
      ┌────┴─────────┐
      │              │
      v              v
   PDF?           CSV?
      │              │
      v              v
 parse_pdf()    pd.read_csv()
      │              │
      └────┬─────────┘
           │
           v
    ┌────────────────────────────┐
    │ _normalize_dataframe()      │
    │ • Date parsing             │
    │ • Numeric coercion         │
    │ • Hash generation          │
    └────┬───────────────────────┘
         │
    ┌────┴──────────────────────┐
    │                           │
    v                           v
insert_raw()           bulk_insert_clean()
(raw_transactions)     (clean_transactions)
    │                           │
    └──────────────┬────────────┘
                   │
                   v
         ┌──────────────────────┐
         │ Supabase Database    │
         │ (with RLS policies)  │
         └──────────────────────┘
```

---

## Supported PDF Formats

The parser handles bank statement PDFs with **tabular transaction data**:

### Example PDF Table Structure:
```
| Transaction Date | Description | Debit | Credit | Balance |
|---|---|---|---|---|
| 2023-01-01 | Grocery Store | 50.00 | | 950.00 |
| 2023-01-02 | Salary Deposit | | 1000.00 | 1950.00 |
```

### Requirements:
- ✅ Tables must be extractable by `pdfplumber`
- ✅ Column names should contain recognizable keywords:
  - Date: "date", "transaction date", "txn date"
  - Description: "description", "narration", "details"
  - Amounts: "debit", "credit", "dr", "cr", "amount"
- ✅ Numeric values can use commas (automatically stripped)

---

## Usage

### 1. **Run Streamlit App**
```bash
streamlit run app/main.py
```

### 2. **Upload a File**
- Click **"Upload CSV or PDF bank statement"**
- Select a `.csv` or `.pdf` file
- System auto-detects format and processes accordingly

### 3. **API Usage** (Programmatic)
```python
from services.ingestion_service import IngestionService

service = IngestionService()

# Process CSV
with open("statement.csv", "rb") as f:
    processed = service.ingest_file(f, user_id="user123")
    print(f"Processed {processed} transactions")

# Process PDF
with open("statement.pdf", "rb") as f:
    processed = service.ingest_file(f, user_id="user123")
    print(f"Processed {processed} transactions")
```

---

## Error Handling

The system is robust to:
- ❌ PDFs with no extractable tables → `ValueError` with clear message
- ❌ Malformed dates → Falls back to raw string storage
- ❌ Missing amount columns → Derives from debit/credit
- ❌ Duplicate uploads → Silently skipped (upsert on `txn_hash`)

---

## Performance Considerations

1. **Batch Insertion:** Raw and clean transactions are inserted in bulk
2. **Idempotency:** Upsert prevents duplicate transactions on re-upload
3. **Lazy Parsing:** PDF tables only extracted when needed
4. **Memory Efficient:** Streaming large DataFrames (not all in memory at once)

---

## Testing

Run test suite:
```bash
pytest tests/test_ingestion_pdf.py -v
```

Test covers:
- ✅ PDF parsing delegation
- ✅ File type detection
- ✅ Repository insertion calls
- ✅ Transaction count return value

---

## Future Enhancements

- [ ] Support for OCR-based PDFs (non-table)
- [ ] Multi-page PDF handling optimization
- [ ] Bank-specific format detection
- [ ] Async ingestion for large files
- [ ] Progress tracking UI
- [ ] Batch re-processing with filtering

---

## Summary of Changes

| File | Change | Reason |
|---|---|---|
| `pdf_parser_service.py` | Already exists | Parse PDF tables to DataFrame |
| `ingestion_service.py` | Unified `ingest_file()` method | Support CSV/PDF with single pipeline |
| `transaction_repo.py` | Changed to `upsert()` | Idempotent insertion |
| `app/main.py` | Accept PDF uploads | UI supports both formats |
| `tests/test_ingestion_pdf.py` | New test module | Validate PDF parsing flow |

