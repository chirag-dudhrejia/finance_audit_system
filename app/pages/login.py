"""
Login and Signup page for Finance Audit System.
Brand card (top) + Form with header (bottom), no wrapping divs.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import streamlit as st
from core.auth import sign_in, sign_up

if "auth_view" not in st.session_state:
    st.session_state.auth_view = "login"

CHART_SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>'
EMAIL_SVG = '<svg viewBox="0 0 24 24" width="16" height="16"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>'
LOCK_SVG = '<svg viewBox="0 0 24 24" width="16" height="16"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>'
USER_SVG = '<svg viewBox="0 0 24 24" width="16" height="16"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'

LOGIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #f8fafc;
}

[data-testid="stSidebar"] {
    display: none !important;
}

.auth-brand-card {
    max-width: 480px;
    margin: 0.2rem
     auto 0 auto;
    display: flex;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    overflow: hidden;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
    background: #ffffff;
    min-height: 180px;
}

.auth-brand-left {
    flex: 0 0 38%;
    background: linear-gradient(135deg, #312e81 0%, #4f46e5 40%, #6366f1 100%);
    padding: 2.5rem 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
}

.auth-brand-left::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background:
        radial-gradient(ellipse at 20% 80%, rgba(99,102,241,0.5) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(129,140,248,0.35) 0%, transparent 50%);
    pointer-events: none;
}

.auth-brand-left .icon-box {
    width: 70px;
    height: 70px;
    background: rgba(255,255,255,0.2);
    border-radius: 12px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(255,255,255,0.25);
    position: relative;
    z-index: 1;
}

.auth-brand-left .icon-box svg {
    width: 52px;
    height: 52px;
    stroke: #ffffff;
    fill: none;
    stroke-width: 2;
    stroke-linecap: round;
    stroke-linejoin: round;
}

.auth-brand-right {
    flex: 1;
    padding: 2.5rem 2rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.auth-brand-right h1 {
    margin: 0;
    font-size: 1.375rem;
    font-weight: 700;
    color: #0f172a;
    letter-spacing: -0.01em;
}

.auth-brand-right p {
    margin: 0.375rem 0 0 0;
    font-size: 0.8125rem;
    color: #64748b;
    line-height: 1.5;
}

.auth-brand-right .tagline {
    margin-top: 1rem;
    font-size: 0.75rem;
    color: #94a3b8;
    padding-top: 0.75rem;
    border-top: 1px solid #f1f5f9;
}

.st-emotion-cache-1bcyifm {
    background: white;
}

/* Form header — inside the form card */
.auth-form-header h2 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 700;
    color: #0f172a;
    letter-spacing: -0.02em;
    padding-bottom: 0.5rem;
}

.auth-form-header .subtitle {
    margin: 0.25rem 0 0 0;
    font-size: 0.875rem;
    color: #64748b;
}

.auth-form-header .divider {
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, rgba(226, 232, 240, 0.6) 5%, rgba(226, 232, 240, 0.6) 80%, transparent 100%);
    margin: 0.25rem 0 0.75rem 0;
}

/* Form card */
.auth-form-card .stForm {
    max-width: 480px;
    margin: 0.75rem auto 0 auto !important;
    background: white;
    border: 1px solid #e2e8f0 !important;
    border-radius: 16px !important;
    padding: 1.75rem 2.25rem 1.75rem 2.25rem !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06) !important;
}

.auth-form-card .stForm label {
    font-size: 0.8125rem !important;
    font-weight: 600 !important;
    color: #1e293b !important;
    margin-bottom: 0.375rem !important;
}

.auth-form-card .stForm [data-testid="stTextInput"] {
    margin-bottom: 0.5rem;
}

.auth-form-card .stForm [data-testid="stTextInput"] input {
    border-radius: 10px !important;
    border: 1.5px solid #e2e8f0 !important;
    padding: 0.75rem 0.875rem !important;
    font-size: 0.875rem !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    background: #f8fafc !important;
}

.auth-form-card .stForm [data-testid="stTextInput"] input:focus {
    border-color: #4f46e5 !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,0.1) !important;
    background: #ffffff !important;
}

.auth-form-card .stForm [data-testid="stTextInput"] input::placeholder {
    color: #94a3b8 !important;
}

.auth-form-card .stForm [data-testid="stFormSubmitButton"] {
    margin-top: 1rem;
}

.auth-form-card .stForm [data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    font-weight: 600;
    font-size: 0.9375rem;
    letter-spacing: 0.02em;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(79,70,229,0.25);
}

.auth-form-card .stForm [data-testid="stFormSubmitButton"] button:hover {
    background: linear-gradient(135deg, #4338ca 0%, #4f46e5 100%);
    box-shadow: 0 4px 12px rgba(79,70,229,0.35);
    transform: translateY(-1px);
}

.auth-form-card .stForm [data-testid="stFormSubmitButton"] button:active {
    transform: translateY(0);
}

/* Error and success states */
.auth-form-card .stForm [data-testid="stAlert"] {
    border-radius: 10px !important;
    font-size: 0.8125rem !important;
    margin-top: 0.5rem !important;
}

</style>
"""


