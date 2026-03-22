import sys
import os
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import streamlit as st
from services.ingestion_service import IngestionService
from components.ui import alert_banner

DEMO_USER_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, "demo-user"))

SVG_ICONS = {
    "upload": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>',
    "chart": '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>',
    "smart": '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg>',
    "ai": '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a4 4 0 0 1 4 4v1h1a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3H7a3 3 0 0 1-3-3v-8a3 3 0 0 1 3-3h1V6a4 4 0 0 1 4-4z"/><path d="M9 14h.01"/><path d="M15 14h.01"/><path d="M10 18h4"/></svg>',
    "insights": '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>',
    "security": '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>',
    "csv": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><path d="M8 13h2"/><path d="M8 17h2"/><path d="M14 13h2"/><path d="M14 17h2"/></svg>',
    "pdf": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><path d="M9 15v-2h2a1 1 0 1 1 0 2H9z"/></svg>',
}

MAIN_STYLES = """
<style>
.stApp {
    background: #f8fafc;
}
.stVerticalBlock {
    gap: 0.5rem;
}
.main-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem;
}
.hero-section {
    background: linear-gradient(135deg, #312e81 0%, #4f46e5 40%, #6366f1 100%);
    border-radius: 16px;
    padding: 1rem 1.5rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 20px rgba(79,70,229,0.2);
}
.hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background:
        radial-gradient(ellipse at 20% 80%, rgba(99,102,241,0.5) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(129,140,248,0.4) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(79,70,229,0.3) 0%, transparent 60%);
    animation: heroGlow 8s ease-in-out infinite;
}
@keyframes heroGlow {
    0%, 100% { opacity: 0.8; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.05); }
}
.hero-section::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}
.hero-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 72px;
    height: 72px;
    background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 18px;
    margin-bottom: 1.25rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2), 0 0 40px rgba(255,255,255,0.15);
    position: relative;
    border: 1px solid rgba(255,255,255,0.3);
    animation: floatIcon 3s ease-in-out infinite;
}
@keyframes floatIcon {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}
.hero-icon svg {
    color: #4f46e5;
    position: relative;
    z-index: 1;
}
.hero-title {
    font-size: 1.875rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 0.5rem 0;
    line-height: 1.2;
    letter-spacing: -0.02em;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    position: relative;
    z-index: 1;
}
.hero-subtitle {
    font-size: 1rem;
    color: rgba(255,255,255,0.9);
    margin: 0 auto;
    max-width: 500px;
    line-height: 1.5;
    position: relative;
    z-index: 1;
}
.features-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.25rem;
    margin-bottom: 1.5rem;
}
.feature-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid #e2e8f0;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.3s ease;
}
.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 32px rgba(15,23,42,0.08);
    border-color: #c7d2fe;
}
.feature-card:hover::before {
    transform: scaleX(1);
}
.feature-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 56px;
    height: 56px;
    background: linear-gradient(135deg, #eef2ff 0%, #ede9fe 100%);
    border-radius: 14px;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}
.feature-card:hover .feature-icon {
    transform: scale(1.05);
    box-shadow: 0 8px 24px rgba(79,70,229,0.2);
}
.feature-icon svg {
    color: #6d28d9;
}
.feature-card h3 {
    font-size: 1rem;
    font-weight: 600;
    color: #0f172a;
    margin: 0 0 0.375rem 0;
}
.feature-card p {
    font-size: 0.8125rem;
    color: #64748b;
    margin: 0;
    line-height: 1.5;
}
.upload-section {
    background: #ffffff;
    border-radius: 16px;
    padding: 1.75rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 3px rgba(15,23,42,0.04);
    margin-bottom: 1.5rem;
}
.upload-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.25rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid #f1f5f9;
}
.upload-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 52px;
    height: 52px;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    border-radius: 12px;
    flex-shrink: 0;
    box-shadow: 0 4px 16px rgba(79,70,229,0.3);
}
.upload-icon svg {
    color: #ffffff;
}
.upload-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: #0f172a;
    margin: 0 0 0.25rem 0;
}
.upload-subtitle {
    font-size: 0.875rem;
    color: #64748b;
    margin: 0;
}
.file-types {
    display: flex;
    gap: 0.75rem;
    margin-top: 1rem;
}
.file-type-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: #f8fafc;
    border-radius: 9999px;
    font-size: 0.8125rem;
    font-weight: 500;
    color: #475569;
    border: 1px solid #e2e8f0;
}
.file-type-badge svg {
    color: #64748b;
}
.next-step-card {
    background: linear-gradient(135deg, #eef2ff 0%, #ede9fe 100%);
    border-radius: 12px;
    padding: 1.25rem;
    border: 1px solid #c7d2fe;
}
.next-step-card h4 {
    color: #4f46e5;
    margin: 0 0 0.5rem 0;
    font-size: 0.875rem;
    font-weight: 600;
}
.next-step-card p {
    color: #6d28d9;
    margin: 0;
    font-size: 0.8125rem;
    line-height: 1.5;
}
.categories-card {
    flex: 1;
}
.category-bar {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 0.5rem 0;
}
.category-name {
    width: 120px;
    font-size: 0.8125rem;
    color: #475569;
    flex-shrink: 0;
}
.category-bar-track {
    flex: 1;
    background: #f1f5f9;
    border-radius: 6px;
    height: 24px;
    overflow: hidden;
}
.category-bar-fill {
    height: 100%;
    border-radius: 6px;
    transition: width 0.5s ease;
}
.category-count {
    width: 40px;
    text-align: right;
    font-size: 0.8125rem;
    color: #64748b;
}
.footer-section {
    text-align: center;
    padding: 2rem 0;
    color: #94a3b8;
}
.footer-section p {
    margin: 0;
    font-size: 0.8125rem;
}
@media (max-width: 768px) {
    .features-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    .success-section {
        flex-direction: column;
    }
}
</style>
"""

