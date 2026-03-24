from supabase import create_client
from core.config import settings

SCHEMA = "bank_statements"


class TransactionRepo:
    def __init__(self):
        self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    def insert_raw(self, record):
        self.client.schema(SCHEMA).table("raw_transactions").insert(record).execute()

    def bulk_insert_clean(self, records):
        self.client.schema(SCHEMA).table("clean_transactions").upsert(
            records, on_conflict="txn_hash"
        ).execute()

    def bulk_insert(self, records):
        self.bulk_insert_clean(records)

    def get_transactions(self, user_id: str) -> list[dict]:
        """Fetch all transactions for a user, ordered by date."""
        result = (
            self.client.schema(SCHEMA)
            .table("clean_transactions")
            .select("*")
            .eq("user_id", user_id)
            .order("txn_date", desc=False)
            .execute()
        )
        return result.data or []
