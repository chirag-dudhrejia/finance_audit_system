#!/usr/bin/env python3
"""
PDF Parser Testing Script
=========================

This script tests the PDF parsing functionality independently.
It can be used to debug PDF parsing issues without running the full Streamlit app.

Usage:
    python explore/test_pdf_parser.py <path_to_pdf_file>

Example:
    python explore/test_pdf_parser.py "OpTransactionHistory17-03-2026.pdf-20-19-08.pdf"

The script will:
1. Load the PDF file
2. Attempt table extraction
3. Fall back to LLM parsing if needed
4. Display the extracted transactions
5. Show detailed debugging information
"""

import sys
import os
import pandas as pd
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from services.pdf_parser_service import parse_pdf
from core.config import settings

def test_pdf_parser(pdf_path: str):
    """Test PDF parsing with detailed output."""

    print("=" * 80)
    print("PDF PARSER TESTING SCRIPT")
    print("=" * 80)

    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"❌ ERROR: PDF file not found: {pdf_path}")
        return

    print(f"📁 Testing PDF: {pdf_path}")
    print(f"📊 File size: {os.path.getsize(pdf_path)} bytes")

    try:
        # Read the PDF file
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()

        print(f"\n🔄 Starting PDF parsing...")
        print("-" * 50)

        # Parse the PDF
        df, method = parse_pdf(pdf_data)

        print("-" * 50)
        print("✅ PARSING SUCCESSFUL!")
        print(f"📋 Parsing method used: {method.upper()}")
        print(f"📊 Transactions extracted: {len(df)}")

        if len(df) > 0:
            print("\n📋 EXTRACTED TRANSACTIONS:")
            print("-" * 50)
            print(df.to_string(index=False))

            print("\n📈 SUMMARY:")
            print(f"   Total transactions: {len(df)}")
            print(f"   Columns: {', '.join(df.columns.tolist())}")

            # Show some statistics
            numeric_cols = ['debit', 'credit', 'transaction amount']
            for col in numeric_cols:
                if col in df.columns:
                    non_null = df[col].notna().sum()
                    print(f"   {col}: {non_null} non-null values")

        else:
            print("⚠️  WARNING: No transactions were extracted from the PDF")

    except Exception as e:
        print("❌ PARSING FAILED!")      
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()

    print("\n" + "=" * 80)

def main():
    """Main function to handle command line arguments."""

    if len(sys.argv) != 2:
        print("Usage: python explore/test_pdf_parser.py <path_to_pdf_file>")
        print("\nExample:")
        print('python explore/test_pdf_parser.py "OpTransactionHistory17-03-2026.pdf-20-19-08.pdf"')
        print("\nAvailable PDF files in project root:")
        print(f"Project path : {project_root}")
        pdf_files = list(project_root.glob("*.pdf"))
        if pdf_files:
            for pdf_file in pdf_files:
                print(f"  - {pdf_file.name}")
        else:
            print("  No PDF files found in project root")

    pdf_path = sys.argv[1]

    # If relative path, make it absolute from project root
    if not os.path.isabs(pdf_path):
        pdf_path = str(project_root / pdf_path)

    test_pdf_parser(pdf_path)

if __name__ == "__main__":
    print("started")
    main()