hero_html = f"""
<div class="hero-section">
    <div class="hero-icon">
        {SVG_ICONS["chart"]}
    </div>
    <div>
        <h1 class="hero-title">Personal Finance Audit</h1>
        <p class="hero-subtitle">Intelligent financial analysis and spending insights powered by AI</p>
    </div>
</div>
"""

features_html = f"""
<div class="features-grid">
    <div class="feature-card">
        <div class="feature-icon">
            {SVG_ICONS["smart"]}
        </div>
        <h3>Smart Import</h3>
        <p>Upload CSV or PDF bank statements for automatic processing</p>
    </div>
    <div class="feature-card">
        <div class="feature-icon">
            {SVG_ICONS["ai"]}
        </div>
        <h3>AI Categorization</h3>
        <p>Machine learning automatically categorizes your transactions</p>
    </div>
    <div class="feature-card">
        <div class="feature-icon">
            {SVG_ICONS["insights"]}
        </div>
        <h3>Deep Insights</h3>
        <p>Discover spending patterns, trends, and opportunities</p>
    </div>
    <div class="feature-card">
        <div class="feature-icon">
            {SVG_ICONS["security"]}
        </div>
        <h3>Private & Secure</h3>
        <p>Your financial data stays private and secure</p>
    </div>
</div>
"""

upload_header_html = f"""
<div class="upload-header">
    <div class="upload-icon">
        {SVG_ICONS["upload"]}
    </div>
    <div>
        <h2 class="upload-title">Upload Your Bank Statement</h2>
        <p class="upload-subtitle">Get started by uploading your bank statement file</p>
    </div>
</div>
"""

file_types_html = f"""
<div class="file-types">
    <div class="file-type-badge">
        {SVG_ICONS["csv"]}
        CSV
    </div>
    <div class="file-type-badge">
        {SVG_ICONS["pdf"]}
        PDF
    </div>
</div>
"""

st.markdown(MAIN_STYLES, unsafe_allow_html=True)

st.markdown('<div class="main-content">', unsafe_allow_html=True)
st.markdown(hero_html, unsafe_allow_html=True)
st.markdown(features_html, unsafe_allow_html=True)

upload_html = f"""
<div class="upload-section">
    {upload_header_html}
"""

st.markdown(upload_html, unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drag and drop your bank statement here",
    type=["csv", "pdf"],
    help="Supported formats: CSV, PDF",
    label_visibility="collapsed",
)

st.markdown(f"    {file_types_html}", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

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

        next_step_html = """
        <div class="next-step-card">
            <h4>What's Next?</h4>
            <p>Navigate to the <strong>Dashboard</strong> page to explore detailed insights, spending patterns, and AI-powered recommendations.</p>
        </div>
        """
        st.markdown(next_step_html, unsafe_allow_html=True)

    with col2:
        if result["categories"]:
            categories_html = """
            <div class="categories-card">
                <h4 style="margin: 0 0 1rem 0; font-size: 0.9375rem; font-weight: 600; color: #0f172a;">
                    Transaction Categories
                </h4>
            </div>
            """
            st.markdown(categories_html, unsafe_allow_html=True)

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
                    "Bank Transfer": "#6366f1",
                    "Transfer": "#6366f1",
                    "Bills & Utilities": "#ef4444",
                    "Rent": "#8b5cf6",
                    "Health": "#10b981",
                    "Investment": "#3b82f6",
                    "Uncategorized": "#94a3b8",
                }
                color = color_map.get(cat, "#64748b")

                category_bar_html = f"""
                <div class="category-bar">
                    <div class="category-name">{cat}</div>
                    <div class="category-bar-track">
                        <div class="category-bar-fill" style="width: {pct}%; background: {color};"></div>
                    </div>
                    <div class="category-count">{count}</div>
                </div>
                """
                st.markdown(category_bar_html, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="footer-section">
        <p>Finance Audit System • Powered by AI</p>
    </div>
    """,
    unsafe_allow_html=True,
)
