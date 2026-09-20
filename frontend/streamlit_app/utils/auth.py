import os
import base64
import streamlit as st

LOGO_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")

def get_logo_base64():
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

DEMO_USERS = {
    "director@gatishakti.gov.in": {
        "name": "Dr. Rajesh Varma, IAS",
        "role": "National Project Director",
        "org": "PM GatiShakti National Master Plan (DPIIT)",
        "badge": "National Clearance",
        "avatar": "🏛️",
        "passwords": ["admin", "admin123", "gati2024"]
    },
    "cala@revenue.gov.in": {
        "name": "Smt. Ananya Sharma",
        "role": "Competent Authority Land Acquisition (CALA)",
        "org": "Ministry of Road Transport & Highways (MoRTH)",
        "badge": "District Level CALA",
        "avatar": "⚖️",
        "passwords": ["cala", "cala123", "revenue"]
    },
    "mospi@gov.in": {
        "name": "Shri Vikramaditya Sen",
        "role": "Chief Statistical Officer",
        "org": "Ministry of Statistics & Programme Implementation (MoSPI)",
        "badge": "Central Monitor",
        "avatar": "📊",
        "passwords": ["mospi", "mospi123"]
    },
    "jury@sih.gov.in": {
        "name": "SIH Evaluation Jury",
        "role": "Technical Jury & Observer",
        "org": "Smart India Hackathon 2024 / MoRTH",
        "badge": "Jury Special",
        "avatar": "⭐",
        "passwords": ["sih", "sih2024", "jury"]
    }
}

import json

SESSION_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".session_officer.json"))

def _save_officer_session(data: dict) -> None:
    try:
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        pass

def _load_officer_session() -> dict | None:
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None

def _clear_officer_session() -> None:
    if os.path.exists(SESSION_FILE):
        try:
            os.remove(SESSION_FILE)
        except Exception:
            pass

def init_auth():
    # 1. Check in-memory session_state first
    if st.session_state.get("officer_authenticated") and st.session_state.get("user"):
        return

    # 2. Check query params or persistent session cache
    saved = _load_officer_session()
    officer_q = st.query_params.get("officer_session")

    if saved and saved.get("officer_authenticated"):
        st.session_state["officer_authenticated"] = True
        st.session_state["officer_role"] = saved.get("officer_role")
        st.session_state["officer_id"] = saved.get("officer_id")
        st.session_state["authenticated"] = True
        st.session_state["user"] = saved.get("user")
        return

    if officer_q:
        key_map = {
            "director": "director@gatishakti.gov.in",
            "cala": "cala@revenue.gov.in",
            "mospi": "mospi@gov.in",
            "jury": "jury@sih.gov.in"
        }
        email = key_map.get(officer_q, "director@gatishakti.gov.in")
        user_data = DEMO_USERS.get(email, DEMO_USERS["director@gatishakti.gov.in"])
        st.session_state["officer_authenticated"] = True
        st.session_state["officer_role"] = user_data["role"]
        st.session_state["officer_id"] = officer_q
        st.session_state["authenticated"] = True
        st.session_state["user"] = {
            "email": email,
            "name": user_data["name"],
            "role": user_data["role"],
            "org": user_data["org"],
            "badge": user_data["badge"],
            "avatar": user_data["avatar"]
        }
        _save_officer_session({
            "officer_authenticated": True,
            "officer_role": user_data["role"],
            "officer_id": officer_q,
            "authenticated": True,
            "user": st.session_state["user"]
        })
        return

    # Default fallback: auto-initialize as National Director so all pages load data smoothly without login barriers
    default_data = DEMO_USERS["director@gatishakti.gov.in"]
    st.session_state["officer_authenticated"] = True
    st.session_state["officer_role"] = default_data["role"]
    st.session_state["officer_id"] = "director"
    st.session_state["authenticated"] = True
    st.session_state["user"] = {
        "email": "director@gatishakti.gov.in",
        "name": default_data["name"],
        "role": default_data["role"],
        "org": default_data["org"],
        "badge": default_data["badge"],
        "avatar": default_data["avatar"]
    }
    _save_officer_session({
        "officer_authenticated": True,
        "officer_role": default_data["role"],
        "officer_id": "director",
        "authenticated": True,
        "user": st.session_state["user"]
    })

def is_authenticated():
    init_auth()
    return st.session_state.get("officer_authenticated", False) or st.session_state.get("authenticated", False)

def get_current_user():
    init_auth()
    return st.session_state.get("user")

