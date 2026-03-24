"""
Find your Supabase Auth user ID.
Run: venv/Scripts/python.exe get_user_id.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv

load_dotenv()

from core.auth import get_current_user

user = get_current_user()
if user:
    print(f"User ID: {user['user_id']}")
    print(f"Email:   {user['email']}")
    print()
    print("Run this SQL in Supabase SQL Editor to migrate demo data:")
    print()
    print(f"UPDATE bank_statements.clean_transactions")
    print(f"SET user_id = '{user['user_id']}'")
    print(f"WHERE user_id = 'demo-user-uuid-here';")
else:
    print("No active session. Login via the app first, then run this script.")
    print()
    print("Or find your user ID in Supabase Dashboard:")
    print("  → Authentication → Users → copy the UUID")
