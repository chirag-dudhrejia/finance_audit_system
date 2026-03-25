"""
Authentication service wrapping Supabase Auth SDK.
Provides sign up, sign in, sign out, and session management.
"""

import streamlit as st
from supabase import create_client, Client
from core.config import settings


def _get_client() -> Client:
    """Create a fresh client and attach THIS user's session from st.session_state"""
    client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    # Re-attach this specific user's session if it exists
    if "sb_access_token" in st.session_state and "sb_refresh_token" in st.session_state:
        try:
            client.auth.set_session(
                st.session_state["sb_access_token"],
                st.session_state["sb_refresh_token"],
            )
        except Exception:
            # Invalid/expired session, clear it
            st.session_state.pop("sb_access_token", None)
            st.session_state.pop("sb_refresh_token", None)

    return client


def sign_up(email: str, password: str) -> dict:
    """Register a new user with email and password.

    Returns:
        dict with keys: success, user_id, email, error
    """
    try:
        client = _get_client()
        response = client.auth.sign_up({"email": email, "password": password})
        if response.user and response.session:
            # Store session in THIS user's session_state
            st.session_state["sb_access_token"] = response.session.access_token
            st.session_state["sb_refresh_token"] = response.session.refresh_token

            return {
                "success": True,
                "user_id": response.user.id,
                "email": response.user.email,
                "error": None,
            }
        return {
            "success": False,
            "user_id": None,
            "email": None,
            "error": "Signup failed",
        }
    except Exception as e:
        return {"success": False, "user_id": None, "email": None, "error": str(e)}


def sign_in(email: str, password: str) -> dict:
    """Sign in with email and password.

    Returns:
        dict with keys: success, user_id, email, error
    """
    try:
        client = _get_client()
        response = client.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        if response.user and response.session:
            # Store session in THIS user's session_state
            st.session_state["sb_access_token"] = response.session.access_token
            st.session_state["sb_refresh_token"] = response.session.refresh_token

            return {
                "success": True,
                "user_id": response.user.id,
                "email": response.user.email,
                "error": None,
            }
        return {
            "success": False,
            "user_id": None,
            "email": None,
            "error": "Login failed",
        }
    except Exception as e:
        error_msg = str(e)
        if "Invalid login credentials" in error_msg:
            error_msg = "Invalid email or password"
        elif "Email not confirmed" in error_msg:
            error_msg = "Please verify your email before logging in"
        return {"success": False, "user_id": None, "email": None, "error": error_msg}


def sign_out() -> None:
    """Sign out the current user."""
    try:
        client = _get_client()
        client.auth.sign_out()
    except Exception:
        pass
    finally:
        # Clear THIS user's session from session_state
        st.session_state.pop("sb_access_token", None)
        st.session_state.pop("sb_refresh_token", None)


def get_current_user() -> dict | None:
    """Get the current authenticated user from Supabase session.

    Returns:
        dict with keys: user_id, email or None if not authenticated
    """
    try:
        client = _get_client()
        user = client.auth.get_user()
        if user and user.user:
            return {
                "user_id": user.user.id,
                "email": user.user.email,
            }
    except Exception:
        pass
    return None
