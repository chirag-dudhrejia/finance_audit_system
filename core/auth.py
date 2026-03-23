"""
Authentication service wrapping Supabase Auth SDK.
Provides sign up, sign in, sign out, and session management.
"""

from supabase import create_client, Client
from core.config import settings

_client: Client = None


def _get_client() -> Client:
    global _client
    if _client is None:
        _client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    return _client


def sign_up(email: str, password: str) -> dict:
    """Register a new user with email and password.

    Returns:
        dict with keys: success, user_id, email, error
    """
    try:
        client = _get_client()
        response = client.auth.sign_up({"email": email, "password": password})
        if response.user:
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
        if response.user:
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


def get_current_user() -> dict | None:
    """Get the current authenticated user from Supabase session.

    Returns:
        dict with keys: user_id, email or None if not authenticated
    """
    try:
        client = _get_client()
        session = client.auth.get_session()
        if session and session.user:
            return {
                "user_id": session.user.id,
                "email": session.user.email,
            }
    except Exception:
        pass
    return None
