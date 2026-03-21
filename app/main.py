import sys
import os
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from services.ingestion_service import IngestionService
from components.ui import apply_theme, alert_banner

st.set_page_config(
    page_title="Finance Audit - Upload",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

DEMO_USER_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, "demo-user"))

with st.sidebar:
    st.image(
        "app/assets/Gemini_Generated_Image_ri1spbri1spbri1s-removebg-preview.png",
        width=200,
    )
    st.markdown(
        """
        <div class="sidebar-brand">
            <h1>Finance Audit</h1>
            <p>Enterprise Edition</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="sidebar-section-title">Navigation</p>', unsafe_allow_html=True
    )
    st.page_link("main.py", label="📤 Upload Statement")
    st.page_link("pages/dashboard.py", label="📈 Dashboard")

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    st.markdown(
        '<p class="sidebar-section-title">Quick Links</p>', unsafe_allow_html=True
    )
    st.markdown("📊 View Analytics")
    st.markdown("🔍 Search Transactions")

st.markdown(
    """
    <style>
    .hero-container {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
        border-radius: 16px;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .hero-container h1 {
        color: white !important;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .hero-container p {
        color: rgba(255,255,255,0.8);
        font-size: 1.1rem;
        margin: 0;
    }
    .features-row {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
    }
    .feature-card {
        flex: 1;
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    .feature-card .icon {
        font-size: 2rem;
        margin-bottom: 0.75rem;
    }
    .feature-card h3 {
        font-size: 1rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    .feature-card p {
        font-size: 0.85rem;
        color: #64748b;
        margin: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-container">
        <h1>📊 Personal Finance Audit</h1>
        <p>Intelligent financial analysis and spending insights powered by AI</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="features-row">
    <div class="feature-card">
        <div class="icon">📄</div>
        <h3>Smart Import</h3>
        <p>Upload CSV or PDF bank statements for automatic processing</p>
    </div>
    <div class="feature-card">
        <div class="icon">🔍</div>
        <h3>AI Categorization</h3>
        <p>Machine learning automatically categorizes your transactions</p>
    </div>
    <div class="feature-card">
        <div class="icon">📈</div>
        <h3>Deep Insights</h3>
        <p>Discover spending patterns, trends, and opportunities</p>
    </div>
    <div class="feature-card">
        <div class="icon">🔒</div>
        <h3>Private & Secure</h3>
        <p>Your financial data stays private and secure</p>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<style>
.upload-section {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.upload-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #e2e8f0;
}
.upload-header .icon {
    font-size: 2rem;
}
.upload-header h2 {
    margin: 0;
    font-size: 1.25rem;
    color: #1e293b;
}
.upload-header p {
    margin: 0.25rem 0 0 0;
    font-size: 0.875rem;
    color: #64748b;
}
.file-types {
    display: flex;
    gap: 0.75rem;
    margin-top: 1rem;
}
.file-type {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: #f1f5f9;
    border-radius: 8px;
    font-size: 0.85rem;
    color: #475569;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="upload-section">
    <div class="upload-header">
        <div class="icon">📤</div>
        <div>
            <h2>Upload Your Bank Statement</h2>
            <p>Get started by uploading your bank statement file</p>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Drag and drop your bank statement here",
    type=["csv", "pdf"],
    help="Supported formats: CSV, PDF",
    label_visibility="collapsed",
)

st.markdown(
    """
    <div class="file-types">
        <div class="file-type">📊 CSV</div>
        <div class="file-type">📄 PDF</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

if uploaded_file:
    with st.spinner("Processing your statement..."):
        service = IngestionService()
        result = service.ingest_file(uploaded_file, user_id=DEMO_USER_ID)

    st.markdown("---")

    col1, col2 = st.columns([1, 2])

    with col1:
        alert_banner(
            f"Successfully processed **{result['count']} transactions**",
            alert_type="success",
        )

        st.markdown(
            """
        <div style="background: #eff6ff; border-radius: 12px; padding: 1.25rem; border: 1px solid #bfdbfe;">
            <h4 style="margin: 0 0 0.75rem 0; color: #1e40af; font-size: 0.9rem; font-weight: 600;">
                What's Next?
            </h4>
            <p style="margin: 0; color: #3b82f6; font-size: 0.85rem;">
                Navigate to the <strong>Dashboard</strong> page to explore detailed insights, 
                spending patterns, and AI-powered recommendations.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        if result["categories"]:
            st.markdown(
                """
            <div style="background: white; border-radius: 12px; padding: 1.5rem; border: 1px solid #e2e8f0;">
                <h3 style="margin: 0 0 1rem 0; color: #1e293b; font-size: 1rem; font-weight: 600;">
                    Transaction Categories
                </h3>
            </div>
            """,
                unsafe_allow_html=True,
            )

            sorted_cats = sorted(
                result["categories"].items(), key=lambda x: x[1], reverse=True
            )

            total = sum(result["categories"].values())

            for cat, count in sorted_cats:
                pct = (count / total) * 100

                color_map = {
                    "Food & Dining": "#f59e0b",
                    "Transport": "#3b82f6",
                    "Shopping": "#ec4899",
                    "Entertainment": "#8b5cf6",
                    "Bank Transfer": "#06b6d4",
                    "Transfer": "#06b6d4",
                    "Bills & Utilities": "#ef4444",
                    "Rent": "#8b5cf6",
                    "Health": "#10b981",
                    "Investment": "#3b82f6",
                    "Uncategorized": "#94a3b8",
                }
                color = color_map.get(cat, "#64748b")

                st.markdown(
                    f"""
                <div style="display: flex; align-items: center; gap: 1rem; margin: 0.5rem 0;">
                    <div style="width: 100px; font-size: 0.85rem; color: #475569;">
                        {cat}
                    </div>
                    <div style="flex: 1; background: #f1f5f9; border-radius: 4px; height: 24px; overflow: hidden;">
                        <div style="width: {pct}%; background: {color}; height: 100%; border-radius: 4px;"></div>
                    </div>
                    <div style="width: 50px; text-align: right; font-size: 0.85rem; color: #64748b;">
                        {count}
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

st.markdown("---")

st.markdown(
    """
<div style="text-align: center; padding: 2rem 0; color: #94a3b8; font-size: 0.85rem;">
    <p style="margin: 0;">Finance Audit System • Powered by AI</p>
</div>
""",
    unsafe_allow_html=True,
)
