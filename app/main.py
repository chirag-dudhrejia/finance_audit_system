import sys
import os
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from services.ingestion_service import IngestionService

st.set_page_config(page_title="Upload", layout="wide")

st.title("Personal Finance Audit")

DEMO_USER_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, "demo-user"))

uploaded_file = st.file_uploader(
    "Upload CSV or PDF bank statement", type=["csv", "pdf"]
)

if uploaded_file:
    service = IngestionService()
    result = service.ingest_file(uploaded_file, user_id=DEMO_USER_ID)

    st.success(f"Uploaded & processed {result['count']} transactions.")

    if result["categories"]:
        st.subheader("Category Breakdown")
        st.bar_chart(result["categories"])

    st.info("Go to the **Dashboard** page in the sidebar to see detailed insights.")