def login(email: str, password: str) -> bool:
    init_auth()
    email_clean = email.strip().lower()
    if email_clean in DEMO_USERS:
        user_data = DEMO_USERS[email_clean]
        if password in user_data["passwords"] or password == "admin":
            role_slug = email_clean.split("@")[0]
            st.session_state["officer_authenticated"] = True
            st.session_state["officer_role"] = user_data["role"]
            st.session_state["officer_id"] = role_slug
            st.session_state["authenticated"] = True
            st.session_state["user"] = {
                "email": email_clean,
                "name": user_data["name"],
                "role": user_data["role"],
                "org": user_data["org"],
                "badge": user_data["badge"],
                "avatar": user_data["avatar"]
            }
            st.query_params["officer_session"] = role_slug
            _save_officer_session({
                "officer_authenticated": True,
                "officer_role": user_data["role"],
                "officer_id": role_slug,
                "authenticated": True,
                "user": st.session_state["user"]
            })
            return True
    # Fallback generic login for any testing email
    if password in ["admin", "admin123", "bhoomi", "bhoomi123"] and "@" in email_clean:
        role_title = "Infrastructure Monitoring Officer"
        st.session_state["officer_authenticated"] = True
        st.session_state["officer_role"] = role_title
        st.session_state["officer_id"] = email_clean
        st.session_state["authenticated"] = True
        st.session_state["user"] = {
            "email": email_clean,
            "name": email_clean.split("@")[0].title() + " Officer",
            "role": role_title,
            "org": "PM GatiShakti Land Cell",
            "badge": "Verified Officer",
            "avatar": "🛡️"
        }
        st.query_params["officer_session"] = "custom"
        _save_officer_session({
            "officer_authenticated": True,
            "officer_role": role_title,
            "officer_id": email_clean,
            "authenticated": True,
            "user": st.session_state["user"]
        })
        return True
    return False

def quick_login(role_key: str):
    init_auth()
    key_map = {
        "director": "director@gatishakti.gov.in",
        "cala": "cala@revenue.gov.in",
        "mospi": "mospi@gov.in",
        "jury": "jury@sih.gov.in"
    }
    email = key_map.get(role_key, "director@gatishakti.gov.in")
    user_data = DEMO_USERS[email]
    st.session_state["officer_authenticated"] = True
    st.session_state["officer_role"] = user_data["role"]
    st.session_state["officer_id"] = role_key
    st.session_state["authenticated"] = True
    st.session_state["user"] = {
        "email": email,
        "name": user_data["name"],
        "role": user_data["role"],
        "org": user_data["org"],
        "badge": user_data["badge"],
        "avatar": user_data["avatar"]
    }
    st.query_params["officer_session"] = role_key
    _save_officer_session({
        "officer_authenticated": True,
        "officer_role": user_data["role"],
        "officer_id": role_key,
        "authenticated": True,
        "user": st.session_state["user"]
    })

def logout():
    """Clears ONLY officer session state keys, session file, and query params. Never touches citizen_* keys."""
    _clear_officer_session()
    for k in ["officer_authenticated", "officer_role", "officer_id", "authenticated", "user"]:
        st.session_state.pop(k, None)
    st.session_state["officer_authenticated"] = False
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    if "officer_session" in st.query_params:
        del st.query_params["officer_session"]
    st.rerun()




def render_sidebar_brand():
    """Renders the official Bhoomi AI logo, title, and current logged-in officer profile in the sidebar."""
    init_auth()
    with st.sidebar:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=220)
        else:
            st.markdown("### 🌱 **BHOOMI AI**")

        st.markdown(
            """
            <div style="text-align: center; margin-top: -8px; margin-bottom: 14px;">
                <span style="font-size: 0.72rem; letter-spacing: 2px; color: #15803D; font-weight: 800;">LAND • DATA • BETTER TOMORROW</span><br>
                <span style="font-size: 0.68rem; color: #64748B; font-weight: 500;">PM GatiShakti | SIH26017</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        user = get_current_user()
        if user:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #064E3B 0%, #065F46 100%); border-radius: 12px; padding: 12px 14px; margin-bottom: 16px; border: 1px solid #047857; color: white;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="font-size: 1.8rem; background: rgba(255,255,255,0.1); border-radius: 50%; width: 44px; height: 44px; display: flex; align-items: center; justify-content: center;">
                            {user['avatar']}
                        </div>
                        <div style="overflow: hidden;">
                            <div style="font-weight: 700; font-size: 0.88rem; color: #F8FAFC; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">{user['name']}</div>
                            <div style="font-size: 0.72rem; color: #4ADE80; font-weight: 600;">{user['role']}</div>
                            <div style="font-size: 0.68rem; color: #94A3B8;">{user['org']}</div>
                        </div>
                    </div>
                    <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1); display: flex; justify-content: space-between; align-items: center;">
                        <span style="background: #166534; color: #BBF7D0; font-size: 0.65rem; font-weight: 700; padding: 2px 8px; border-radius: 10px;">🟢 {user['badge']}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("🚪 Log Out", key="sb_logout_btn", help="Sign out of Bhoomi AI session"):
                logout()
        else:
            st.markdown(
                """
                <div style="background: #FEF3C7; border: 1px solid #FCD34D; border-radius: 10px; padding: 10px; margin-bottom: 12px; text-align: center;">
                    <span style="font-size: 0.75rem; color: #92400E; font-weight: 600;">⚠️ Guest Viewing Session</span><br>
                    <span style="font-size: 0.70rem; color: #B45309;">Log in to access official approvals & alerts</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            c1, c2 = st.columns(2)
            with c1:
                if st.button("⚡ CALA Login", key="sb_cala_quick"):
                    quick_login("cala")
            with c2:
                if st.button("🏛️ Director", key="sb_director_quick"):
                    quick_login("director")

        st.markdown("<hr style='margin: 10px 0 16px 0; border: 0.5px solid #E2E8F0;'>", unsafe_allow_html=True)
