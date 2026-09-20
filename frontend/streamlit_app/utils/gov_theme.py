"""
gov_theme.py — BHOOMI AI Government Portal Theme
=================================================
Provides reusable theme components giving every page a government-portal look:
  - Navy header bar with Ashoka chakra strip
  - Saffron / White / Green tricolor accent strip
  - Status pill badges (complete, in_progress, delayed, not_started)
  - Standardised GOI-style footer

Usage (on each officer page):
    from utils.gov_theme import apply_gov_theme, render_gov_header, render_breadcrumb, status_pill, render_gov_footer

    st.set_page_config(...)
    apply_gov_theme()
    render_gov_header("Ministry of Road Transport & Highways")
    render_breadcrumb(["Home", "Project Details"])
    ...page content...
    render_gov_footer()
"""

import streamlit as st
from typing import Literal

# ─────────────────────────────────────────────
# NAV_ITEMS — horizontal navbar page list
# ─────────────────────────────────────────────

NAV_ITEMS = [
    {"label": "🏛️ Dashboard",    "slug": "Officer_Dashboard",   "url": "/Officer_Dashboard"},
    {"label": "📊 Projects",     "slug": "Project_Details",      "url": "/Project_Details"},
    {"label": "🏆 Risk Ranking", "slug": "Risk_Ranking",         "url": "/Risk_Ranking"},
    {"label": "🧠 SHAP AI",      "slug": "SHAP_Explanations",    "url": "/SHAP_Explanations"},
    {"label": "🗺️ GIS Map",      "slug": "GIS_Map",              "url": "/GIS_Map"},
    {"label": "🚨 Alerts",       "slug": "Alerts",               "url": "/Alerts"},
    {"label": "➕ Add Project",  "slug": "Add_Project",          "url": "/Add_Project"},
    {"label": "📜 DILRMP",       "slug": "DILRMP_Land_Records",  "url": "/DILRMP_Land_Records"},
]



# ─────────────────────────────────────────────
# render_role_selection_landing(logo_path, site_title, site_subtitle)
# ─────────────────────────────────────────────