def render_login_page():
    st.markdown(LOGIN_CSS, unsafe_allow_html=True)

    log1, log2 = st.columns(2)
    with log1:
        st.markdown(
            f"""
        <div class="auth-brand-card">
            <div class="auth-brand-left">
                <div class="icon-box">
                    {CHART_SVG}
                </div>
            </div>
            <div class="auth-brand-right">
                <h1>Finance Audit</h1>
                <p>Intelligence Platform</p>
                <div class="tagline">Secure financial analysis powered by AI</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with log2:
        if st.session_state.auth_view == "login":
            _render_login_view()
        else:
            _render_signup_view()


def _render_login_view():
    with st.form("login_form", clear_on_submit=False):
        st.markdown(
            """<div class="auth-form-header">
    <h2>Welcome back</h2>
    <p class="subtitle">Sign in to your account</p>
    <div class="divider"></div>
</div>""",
            unsafe_allow_html=True,
        )
        email = st.text_input("Email", placeholder="you@example.com", key="login_email")
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password",
        )
        submit = st.form_submit_button(
            "Sign In", use_container_width=True, type="primary"
        )

        if submit:
            if not email or not password:
                st.error("Please enter both email and password")
                return

            with st.spinner("Signing in..."):
                result = sign_in(email.strip(), password)

            if result["success"]:
                st.session_state.user_id = result["user_id"]
                st.session_state.user_email = result["email"]
                st.session_state.auth_view = "login"
                st.rerun()
            else:
                st.error(result["error"])

    if st.button("Don't have an account? Create one", key="goto_signup"):
        st.session_state.auth_view = "signup"
        st.rerun()


def _render_signup_view():
    with st.form("signup_form", clear_on_submit=False):
        st.markdown(
            """<div class="auth-form-header">
    <h2>Create account</h2>
    <p class="subtitle">Get started with Finance Audit</p>
    <div class="divider"></div>
</div>""",
            unsafe_allow_html=True,
        )
        email = st.text_input(
            "Email", placeholder="you@example.com", key="signup_email"
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="At least 6 characters",
            key="signup_password",
        )
        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter password",
            key="signup_confirm",
        )
        submit = st.form_submit_button(
            "Create Account", use_container_width=True, type="primary"
        )

        if submit:
            if not email or not password or not confirm_password:
                st.error("Please fill in all fields")
                return

            if password != confirm_password:
                st.error("Passwords do not match")
                return

            if len(password) < 6:
                st.error("Password must be at least 6 characters")
                return

            with st.spinner("Creating account..."):
                result = sign_up(email.strip(), password)

            if result["success"]:
                st.session_state.user_id = result["user_id"]
                st.session_state.user_email = result["email"]
                st.session_state.auth_view = "login"
                st.success("Account created successfully!")
                st.rerun()
            else:
                st.error(result["error"])

    if st.button("Already have an account? Sign in", key="goto_login"):
        st.session_state.auth_view = "login"
        st.rerun()


render_login_page()
