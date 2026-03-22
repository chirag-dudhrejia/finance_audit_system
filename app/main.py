import sys
import os
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from components.ui import apply_theme, render_sidebar
from data.repositories.transaction_repo import TransactionRepo

st.set_page_config(
    page_title="Finance Audit",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

DEMO_USER_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, "demo-user"))
repo = TransactionRepo()
txn_count = len(repo.get_transactions(DEMO_USER_ID))

with st.sidebar:
    render_sidebar(transaction_count=txn_count)

pages = [
    st.Page("pages/dashboard.py", title="Dashboard", icon="📊", url_path="dashboard"),
    st.Page("pages/upload.py", title="Upload Statement", icon="📤", url_path="upload"),
]

pg = st.navigation(pages, position="sidebar")
pg.run()