def render_role_selection_landing(
    logo_path: str = "",
    site_title: str = "BHOOMI AI",
    site_subtitle: str = "Land Acquisition Delay Prediction & Risk Management System"
) -> None:
    """
    Renders a stylish role-selection landing hero & cards (Officer Login / Citizen Login).
    Only called on Home.py/app.py.
    """
    import base64
    import os

    logo_img_html = '<span style="font-size:3.2rem;">🌱</span>'
    if logo_path and os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(logo_path)[1].lstrip(".").lower()
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext
        logo_img_html = (
            f'<img src="data:image/{mime};base64,{logo_b64}" '
            f'style="height:76px; width:auto; object-fit:contain; border-radius:10px; background:rgba(255,255,255,0.12); padding:6px; border:1px solid rgba(255,255,255,0.2);">'
        )

    # Tricolor Strip & Hero Header Band
    st.markdown(f"""
<style>
/* Landing Page Specific Styling */
.landing-hero-band {{
    background: linear-gradient(135deg, #001A52 0%, #00256E 50%, #003087 100%);
    border-radius: 12px;
    padding: 32px 28px 24px 28px;
    color: #FFFFFF;
    text-align: center;
    box-shadow: 0 10px 25px -5px rgba(0, 48, 135, 0.25);
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}}
.landing-tricolor {{
    display: flex;
    height: 5px;
    width: 100%;
    margin-bottom: 20px;
    border-radius: 3px;
    overflow: hidden;
}}
.landing-tricolor .saffron {{ background: #FF9933; flex: 1; }}
.landing-tricolor .white   {{ background: #FFFFFF; flex: 1; }}
.landing-tricolor .green   {{ background: #138808; flex: 1; }}

.landing-title {{
    font-size: 2.3rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 10px 0 4px 0;
    color: #FFFFFF;
}}
.landing-subtitle {{
    font-size: 1.05rem;
    color: #93C5FD;
    font-weight: 500;
    max-width: 680px;
    margin: 0 auto;
    line-height: 1.4;
}}
.landing-trust {{
    font-size: 0.78rem;
    color: #BFDBFE;
    margin-top: 10px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    font-weight: 600;
    opacity: 0.85;
}}

/* Interactive Role Cards */
.role-select-card {{
    background: #FFFFFF;
    border: 1.5px solid #E2E8F0;
    border-radius: 8px;
    padding: 28px 24px 20px 24px;
    box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08), 0 4px 6px -2px rgba(15, 23, 42, 0.04);
    transition: all 0.2s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}
.role-select-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 20px 30px -10px rgba(0, 48, 135, 0.15), 0 8px 10px -4px rgba(0, 48, 135, 0.08);
}}
.role-card-officer:hover {{
    border-color: #003087;
}}
.role-card-citizen:hover {{
    border-color: #10B981;
}}

.icon-badge {{
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    margin: 0 auto 16px auto;
}}
.icon-badge-blue {{
    background: #DBEAFE;
    color: #1E40AF;
    border: 1.5px solid #BFDBFE;
}}
.icon-badge-green {{
    background: #DCFCE7;
    color: #166534;
    border: 1.5px solid #BBF7D0;
}}

.role-card-heading {{
    font-size: 1.35rem;
    font-weight: 800;
    color: #0F172A;
    text-align: center;
    margin-bottom: 8px;
}}
.role-card-desc {{
    font-size: 0.88rem;
    color: #475569;
    text-align: center;
    line-height: 1.45;
    margin-bottom: 18px;
    min-height: 48px;
}}

.feature-pill-list {{
    margin: 0 0 20px 0;
    padding: 0;
    list-style: none;
}}
.feature-pill-list li {{
    font-size: 0.82rem;
    color: #334155;
    padding: 6px 0;
    border-bottom: 1px solid #F1F5F9;
    display: flex;
    align-items: center;
    gap: 8px;
}}

/* Custom buttons styling */
div[data-testid="stButton"] > button.officer-btn {{
    background-color: #003087 !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 700 !important;
    border-radius: 6px !important;
    padding: 10px 16px !important;
    width: 100% !important;
}}
div[data-testid="stButton"] > button.citizen-btn {{
    background-color: #065F46 !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 700 !important;
    border-radius: 6px !important;
    padding: 10px 16px !important;
    width: 100% !important;
}}
</style>

<div class="landing-hero-band">
    <div class="landing-tricolor">
        <div class="saffron"></div>
        <div class="white"></div>
        <div class="green"></div>
    </div>
    <div style="display:flex; align-items:center; justify-content:center; gap:16px; margin-bottom:6px;">
        {logo_img_html}
        <div style="text-align:left;">
            <div class="landing-title">{site_title}</div>
            <div style="font-size:0.85rem; letter-spacing:1.5px; color:#4ADE80; font-weight:700;">
                LAND • DATA • BETTER TOMORROW
            </div>
        </div>
    </div>
    <div class="landing-subtitle">{site_subtitle}</div>
    <div class="landing-trust">PM GatiShakti • SIH26017 Prototype</div>
</div>
""", unsafe_allow_html=True)

    # Two Centered Columns for Cards
    _, col_off, col_cit, _ = st.columns([1, 4, 4, 1])

    with col_off:
        st.markdown("""
<div class="role-select-card role-card-officer">
    <div>
        <div class="icon-badge icon-badge-blue">🔐</div>
        <div class="role-card-heading">Officer Portal</div>
        <div class="role-card-desc">
            Role-based access for CALA, National Project Directors, MoSPI monitors, and SIH jury evaluation.
        </div>
        <ul class="feature-pill-list">
            <li><span>🤖</span> <strong>TreeSHAP AI:</strong> Delay cause attribution</li>
            <li><span>📊</span> <strong>Risk Ranking:</strong> Portfolio-wide delay prediction</li>
            <li><span>🗺️</span> <strong>GIS Corridor:</strong> Alignment risk mapping</li>
            <li><span>🚨</span> <strong>Smart Alerts:</strong> Section 24 lapsing risk warnings</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)
        if st.button("Go to Officer Login →", key="btn_landing_officer", type="primary", use_container_width=True):
            try:
                st.switch_page("pages/0_🔐_Officer_Login.py")
            except Exception:
                st.markdown('<meta http-equiv="refresh" content="0; url=/Officer_Login">', unsafe_allow_html=True)

    with col_cit:
        st.markdown("""
<div class="role-select-card role-card-citizen">
    <div>
        <div class="icon-badge icon-badge-green">🧑‍🌾</div>
        <div class="role-card-heading">Citizen Land Tracker</div>
        <div class="role-card-desc">
            Public parcel tracking for landowners and affected families under RFCTLARR Act, 2013.
        </div>
        <ul class="feature-pill-list">
            <li><span>📱</span> <strong>OTP Verification:</strong> Direct mobile/email access</li>
            <li><span>💰</span> <strong>Compensation Status:</strong> SLA tracking & payout</li>
            <li><span>⚖️</span> <strong>Statutory Rights:</strong> Section 24 & grievance filing</li>
            <li><span>📜</span> <strong>Bilingual Portal:</strong> English & हिन्दी support</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)
        if st.button("Go to Citizen Login →", key="btn_landing_citizen", type="secondary", use_container_width=True):
            try:
                st.switch_page("pages/9_🔑_Citizen_Login.py")
            except Exception:
                st.markdown('<meta http-equiv="refresh" content="0; url=/Citizen_Login">', unsafe_allow_html=True)



