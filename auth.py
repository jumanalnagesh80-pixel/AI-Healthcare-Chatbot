"""
Authentication module for AI Healthcare Chatbot
Handles user authentication and session management
"""

import streamlit as st
from typing import Optional, Dict


def init_session_state():
    """Initialize session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "login"


def login_user(user: Dict):
    """Log in a user"""
    st.session_state.authenticated = True
    st.session_state.user = user
    if user['role'] == 'admin':
        st.session_state.current_page = "admin_dashboard"
    else:
        st.session_state.current_page = "patient_portal"


def logout_user():
    """Log out the current user"""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.current_page = "login"
    if "current_patient" in st.session_state:
        st.session_state.current_patient = None
    if "chat_history" in st.session_state:
        st.session_state.chat_history = []


def is_authenticated() -> bool:
    """Check if user is authenticated"""
    return st.session_state.get("authenticated", False)


def is_admin() -> bool:
    """Check if current user is admin"""
    user = st.session_state.get("user")
    return user and user.get("role") == "admin"


def get_current_user() -> Optional[Dict]:
    """Get current logged in user"""
    return st.session_state.get("user")


def require_auth(func):
    """Decorator to require authentication"""
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            st.warning("⚠️ Please log in to access this page")
            st.stop()
        return func(*args, **kwargs)
    return wrapper


def require_admin(func):
    """Decorator to require admin role"""
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            st.warning("⚠️ Please log in to access this page")
            st.stop()
        if not is_admin():
            st.error("❌ You don't have permission to access this page")
            st.stop()
        return func(*args, **kwargs)
    return wrapper
