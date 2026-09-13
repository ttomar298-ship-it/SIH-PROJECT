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

def init_auth():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        st.session_state["user"] = None

def is_authenticated():
    init_auth()
    return st.session_state.get("authenticated", False)

def get_current_user():
    init_auth()
    return st.session_state.get("user")

def login(email: str, password: str) -> bool:
    init_auth()
    email_clean = email.strip().lower()
    if email_clean in DEMO_USERS:
        user_data = DEMO_USERS[email_clean]
        if password in user_data["passwords"] or password == "admin":
            st.session_state["authenticated"] = True
            st.session_state["user"] = {
                "email": email_clean,
                "name": user_data["name"],
                "role": user_data["role"],
                "org": user_data["org"],
                "badge": user_data["badge"],
                "avatar": user_data["avatar"]
            }
            return True
    # Fallback generic login for any testing email
    if password in ["admin", "admin123", "bhoomi", "bhoomi123"] and "@" in email_clean:
        st.session_state["authenticated"] = True
        st.session_state["user"] = {
            "email": email_clean,
            "name": email_clean.split("@")[0].title() + " Officer",
            "role": "Infrastructure Monitoring Officer",
            "org": "PM GatiShakti Land Cell",
            "badge": "Verified Officer",
            "avatar": "🛡️"
        }
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
    st.session_state["authenticated"] = True
    st.session_state["user"] = {
        "email": email,
        "name": user_data["name"],
        "role": user_data["role"],
        "org": user_data["org"],
        "badge": user_data["badge"],
        "avatar": user_data["avatar"]
    }
    st.rerun()

def logout():
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
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
                <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); border-radius: 12px; padding: 12px 14px; margin-bottom: 16px; border: 1px solid #334155; color: white;">
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
