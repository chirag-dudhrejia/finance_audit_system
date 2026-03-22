import os
import math

import pandas as pd

from services.pdf_parser_service import parse_pdf, _coerce_numeric
from services.categorization_service import CategorizationService
from utils.hashing import generate_txn_hash
from data.repositories.transaction_repo import TransactionRepo


def _clean_nan(val):
    """Convert NaN/inf to None for JSON compliance."""
    if val is None:
        return None
    if isinstance(val, float):
        if math.isnan(val) or math.isinf(val):
            return None
    return val


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
        self.categorizer = CategorizationService()

    def _normalize_dataframe(self, df: pd.DataFrame, user_id: str) -> dict:
        """Normalize and categorize all transactions.

        Returns:
            dict with keys: count, categories
        """
        try:
            df = df.loc[:, ~df.columns.duplicated()]
            raw_data = df.to_dict(orient="records")
            raw_data = [
                {
                    k: None
                    if isinstance(v, float) and (math.isnan(v) or math.isinf(v))
                    else v
                    for k, v in rec.items()
                }
                for rec in raw_data
            ]
            self.repo.insert_raw({"user_id": user_id, "raw_data": raw_data})
        except Exception as e:
            print(f"[INGESTION] Warning: Failed to insert raw data: {e}")

        # Build normalized records
        records = []
        for _, row in df.iterrows():
            txn_date_raw = _safe_get_value(row, "transaction date", "date")
            txn_date = None
            if pd.notna(txn_date_raw):
                try:
                    date_str = str(txn_date_raw).strip()
                    if (
                        len(date_str) == 10
                        and date_str[4] == "-"
                        and date_str[7] == "-"
                    ):
                        parsed_date = pd.to_datetime(date_str, format="%Y-%m-%d")
                    else:
                        parsed_date = pd.to_datetime(
                            date_str, errors="coerce", dayfirst=True
                        )
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
                    "debit": _clean_nan(debit),
                    "credit": _clean_nan(credit),
                    "amount": _clean_nan(amount),
                    "txn_hash": txn_hash,
                }
            )

        if not records:
            print("[INGESTION] No records to insert")
            return {"count": 0, "categories": {}}

        # Categorize each transaction (two-pass: rules first, then batch LLM)
        print(f"[INGESTION] Categorizing {len(records)} transactions...")
        category_summary = {}

        # Pass 1: Rule-based categorization, collect fallbacks
        fallback_indices = []
        for i, rec in enumerate(records):
            cat = self.categorizer.categorize(rec["description"])
            if cat == "PENDING_LLM":
                fallback_indices.append(i)
            else:
                rec["category"] = cat
                category_summary[cat] = category_summary.get(cat, 0) + 1

        # Pass 2: Batch LLM for fallbacks
        if fallback_indices:
            print(
                f"[INGESTION] {len(fallback_indices)} transactions need LLM categorization (batching in chunks of 15)..."
            )
            fallback_descs = [records[i]["description"] for i in fallback_indices]
            batch_results = self.categorizer.categorize_batch(fallback_descs)
            for idx, cat in zip(fallback_indices, batch_results):
                records[idx]["category"] = cat
                category_summary[cat] = category_summary.get(cat, 0) + 1

        print(f"[INGESTION] Categories: {category_summary}")

        df = pd.DataFrame(records)
        df.to_csv("debug_records_before.csv", index=False)

        # Final cleanup: remove any NaN values from all records
        for rec in records:
            for key in rec:
                rec[key] = _clean_nan(rec[key])

        # this line is for coding agent here write the code for saving the records to the csv file for debugging purpose
        df = pd.DataFrame(records)
        df.to_csv("debug_records_after.csv", index=False)

        # Insert into DB
        self.repo.bulk_insert_clean(records)

        return {
            "count": len(records),
            "categories": category_summary,
        }

    def ingest_file(self, file, user_id) -> dict:
        """Ingest a CSV or PDF bank statement file."""
        filename = None
        if hasattr(file, "name"):
            filename = file.name
        elif isinstance(file, str):
            filename = file

        ext = os.path.splitext(filename or "")[1].lower()

        if ext == ".pdf":
            df, method = parse_pdf(file)
            print(f"[INGESTION] PDF parsed using: {method.upper()} method")
        else:
            df = pd.read_csv(file)
            print("[INGESTION] CSV file loaded")

        return self._normalize_dataframe(df, user_id)

    def ingest_csv(self, file, user_id):
        """Backward-compatible CSV ingestion helper."""
        return self.ingest_file(file, user_id)
