import sys
import os

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

# Auth gate: check if user is logged in
if "user_id" not in st.session_state:
    # Hide sidebar on auth pages
    st.markdown(
        "<style>[data-testid='stSidebar'] { display: none !important; }</style>",
        unsafe_allow_html=True,
    )
    pg = st.navigation(
        [st.Page("pages/login.py", title="Login", icon="🔑", url_path="login")],
        position="hidden",
    )
    pg.run()
else:
    # Authenticated — show main app
    user_id = st.session_state.user_id
    user_email = st.session_state.get("user_email", "")

    repo = TransactionRepo()
    txn_count = len(repo.get_transactions(user_id))

    with st.sidebar:
        render_sidebar(transaction_count=txn_count, user_email=user_email)

    pages = [
        st.Page(
            "pages/dashboard.py", title="Dashboard", icon="📊", url_path="dashboard"
        ),
        st.Page(
            "pages/upload.py",
            title="Upload Statement",
            icon="📤",
            url_path="upload",
        ),
        st.Page("pages/logout.py", title="Logout", icon="🚪", url_path="logout"),
    ]

    pg = st.navigation(pages, position="sidebar")
    pg.run()