# ─────────────────────────────────────────────
# hide_default_sidebar_nav()
# ─────────────────────────────────────────────

def hide_default_sidebar_nav() -> None:
    """
    Hides Streamlit's auto-generated sidebar page list and collapses the sidebar
    so the top navbar is the sole navigation mechanism.
    """
    st.markdown("""
<style>
/* Hide Streamlit's auto sidebar page list */
[data-testid="stSidebarNav"] { display: none !important; }
/* Collapse sidebar entirely */
section[data-testid="stSidebar"] {
    display: none !important;
    min-width: 0 !important;
    width: 0 !important;
}
/* Hide sidebar toggle arrow */
[data-testid="collapsedControl"] { display: none !important; }
/* Expand main content to full width */
.main .block-container {
    max-width: 100% !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# render_top_navbar(current_slug, logo_path, ...)
# ─────────────────────────────────────────────

def render_top_navbar(
    current_slug: str = "Home",
    logo_path: str = "",
    site_title: str = "BHOOMI AI",
    site_subtitle: str = "Land Intelligence Platform"
) -> None:
    """
    Renders a full-width sticky top navbar with:
      - Logo + brand on the left
      - Horizontal nav links (active link highlighted with saffron underline)
      - Session badge on the right (officer name or citizen indicator)

    Args:
        current_slug: URL slug of the current page (e.g. 'Home', 'Project_Details').
        logo_path: Absolute path to the logo image file.
        site_title: System name beside the logo.
        site_subtitle: Tagline below the system name.
    """
    import base64
    import os

    # Build base64 logo
    logo_img_html = '<span style="font-size:2rem;">🌱</span>'
    if logo_path and os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(logo_path)[1].lstrip(".").lower()
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext
        logo_img_html = (
            f'<img src="data:image/{mime};base64,{logo_b64}" '
            f'style="height:52px; width:auto; object-fit:contain; border-radius:6px;">'
        )

    # Build nav links with preserved session query parameters
    officer_q = st.session_state.get("officer_id") or st.query_params.get("officer_session")
    citizen_q = st.session_state.get("citizen_identifier") or st.query_params.get("citizen_id")

    nav_links_html = ""
    for item in NAV_ITEMS:
        is_active = item["slug"] == current_slug
        active_style = (
            "background:rgba(255,255,255,0.22); font-weight:700; "
            "border-bottom:3px solid #FF9933;"
        ) if is_active else "font-weight:500;"

        url = item["url"]
        if officer_q and item["slug"] != "Citizen_Tracker":
            url = f"{url}?officer_session={officer_q}"
        elif citizen_q and item["slug"] == "Citizen_Tracker":
            url = f"{url}?citizen_session=1&citizen_id={citizen_q}"

        nav_links_html += (
            f'<a href="{url}" target="_self" style="'
            f'color:#FFFFFF; text-decoration:none; padding:8px 11px;'
            f'border-radius:6px 6px 0 0; font-size:0.80rem; white-space:nowrap;'
            f'display:inline-block; {active_style} transition:background 0.15s;">'
            f'{item["label"]}</a>'
        )


    # Session badge & Sign Out
    user = st.session_state.get("user")
    session_badge = ""
    if user:
        name_short = user.get("name", "").split()[0]
        role_short = user.get("role", "")[:22]
        session_badge = (
            f'<div style="display:flex;align-items:center;gap:8px;">'
            f'<span style="background:rgba(255,255,255,0.18);border:1px solid rgba(255,255,255,0.3);'
            f'padding:3px 10px;border-radius:20px;font-size:0.72rem;color:#D1FAE5;font-weight:600;white-space:nowrap;">'
            f'🟢 {name_short} · {role_short}</span>'
            f'<a href="/Officer_Login" target="_self" style="background:#EF4444;color:#FFFFFF;text-decoration:none;'
            f'padding:3px 9px;border-radius:12px;font-size:0.70rem;font-weight:700;white-space:nowrap;">Sign Out</a>'
            f'</div>'
        )
    elif st.session_state.get("citizen_authenticated"):
        cid = st.session_state.get("citizen_identifier", "")
        masked = cid[-4:] if cid else ""
        session_badge = (
            f'<div style="display:flex;align-items:center;gap:8px;">'
            f'<span style="background:rgba(255,255,255,0.18);border:1px solid rgba(255,255,255,0.3);'
            f'padding:3px 10px;border-radius:20px;font-size:0.72rem;color:#A7F3D0;font-weight:600;white-space:nowrap;">'
            f'🌾 Citizen ···{masked}</span>'
            f'<a href="/Citizen_Login" target="_self" style="background:#065F46;color:#FFFFFF;text-decoration:none;'
            f'padding:3px 9px;border-radius:12px;font-size:0.70rem;font-weight:700;white-space:nowrap;">Sign Out</a>'
            f'</div>'
        )


    st.markdown(f"""
<div style="background:linear-gradient(135deg,#003087 0%,#001A52 100%);
     padding:0 24px; box-shadow:0 4px 16px rgba(0,48,135,0.3);
     position:sticky; top:0; z-index:9999;">
  <div style="display:flex;align-items:center;justify-content:space-between;
       min-height:64px;flex-wrap:wrap;gap:8px;">
    <!-- Logo + Brand -->
    <div style="display:flex;align-items:center;gap:12px;flex-shrink:0;">
      {logo_img_html}
      <div>
        <div style="font-size:1.15rem;font-weight:800;color:#FFFFFF;
             letter-spacing:-0.3px;line-height:1.1;">{site_title}</div>
        <div style="font-size:0.68rem;color:#93C5FD;font-weight:500;
             letter-spacing:0.5px;">{site_subtitle}</div>
      </div>
    </div>
    <!-- Nav Links -->
    <div style="display:flex;align-items:flex-end;gap:2px;flex-wrap:wrap;">
      {nav_links_html}
    </div>
    <!-- Session Badge -->
    <div style="flex-shrink:0;">{session_badge}</div>
  </div>
  <!-- Tricolor strip -->
  <div style="display:flex;height:4px;width:100%;">
    <div style="background:#FF9933;flex:1;"></div>
    <div style="background:#FFFFFF;flex:1;"></div>
    <div style="background:#138808;flex:1;"></div>
  </div>
</div>
<div style="height:12px;"></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# render_citizen_navbar(logo_path, site_title, site_subtitle)
# ─────────────────────────────────────────────

def render_citizen_navbar(
    logo_path: str = "",
    site_title: str = "BHOOMI AI",
    site_subtitle: str = "Citizen Land Acquisition & Compensation Portal • नागरिक भूमि पोर्टल"
) -> None:
    """
    Renders a dedicated, emerald-green citizen navbar with zero officer information,
    zero officer navigation links, and an isolated citizen session status badge + sign out button.
    """
    import base64
    import os

    logo_img_html = '<span style="font-size:2rem;">🌱</span>'
    if logo_path and os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(logo_path)[1].lstrip(".").lower()
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext
        logo_img_html = (
            f'<img src="data:image/{mime};base64,{logo_b64}" '
            f'style="height:50px; width:auto; object-fit:contain; border-radius:6px; background:rgba(255,255,255,0.12); padding:4px;">'
        )

    cid = st.session_state.get("citizen_identifier", "")
    display_id = f"🌾 Citizen: {cid}" if cid else "🌾 Verified Citizen"

    st.markdown(f"""
<div style="background:linear-gradient(135deg,#064E3B 0%,#065F46 55%,#047857 100%);
     padding:0 24px; box-shadow:0 4px 16px rgba(6,78,59,0.35);
     position:sticky; top:0; z-index:9999;">
  <div style="display:flex;align-items:center;justify-content:space-between;
       min-height:64px;flex-wrap:wrap;gap:8px;">
    <!-- Logo + Brand -->
    <div style="display:flex;align-items:center;gap:12px;flex-shrink:0;">
      {logo_img_html}
      <div>
        <div style="font-size:1.18rem;font-weight:800;color:#FFFFFF;
             letter-spacing:-0.3px;line-height:1.1;">{site_title} <span style="font-size:0.82rem;color:#A7F3D0;font-weight:600;">• नागरिक भूमि ट्रैकर</span></div>
        <div style="font-size:0.70rem;color:#D1FAE5;font-weight:500;
             letter-spacing:0.4px;">{site_subtitle}</div>
      </div>
    </div>
    <!-- Citizen Status & Action -->
    <div style="display:flex;align-items:center;gap:10px;flex-shrink:0;">
      <span style="background:rgba(255,255,255,0.18);border:1px solid rgba(255,255,255,0.3);
            padding:4px 12px;border-radius:20px;font-size:0.75rem;color:#FFFFFF;font-weight:600;white-space:nowrap;">
        {display_id}
      </span>
      <a href="/Citizen_Login" target="_self" style="background:#DC2626;color:#FFFFFF;text-decoration:none;
            padding:4px 12px;border-radius:12px;font-size:0.72rem;font-weight:700;white-space:nowrap;box-shadow:0 2px 6px rgba(0,0,0,0.2);">
        🚪 Sign Out
      </a>
    </div>
  </div>
  <!-- Tricolor strip -->
  <div style="display:flex;height:4px;width:100%;">
    <div style="background:#FF9933;flex:1;"></div>
    <div style="background:#FFFFFF;flex:1;"></div>
    <div style="background:#138808;flex:1;"></div>
  </div>
</div>
<div style="height:12px;"></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# render_split_login_header(logo_path, title, subtitle)
# ─────────────────────────────────────────────

def render_split_login_header(
    logo_path: str = "",
    title: str = "Login",
    subtitle: str = "Secure portal access"
) -> None:
    """
    Renders a navy split-layout login header: logo frosted-card on the left,
    title + subtitle text on the right. Used on login pages instead of
    render_top_navbar().

    Args:
        logo_path: Absolute path to the logo image file.
        title: Login page title (e.g. 'Officer Login').
        subtitle: Short description below the title.
    """
    import base64
    import os

    logo_html = '<span style="font-size:3.5rem;">🌱</span>'
    if logo_path and os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(logo_path)[1].lstrip(".").lower()
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext
        logo_html = (
            f'<img src="data:image/{mime};base64,{logo_b64}" '
            f'style="height:80px;width:auto;object-fit:contain;border-radius:8px;">'
        )

    st.markdown(f"""
<div style="background:linear-gradient(135deg,#003087 0%,#001A52 100%);
     padding:24px 28px 0 28px;
     box-shadow:0 4px 16px rgba(0,48,135,0.3);">
  <div style="display:flex;align-items:center;gap:20px;padding-bottom:20px;">
    <div style="flex-shrink:0;background:rgba(255,255,255,0.12);
         border-radius:12px;padding:10px;border:1px solid rgba(255,255,255,0.2);">
      {logo_html}
    </div>
    <div>
      <div style="font-size:1.8rem;font-weight:800;color:#FFFFFF;
           letter-spacing:-0.5px;line-height:1.1;">{title}</div>
      <div style="font-size:0.9rem;color:#93C5FD;margin-top:4px;">{subtitle}</div>
      <div style="font-size:0.72rem;color:#BFDBFE;margin-top:4px;font-style:italic;">
        BHOOMI AI • PM GatiShakti National Master Plan • SIH26017
      </div>
    </div>
  </div>
  <!-- Tricolor strip -->
  <div style="display:flex;height:5px;width:100%;">
    <div style="background:#FF9933;flex:1;"></div>
    <div style="background:#FFFFFF;flex:1;"></div>
    <div style="background:#138808;flex:1;"></div>
  </div>
</div>
<div style="height:20px;"></div>
""", unsafe_allow_html=True)



# ─────────────────────────────────────────────
# 1. apply_gov_theme()
# Injects GOI-standard CSS: navy palette, typography, card styles, tricolor strip.
# ─────────────────────────────────────────────

def apply_gov_theme() -> None:
    """
    Injects the GOI Government Portal CSS into the current Streamlit page.
    Must be called immediately after st.set_page_config().
    """
    st.markdown("""
<style>
/* ── Google Fonts ─────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* ── Base Reset ───────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Noto Sans', 'Plus Jakarta Sans', sans-serif !important;
}

/* ── GOI Tricolor Strip (top accent) ─────────────────────────────────────── */
.gov-tricolor-strip {
    display: flex;
    height: 6px;
    width: 100%;
    border-radius: 0 0 4px 4px;
    overflow: hidden;
    margin-bottom: 0;
}
.gov-tricolor-strip .saffron { background: #FF9933; flex: 1; }
.gov-tricolor-strip .white   { background: #FFFFFF; flex: 1; }
.gov-tricolor-strip .green   { background: #138808; flex: 1; }

/* ── Navy GOI Header ─────────────────────────────────────────────────────── */
.gov-header {
    background: linear-gradient(135deg, #003087 0%, #00256E 60%, #001A52 100%);
    padding: 18px 28px 14px 28px;
    border-radius: 0 0 0 0;
    color: #FFFFFF;
    margin-bottom: 0;
    box-shadow: 0 4px 12px rgba(0, 48, 135, 0.25);
}
.gov-header-inner {
    display: flex;
    align-items: center;
    gap: 16px;
}
.gov-header-emblem {
    font-size: 2.2rem;
    line-height: 1;
    flex-shrink: 0;
}
.gov-header-text {
    flex: 1;
}
.gov-header-system-name {
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: -0.3px;
    color: #FFFFFF;
    margin: 0;
    line-height: 1.2;
}
.gov-header-ministry {
    font-size: 0.82rem;
    font-weight: 500;
    color: #93C5FD;
    margin-top: 3px;
    letter-spacing: 0.4px;
}
.gov-header-tagline {
    font-size: 0.72rem;
    color: #BFDBFE;
    margin-top: 2px;
    font-style: italic;
}
.gov-header-badge-row {
    display: flex;
    gap: 8px;
    margin-top: 10px;
    flex-wrap: wrap;
}
.gov-badge {
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.25);
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    color: #E0F2FE;
    backdrop-filter: blur(4px);
}

/* ── Breadcrumb Nav ──────────────────────────────────────────────────────── */
.gov-breadcrumb {
    background: #F0F4FF;
    border-bottom: 1px solid #CBD5E1;
    padding: 8px 28px;
    font-size: 0.8rem;
    color: #475569;
    display: flex;
    align-items: center;
    gap: 4px;
    flex-wrap: wrap;
}
.gov-breadcrumb a, .gov-breadcrumb .bc-item {
    color: #003087;
    text-decoration: none;
    font-weight: 600;
}
.gov-breadcrumb .bc-sep {
    color: #94A3B8;
    font-size: 0.72rem;
    margin: 0 2px;
}
.gov-breadcrumb .bc-current {
    color: #64748B;
    font-weight: 500;
}

/* ── Status Pills ────────────────────────────────────────────────────────── */
.status-pill {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.3px;
    line-height: 1.6;
}
.status-complete    { background: #D1FAE5; color: #065F46; border: 1px solid #A7F3D0; }
.status-in_progress { background: #DBEAFE; color: #1E40AF; border: 1px solid #BFDBFE; }
.status-delayed     { background: #FEE2E2; color: #991B1B; border: 1px solid #FECACA; }
.status-not_started { background: #F1F5F9; color: #475569; border: 1px solid #CBD5E1; }

/* ── GOI Footer ──────────────────────────────────────────────────────────── */
.gov-footer {
    margin-top: 40px;
    background: #003087;
    border-radius: 8px;
    padding: 16px 24px;
    color: #BFDBFE;
    font-size: 0.78rem;
}
.gov-footer-inner {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 12px;
}
.gov-footer-left {
    flex: 1;
    min-width: 220px;
}
.gov-footer-right {
    text-align: right;
    flex: 1;
    min-width: 180px;
}
.gov-footer-logo-text {
    font-size: 1rem;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.2px;
}
.gov-footer-subtitle {
    font-size: 0.7rem;
    color: #93C5FD;
    margin-top: 2px;
}
.gov-footer-links {
    margin-top: 6px;
    display: flex;
    gap: 14px;
    flex-wrap: wrap;
}
.gov-footer-links a {
    color: #BFDBFE;
    text-decoration: underline;
    font-size: 0.72rem;
}
.gov-footer-disclaimer {
    font-size: 0.68rem;
    color: #93C5FD;
    margin-top: 10px;
    padding-top: 8px;
    border-top: 1px solid rgba(255, 255, 255, 0.15);
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 2. render_gov_header(ministry, lang_default)
# ─────────────────────────────────────────────

def render_gov_header(
    ministry: str = "Ministry of Road Transport & Highways (MoRTH) | DPIIT | MoSPI",
    lang_default: str = "EN"
) -> None:
    """
    Renders the GOI navy header bar with Ashoka chakra emblem,
    system name, ministry label, and a tricolor accent strip below.

    Args:
        ministry: Ministry / Department string displayed under the system name.
        lang_default: Language label shown in the header badge (e.g. "EN" or "HI").
    """
    st.markdown(f"""
<div class="gov-header">
    <div class="gov-header-inner">
        <div class="gov-header-emblem">🏛️</div>
        <div class="gov-header-text">
            <div class="gov-header-system-name">🌱 BHOOMI AI — Land Intelligence Platform</div>
            <div class="gov-header-ministry">{ministry}</div>
            <div class="gov-header-tagline">PM GatiShakti National Master Plan • SIH26017 Prototype</div>
            <div class="gov-header-badge-row">
                <span class="gov-badge">🤖 TreeSHAP Explainable AI</span>
                <span class="gov-badge">📊 RFCTLARR Act, 2013</span>
                <span class="gov-badge">🌐 DILRMP Land Records</span>
                <span class="gov-badge">🔐 Role-Based Access</span>
                <span class="gov-badge">🗣️ {lang_default}</span>
            </div>
        </div>
    </div>
</div>
<div class="gov-tricolor-strip">
    <div class="saffron"></div>
    <div class="white"></div>
    <div class="green"></div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 3. render_breadcrumb(path: list[str])
# ─────────────────────────────────────────────

def render_breadcrumb(path: list[str]) -> None:
    """
    Renders a GOI-style breadcrumb navigation bar.

    Args:
        path: List of breadcrumb labels, e.g. ["Home", "Project Details"].
              The last item is rendered as the current (non-linked) page.
    """
    if not path:
        return

    crumbs_html = ""
    for i, crumb in enumerate(path):
        is_last = (i == len(path) - 1)
        if is_last:
            crumbs_html += f'<span class="bc-current">{crumb}</span>'
        else:
            crumbs_html += f'<span class="bc-item">🏠 {crumb}</span>' if i == 0 else f'<span class="bc-item">{crumb}</span>'
            crumbs_html += '<span class="bc-sep">›</span>'

    st.markdown(f"""
<div class="gov-breadcrumb">
    {crumbs_html}
</div>
<div style="margin-bottom: 16px;"></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 4. status_pill(label, status)
# ─────────────────────────────────────────────

StatusType = Literal["complete", "in_progress", "delayed", "not_started"]

def status_pill(label: str, status: StatusType) -> str:
    """
    Returns an HTML string for a government-portal-styled status pill badge.
    Render it with st.markdown(status_pill(...), unsafe_allow_html=True).

    Args:
        label: Display text for the pill (e.g. "Completed", "Pending", "Delayed").
        status: One of "complete" | "in_progress" | "delayed" | "not_started".

    Returns:
        HTML string: <span class="status-pill status-{status}">{label}</span>
    """
    css_class = f"status-{status}"
    icons = {
        "complete": "✅",
        "in_progress": "🔄",
        "delayed": "🔴",
        "not_started": "⬜"
    }
    icon = icons.get(status, "")
    return f'<span class="status-pill {css_class}">{icon} {label}</span>'


# ─────────────────────────────────────────────
# 5. render_gov_footer()
# ─────────────────────────────────────────────

def render_gov_footer() -> None:
    """
    Renders the standardised GOI-style footer at the bottom of a page.
    Shows platform identity, statutory references, and boilerplate disclaimer.
    """
    from datetime import datetime
    current_year = datetime.now().year

    st.markdown(f"""
<div class="gov-footer">
    <div class="gov-footer-inner">
        <div class="gov-footer-left">
            <div class="gov-footer-logo-text">🌱 BHOOMI AI</div>
            <div class="gov-footer-subtitle">
                Land Acquisition Delay Prediction &amp; Risk Management System<br>
                Smart India Hackathon SIH26017 | PM GatiShakti National Master Plan
            </div>
            <div class="gov-footer-links">
                <a href="https://pib.gov.in" target="_blank">PIB India</a>
                <a href="https://dilrmp.gov.in" target="_blank">DILRMP Portal</a>
                <a href="https://mospi.gov.in" target="_blank">MoSPI</a>
                <a href="https://morth.nic.in" target="_blank">MoRTH</a>
                <a href="https://gatishakti.gov.in" target="_blank">PM GatiShakti</a>
            </div>
        </div>
        <div class="gov-footer-right">
            <div style="font-size: 0.72rem; color: #93C5FD;">
                🏛️ Ministry of Road Transport &amp; Highways<br>
                🧠 Powered by XGBoost + TreeSHAP<br>
                📊 MoSPI Mega Infrastructure Dataset<br>
                📜 RFCTLARR Act, 2013 Compliant<br>
                🔐 Role-Based Access Control (RBAC)
            </div>
        </div>
    </div>
    <div class="gov-footer-disclaimer">
        ⚠️ This is a Smart India Hackathon prototype (SIH26017). Data used is for demonstration purposes only.
        Not an official Government of India publication. © {current_year} BHOOMI AI Team.
        Governed by IT Act, 2000 | Data Protection Standards.
    </div>
</div>
""", unsafe_allow_html=True)

