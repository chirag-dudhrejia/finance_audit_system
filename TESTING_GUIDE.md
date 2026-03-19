# Testing Guide - PDF & CSV Ingestion Feature

## Quick Start Testing

### ✅ Test 1: Import & Core Logic (No Database Required)

```bash
# Run validation of all core components
cd finance_audit_system
venv\Scripts\python.exe test_quick_validation.py
```

**Expected Output:**
- ✅ PDF parser service working
- ✅ Numeric coercion robust
- ✅ Column mapping flexible
- ✅ Transaction hashing idempotent
- ✅ Ingestion service normalizes data
- ✅ Repository integration points ready
- ✅ File type detection logic verified

---

### ✅ Test 2: Module Imports

```bash
venv\Scripts\python.exe test_imports.py
```

**Expected Output:**
- ✅ pdf_parser_service imports OK
- ✅ hashing utilities imports OK
- ✅ ingestion_service imports OK
- ✅ config imports OK

---

### ✅ Test 3: CSV Ingestion Demo

```bash
venv\Scripts\python.exe demo_csv_ingestion.py
```

This will:
1. Read `sample_statement.csv` (10 transactions)
2. Auto-detect CSV format
3. Normalize all data
4. Show transaction details
5. Display what would be sent to database

**Sample Output:**
```
✅ Successfully processed 10 transactions

📊 Transaction Details:

  Transaction 1:
    Date:        2023-01-01
    Description: Walmart - Groceries
    Amount:      75.5
    Debit:       75.5
    Credit:      None
    Hash:        abc123def456...
```

---

## Full Integration Testing (With Supabase)

### Step 1: Setup Environment

```bash
# Create .env file from example
copy .env.example .env

# Edit .env with your credentials:
# SUPABASE_URL=your-supabase-url
# SUPABASE_KEY=your-supabase-key
# GEMINI_API_KEY=your-gemini-key
```

### Step 2: Initialize Database

```bash
# Create tables (run in Supabase SQL editor)
psql -f data/schemas/schema.sql
```

### Step 3: Install All Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Streamlit App

```bash
streamlit run app/main.py
```

Then:
1. Open browser → http://localhost:8501
2. Click "Upload CSV or PDF bank statement"
3. Select `sample_statement.csv`
4. See: "Uploaded & processed 10 transactions"
5. Check Supabase tables:
   - `bank_statements.raw_transactions` (raw JSONB data)
   - `bank_statements.clean_transactions` (normalized transactions)

---

## Test Files Provided

### `sample_statement.csv`
- 10 sample transactions
- Standard bank statement format
- Includes debits, credits, and salaries
- Ready to upload

### `test_quick_validation.py`
- Tests all core components
- No database required
- Mocks repository layer
- Validates logic independently

### `test_imports.py`
- Simple import test
- Verifies all modules load cleanly
- Quick sanity check

### `demo_csv_ingestion.py`
- End-to-end CSV processing demo
- Shows data transformation
- Displays results without database

### `tests/test_ingestion_pdf.py`
- Unit test for PDF flow
- Uses pytest framework
- Run with: `pytest tests/test_ingestion_pdf.py -v`

---

## Verification Checklist

After testing, verify:

- [ ] Core validation passes (all components working)
- [ ] CSV ingestion demo shows 10 transactions processed
- [ ] Import test confirms all modules load
- [ ] Streamlit app runs without errors
- [ ] File uploader accepts both CSV and PDF
- [ ] Transaction count displayed correctly
- [ ] Sample transactions visible in database

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'pandas'"
- Use: `venv\Scripts\python.exe script.py`
- Do NOT use global Python directly

### "SUPABASE_URL not found"
- Create `.env` file in `finance_audit_system/` folder
- Copy values from `.env.example`

### PDF upload fails
- Ensure PDF has tabular transaction data
- Columns must contain recognizable keywords:
  - Date: "date", "transaction date"
  - Description: "description", "narration"
  - Amount: "debit", "credit", "amount"

### "No tables found in PDF" error
- PDF likely doesn't have extractable tables
- pdfplumber works best with well-structured bank PDFs
- Test with `sample_statement.csv` first

---

## Performance Testing

For larger files, monitor:

```python
# Time ingestion
import time
start = time.time()
count = service.ingest_file(large_file, user_id="test")
elapsed = time.time() - start
print(f"Processed {count} records in {elapsed:.2f}s")
```

**Expected Performance:**
- 100 transactions: < 1 second
- 1,000 transactions: < 5 seconds
- 10,000 transactions: < 30 seconds

---

## Next Steps After Testing

1. **Connect to Production Supabase**
   - Update .env with production credentials
   - Run initial data migration

2. **Integrate with Agents**
   - Feed clean_transactions to categorization agents
   - Use raw_transactions for audit trail

3. **Add PDF OCR** (Optional)
   - Support scanned/image-based PDFs
   - Use `easyocr` or `tesseract`

4. **Implement Batch Processing**
   - Async file uploads
   - Progress tracking UI
   - Email notifications

5. **Add Bank Detection**
   - Auto-classify by PDF structure
   - Bank-specific column mapping

