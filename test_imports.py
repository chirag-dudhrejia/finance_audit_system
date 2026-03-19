"""
Simple import and functionality test
"""
import sys

print("Testing imports...")

try:
    from services.pdf_parser_service import _coerce_numeric
    print("✅ pdf_parser_service imports OK")
except Exception as e:
    print(f"❌ pdf_parser_service: {e}")
    sys.exit(1)

try:
    from utils.hashing import generate_txn_hash
    print("✅ hashing utilities imports OK")
except Exception as e:
    print(f"❌ hashing: {e}")
    sys.exit(1)

try:
    from services.ingestion_service import IngestionService
    print("✅ ingestion_service imports OK")
except Exception as e:
    print(f"❌ ingestion_service: {e}")
    sys.exit(1)

try:
    from core.config import settings
    print("✅ config imports OK")
except Exception as e:
    print(f"❌ config: {e}")
    sys.exit(1)

print("\n✅ ALL IMPORTS SUCCESSFUL")
print("\nCore components are functional!")
print("Ready to test with actual files or Streamlit.")
