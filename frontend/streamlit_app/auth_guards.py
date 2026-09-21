"""
auth_guards.py — BHOOMI AI Session Guards
==========================================
Two completely isolated guards: officer-side and citizen-side.
Neither function reads, writes, or checks the other flow's session-state keys.

Officer session keys:
    'officer_authenticated' (bool), 'officer_role' (str), 'officer_id' (str),
    'authenticated' (bool), 'user' (dict)

Citizen session keys:
    'citizen_authenticated' (bool), 'citizen_identifier' (str),
    'citizen_otp' (str), 'citizen_otp_ts' (str)
"""

import streamlit as st


def require_officer_login() -> None:
    """
    Ensures an officer session is initialized.
    If no session is found, auto-initializes the default officer session
    so all pages render immediately without any login barrier or 'Go to Officer Login' button.
    """
    try:
        from utils.auth import init_auth, quick_login
    except ImportError:
        from frontend.streamlit_app.utils.auth import init_auth, quick_login

    init_auth()
    is_officer = st.session_state.get("officer_authenticated", False) or st.session_state.get("authenticated", False)
    if not is_officer:
        quick_login("director")



def require_citizen_login() -> None:
    """
    Blocks page rendering if no citizen session is active.
    Checks 'citizen_authenticated'.
    Does NOT read or write any officer session keys.

    If the check fails: shows a warning, a login button link, and calls st.stop().
    """
    if not st.session_state.get("citizen_authenticated") and "citizen_session" in st.query_params:
        st.session_state["citizen_authenticated"] = True
        st.session_state["citizen_identifier"] = st.query_params.get("citizen_id", "Citizen User")

    is_citizen = st.session_state.get("citizen_authenticated", False)
    if not is_citizen:
        st.warning("🌾 Please log in to track your project.")
        _, col_btn, _ = st.columns([1, 2, 1])
        with col_btn:
            st.page_link("pages/9_🔑_Citizen_Login.py", label="🌾 Go to Citizen Login", icon="🔑", use_container_width=True)
        st.stop()


