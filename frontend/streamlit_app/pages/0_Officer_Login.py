import sys
import os
import streamlit as st

# Ensure application directory and root are in sys.path
PAGE_DIR = os.path.abspath(os.path.dirname(__file__))
STREAMLIT_DIR = os.path.abspath(os.path.join(PAGE_DIR, ".."))
ROOT_DIR = os.path.abspath(os.path.join(PAGE_DIR, "..", "..", ".."))
for p in [PAGE_DIR, STREAMLIT_DIR, ROOT_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from utils.auth import (
    is_authenticated,
    get_current_user,
    login,
    quick_login,
    logout,
    render_sidebar_brand,
    DEMO_USERS,
    LOGO_PATH,
    get_logo_base64
)

st.set_page_config(
    page_title="Officer Login — Bhoomi AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Render global sidebar brand with logo
render_sidebar_brand()

# Custom CSS for Login Portal
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .login-container {
        max-width: 900px;
        margin: 0 auto;
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 40px -15px rgba(15, 23, 42, 0.12);
        border: 1px solid #E2E8F0;
        overflow: hidden;
    }
    
    .portal-hero {
        background: linear-gradient(135deg, #064E3B 0%, #065F46 40%, #047857 70%, #059669 100%);
        color: white;
        padding: 36px 40px;
        text-align: center;
        border-bottom: 4px solid #10B981;
    }
    
    .role-card {
        background: #F8FAFC;
        border: 1.5px solid #E2E8F0;
        border-radius: 14px;
        padding: 18px;
        text-align: center;
        transition: all 0.2s ease-in-out;
        height: 100%;
    }
    .role-card:hover {
        border-color: #10B981;
        background: #F0FDF4;
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.15);
    }
    
    .role-icon {
        font-size: 2.2rem;
        margin-bottom: 8px;
    }
    .role-title {
        font-weight: 700;
        font-size: 0.95rem;
        color: #0F172A;
    }
    .role-dept {
        font-size: 0.75rem;
        color: #64748B;
        margin-top: 4px;
        min-height: 34px;
    }
    
    .active-profile-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: white;
        border-radius: 16px;
        padding: 24px;
        border: 1px solid #334155;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Top Brand Header Banner
col_l, col_r = st.columns([1, 4])
with col_l:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=170)
    else:
        st.markdown("# 🌱")
with col_r:
    st.markdown("""
    <div style="padding-top: 10px;">
        <h1 style="margin: 0; font-size: 2.3rem; font-weight: 800; color: #064E3B; letter-spacing: -0.5px;">
            BHOOMI <span style="color: #10B981;">AI</span>
        </h1>
        <div style="font-size: 0.85rem; font-weight: 700; letter-spacing: 2px; color: #047857; margin-top: 2px;">
            LAND • DATA • BETTER TOMORROW
        </div>
        <div style="font-size: 0.95rem; color: #475569; margin-top: 4px;">
            National Infrastructure Land Acquisition & Delay Intelligence Portal • PM GatiShakti
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='margin: 16px 0 24px 0; border: 0.5px solid #E2E8F0;'>", unsafe_allow_html=True)

user = get_current_user()

if is_authenticated() and user:
    st.success(f"✅ **Session Active:** Logged in as **{user['name']}** ({user['role']})")
    
    c_card, c_actions = st.columns([2, 1])
    with c_card:
        st.markdown(f"""
        <div class="active-profile-card">
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="font-size: 3rem; background: rgba(255,255,255,0.1); border-radius: 50%; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; border: 2px solid #10B981;">
                    {user['avatar']}
                </div>
                <div>
                    <span style="background: #065F46; color: #6EE7B7; font-size: 0.72rem; font-weight: 700; padding: 3px 10px; border-radius: 12px; text-transform: uppercase;">
                        {user['badge']}
                    </span>
                    <h2 style="margin: 6px 0 2px 0; font-size: 1.4rem; color: #F8FAFC;">{user['name']}</h2>
                    <div style="color: #93C5FD; font-weight: 600; font-size: 0.9rem;">{user['role']}</div>
                    <div style="color: #94A3B8; font-size: 0.8rem; margin-top: 2px;">{user['org']}</div>
                    <div style="color: #64748B; font-size: 0.75rem; margin-top: 4px;">Official ID: <code>{user['email']}</code></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with c_actions:
        st.markdown("#### Session Controls")
        if st.button("🚪 Sign Out of Bhoomi AI", width="stretch", type="secondary"):
            logout()
            st.rerun()
            
        st.markdown("---")
        st.markdown("**Quick Navigation:**")
        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            st.page_link("app.py", label="📊 Dashboard", icon="📈", width="stretch")
            st.page_link("pages/4_GIS_Map.py", label="🗺️ GIS Map", icon="🌍", width="stretch")
        with col_nav2:
            st.page_link("pages/2_Risk_Ranking.py", label="⚠️ Risk Ranking", icon="🚨", width="stretch")
            st.page_link("pages/5_Alerts.py", label="🔔 Smart Alerts", icon="📬", width="stretch")

    st.markdown("---")
    st.markdown("### 🔄 Switch Officer Role")
    st.caption("Select a different department or jurisdiction to view role-tailored views and alerts:")

# Render Login Tabs (shown when not logged in, or as role-switcher when logged in)
tab_quick, tab_form = st.tabs(["⚡ 1-Click Fast Login (Presentation / Jury)", "🔐 Official Credentials Login"])

with tab_quick:
    st.markdown("#### Select Officer Role for Immediate Authentication:")
    st.caption("Pre-authorized credentials for Smart India Hackathon jury, district authorities, and ministry delegates.")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="role-card">
            <div class="role-icon">🏛️</div>
            <div class="role-title">National Director</div>
            <div class="role-dept">PM GatiShakti National Master Plan (DPIIT)</div>
            <span style="font-size: 0.7rem; background: #DBEAFE; color: #1E40AF; padding: 2px 8px; border-radius: 8px; font-weight: 600;">Full Access</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Log In as Director", key="btn_login_director", width="stretch", type="primary"):
            quick_login("director")

    with col2:
        st.markdown("""
        <div class="role-card">
            <div class="role-icon">⚖️</div>
            <div class="role-title">CALA Officer</div>
            <div class="role-dept">Competent Authority Land Acquisition (Revenue)</div>
            <span style="font-size: 0.7rem; background: #FEF3C7; color: #92400E; padding: 2px 8px; border-radius: 8px; font-weight: 600;">District Level</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Log In as CALA", key="btn_login_cala", width="stretch", type="primary"):
            quick_login("cala")

    with col3:
        st.markdown("""
        <div class="role-card">
            <div class="role-icon">📊</div>
            <div class="role-title">MoSPI Central Monitor</div>
            <div class="role-dept">Ministry of Statistics & Programme Implementation</div>
            <span style="font-size: 0.7rem; background: #E0E7FF; color: #3730A3; padding: 2px 8px; border-radius: 8px; font-weight: 600;">National Audit</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Log In as MoSPI", key="btn_login_mospi", width="stretch", type="primary"):
            quick_login("mospi")

    with col4:
        st.markdown("""
        <div class="role-card">
            <div class="role-icon">⭐</div>
            <div class="role-title">SIH Evaluation Jury</div>
            <div class="role-dept">Smart India Hackathon Grand Finale Jury</div>
            <span style="font-size: 0.7rem; background: #DCFCE7; color: #166534; padding: 2px 8px; border-radius: 8px; font-weight: 600;">VIP Evaluator</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Log In as SIH Jury", key="btn_login_jury", width="stretch", type="primary"):
            quick_login("jury")

with tab_form:
    st.markdown("#### Enter Official Email & Password")
    with st.form("credentials_login_form"):
        f_email = st.text_input("Official Gov Email / Username", placeholder="e.g. director@gatishakti.gov.in or cala@revenue.gov.in")
        f_pass = st.text_input("Password", type="password", placeholder="Enter official access token or password")
        remember = st.checkbox("Keep session active on this workstation", value=True)
        submit_btn = st.form_submit_button("Authenticate Officer 🛡️", width="stretch", type="primary")
        
        if submit_btn:
            if login(f_email, f_pass):
                st.success("✅ Authentication successful! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Invalid credentials. You can use 1-click test roles in the first tab or enter password `admin`.")

# Security & Compliance Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="background: #F1F5F9; border-radius: 12px; padding: 14px 20px; border: 1px solid #CBD5E1; font-size: 0.8rem; color: #475569; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
    <div>
        🔒 <strong>Gov-Standard Security:</strong> 256-Bit TLS End-to-End Encryption • Role-Based Access Control (RBAC)
    </div>
    <div>
        🏛️ <strong>Integrations:</strong> PM GatiShakti NMP • DILRMP Land Records • MoSPI Mega-Projects Database
    </div>
</div>
""", unsafe_allow_html=True)

