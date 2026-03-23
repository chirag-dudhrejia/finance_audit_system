"""
Logout handler for Finance Audit System.
Shows confirmation dialog before logging out.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import streamlit as st
from core.auth import sign_out


def perform_logout():
    """Clear session and redirect to login."""
    sign_out()
    for key in ["user_id", "user_email"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()


# Show confirmation dialog
st.markdown("### Confirm Logout")
st.warning("Are you sure you want to log out?")

col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    if st.button("Yes, Log Out", type="primary", use_container_width=True):
        perform_logout()
with col2:
    if st.button("Cancel", use_container_width=True):
        st.switch_page("pages/dashboard.py")
