import os

import pandas as pd

from services.pdf_parser_service import parse_pdf, _coerce_numeric
from utils.hashing import generate_txn_hash
from data.repositories.transaction_repo import TransactionRepo


def _safe_get_value(row, *keys):
    """Safely get a single value from a row, handling duplicate columns and Series returns."""
    for key in keys:
        val = row.get(key)
        if val is not None:
            if isinstance(val, pd.Series):
                val = val.iloc[0] if len(val) > 0 else None
            return val
    return None


class IngestionService:
    def __init__(self):
        self.repo = TransactionRepo()

    def _normalize_dataframe(self, df: pd.DataFrame, user_id: str) -> int:
        """Normalize a DataFrame into clean transaction records.

        Stores raw parsed records into `raw_transactions` and upserts normalized
        transactions into `clean_transactions`.

        Returns:
            Number of clean records processed.
        """
        try:
            # Deduplicate columns to avoid pandas warning
            df = df.loc[:, ~df.columns.duplicated()]
            raw_data = df.to_dict(orient="records")
            self.repo.insert_raw({"user_id": user_id, "raw_data": raw_data})
        except Exception as e:
            print(f"[INGESTION] Warning: Failed to insert raw data: {e}")
            # Continue processing even if raw data insert fails

        records = []
        for _, row in df.iterrows():
            txn_date_raw = _safe_get_value(row, "transaction date", "date")
            txn_date = None
            if pd.notna(txn_date_raw):
                try:
                    parsed_date = pd.to_datetime(txn_date_raw, errors="coerce")
                    if pd.notna(parsed_date):
                        txn_date = parsed_date.date().isoformat()
                    else:
                        txn_date = str(txn_date_raw)
                except Exception:
                    txn_date = str(txn_date_raw) if txn_date_raw else None

            description = _safe_get_value(row, "descriptions", "description") or ""
            debit = _coerce_numeric(_safe_get_value(row, "debit"))
            credit = _coerce_numeric(_safe_get_value(row, "credit"))
            amount = _coerce_numeric(
                _safe_get_value(row, "transaction amount", "amount")
            )

            # Derive net amount if missing
            if amount is None:
                if debit is not None:
                    amount = debit
                elif credit is not None:
                    amount = -credit

            txn_hash = generate_txn_hash(txn_date, amount, description)

            records.append(
                {
                    "user_id": user_id,
                    "txn_date": txn_date,
                    "description": description,
                    "debit": debit,
                    "credit": credit,
                    "amount": amount,
                    "txn_hash": txn_hash,
                }
            )

        if not records:
            print("[INGESTION] No records to insert")
            return 0

        self.repo.bulk_insert_clean(records)
        return len(records)

    def ingest_file(self, file, user_id):
        """Ingest a CSV or PDF bank statement file."""
        filename = None
        if hasattr(file, "name"):
            filename = file.name
        elif isinstance(file, str):
            filename = file

        ext = os.path.splitext(filename or "")[1].lower()

        if ext == ".pdf":
            df, method = parse_pdf(file)  # Unpack tuple: (DataFrame, parsing_method)
            print(f"[INGESTION] PDF parsed using: {method.upper()} method")
        else:
            df = pd.read_csv(file)
            print(f"[INGESTION] CSV file loaded")

        return self._normalize_dataframe(df, user_id)

    def ingest_csv(self, file, user_id):
        """Backward-compatible CSV ingestion helper."""
        return self.ingest_file(file, user_id)
