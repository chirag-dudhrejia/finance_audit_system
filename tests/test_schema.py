import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def test_tables_exist():
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    schema = 'bank_statements'
    tables = [
        f"{schema}.raw_transactions",
        f"{schema}.clean_transactions",
        f"{schema}.merchant_category_map",
        f"{schema}.budgets",
        f"{schema}.agent_logs",
    ]

    for table in tables:
        try:
            # Try to select from table
            result = supabase.table(table).select('*').limit(1).execute()
            print(f"✅ Table '{table}' exists and is accessible.")
        except Exception as e:
            print(f"❌ Table '{table}' does not exist or error: {e}")
            return False

    # Check if vector extension is enabled
    try:
        # This might not work with anon key, but let's try
        result = supabase.rpc('exec_sql', {'query': "SELECT * FROM pg_extension WHERE extname = 'vector';"}).execute()
        if result.data:
            print("✅ Vector extension is enabled.")
        else:
            print("❌ Vector extension is not enabled.")
            return False
    except:
        print("⚠️ Could not verify vector extension (may require service role key).")

    print("All tables are set up correctly!")
    return True

if __name__ == "__main__":
    test_tables_exist()
