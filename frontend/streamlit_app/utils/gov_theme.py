"""
gov_theme.py — BHOOMI AI Government Portal Theme
=================================================
Provides reusable theme components giving every page a government-portal look:
  - Navy/Emerald header bar with Ashoka chakra strip
  - Saffron / White / Green tricolor accent strip
  - Status pill badges (complete, in_progress, delayed, not_started)
  - Standardised GOI-style footer
  - English & Hindi internationalization support
"""

import streamlit as st
from typing import Literal

try:
    from utils.i18n import t, get_current_lang, set_lang
except ImportError:
    from frontend.streamlit_app.utils.i18n import t, get_current_lang, set_lang


# ─────────────────────────────────────────────
# Dynamic NAV_ITEMS
# ─────────────────────────────────────────────

def get_nav_items():
    """Returns horizontal navbar items with dynamic bilingual labels."""
    return [
        {"label": t("nav_dashboard", "🏛️ Dashboard"), "slug": "Officer_Dashboard", "url": "/Officer_Dashboard"},
        {"label": t("nav_projects", "📊 Projects"), "slug": "Project_Details", "url": "/Project_Details"},
        {"label": t("nav_risk", "🏆 Risk Ranking"), "slug": "Risk_Ranking", "url": "/Risk_Ranking"},
        {"label": t("nav_capital", "💰 Capital Allocation"), "slug": "Capital_Allocation", "url": "/Capital_Allocation"},
        {"label": t("nav_shap", "🧠 SHAP AI"), "slug": "SHAP_Explanations", "url": "/SHAP_Explanations"},
        {"label": t("nav_gis", "🗺️ GIS Map"), "slug": "GIS_Map", "url": "/GIS_Map"},
        {"label": t("nav_alerts", "🚨 Alerts"), "slug": "Alerts", "url": "/Alerts"},
        {"label": t("nav_add", "➕ Add Project"), "slug": "Add_Project", "url": "/Add_Project"},
        {"label": t("nav_dilrmp", "📜 DILRMP"), "slug": "DILRMP_Land_Records", "url": "/DILRMP_Land_Records"},
    ]

# Default export
NAV_ITEMS = get_nav_items()


# ─────────────────────────────────────────────
# render_role_selection_landing(logo_path, site_title, site_subtitle)
# ─────────────────────────────────────────────

def render_role_selection_landing(
    logo_path: str = "",
    site_title: str = "",
    site_subtitle: str = ""
) -> None:
    """
    Renders the clean role-selection landing hero & cards (Officer Login / Citizen Login)
    with bilingual English / Hindi support and embedded language switch toggle.
    """
    import base64
    import os

    current_lang = get_current_lang()
    title = site_title if site_title else t("site_title", "BHOOMI AI")
    subtitle = site_subtitle if site_subtitle else t("site_subtitle", "Land Acquisition Delay Prediction & Risk Management System")
    tagline = t("hero_tagline", "LAND • DATA • BETTER TOMORROW")
    trust = t("hero_trust", "PM GATISHAKTI • SIH26017 PROTOTYPE")

    logo_img_html = '<span style="font-size:3.2rem;">🌱</span>'
    if logo_path and os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(logo_path)[1].lstrip(".").lower()
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext
        logo_img_html = f'<img src="data:image/{mime};base64,{logo_b64}" style="height:64px; width:auto; object-fit:contain; border-radius:8px; background:rgba(255,255,255,0.12); padding:4px; border:1px solid rgba(255,255,255,0.2);">'

    en_active = "background:rgba(255,255,255,0.3); color:#FFFFFF; font-weight:800;" if current_lang == "en" else "background:rgba(255,255,255,0.1); color:#D1FAE5; font-weight:500;"
    hi_active = "background:rgba(255,255,255,0.3); color:#FFFFFF; font-weight:800;" if current_lang == "hi" else "background:rgba(255,255,255,0.1); color:#D1FAE5; font-weight:500;"

    html = f"""<style>
.landing-hero-band {{
background: linear-gradient(135deg, #064E3B 0%, #065F46 50%, #047857 100%);
border-radius: 12px;
padding: 24px 32px 20px 32px;
color: #FFFFFF;
box-shadow: 0 10px 25px -5px rgba(6, 78, 59, 0.25);
margin-top: 4px;
margin-bottom: 24px;
text-align: center;
position: relative;
}}
.landing-tricolor {{
display: flex;
height: 5px;
width: 100%;
margin-bottom: 14px;
border-radius: 3px;
overflow: hidden;
}}
.landing-tricolor .saffron {{ background: #FF9933; flex: 1; }}
.landing-tricolor .white {{ background: #FFFFFF; flex: 1; }}
.landing-tricolor .green {{ background: #138808; flex: 1; }}
.landing-lang-bar {{
display: flex;
justify-content: flex-end;
gap: 8px;
margin-bottom: 10px;
}}
.lang-toggle-btn {{
text-decoration: none !important;
padding: 4px 14px;
border-radius: 20px;
font-size: 0.78rem;
border: 1px solid rgba(255, 255, 255, 0.35);
transition: all 0.15s ease;
display: inline-flex;
align-items: center;
gap: 4px;
}}
.lang-toggle-btn:hover {{
background: rgba(255, 255, 255, 0.25) !important;
color: #FFFFFF !important;
}}
.landing-title {{
font-size: 2.2rem;
font-weight: 800;
letter-spacing: -0.5px;
margin: 6px 0 2px 0;
color: #FFFFFF;
}}
.landing-tagline {{
font-size: 0.8rem;
color: #6EE7B7;
font-weight: 700;
letter-spacing: 1.5px;
text-transform: uppercase;
margin-bottom: 6px;
}}
.landing-subtitle {{
font-size: 1.02rem;
color: #D1FAE5;
font-weight: 500;
line-height: 1.4;
max-width: 800px;
margin: 0 auto 8px auto;
}}
.landing-trust {{
font-size: 0.72rem;
color: #A7F3D0;
letter-spacing: 0.5px;
text-transform: uppercase;
font-weight: 600;
opacity: 0.9;
}}
.cards-container {{
display: grid;
grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
gap: 24px;
max-width: 1000px;
margin: 0 auto;
}}
.role-select-card {{
background: #FFFFFF;
border: 1.5px solid #E2E8F0;
border-radius: 14px;
padding: 26px 24px;
box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08), 0 4px 6px -2px rgba(15, 23, 42, 0.04);
transition: all 0.2s ease;
display: flex;
flex-direction: column;
justify-content: space-between;
height: 100%;
}}
.role-select-card:hover {{
transform: translateY(-4px);
box-shadow: 0 20px 30px -10px rgba(6, 95, 70, 0.15), 0 8px 10px -4px rgba(6, 95, 70, 0.08);
}}
.role-card-officer:hover {{ border-color: #059669; }}
.role-card-citizen:hover {{ border-color: #10B981; }}
.icon-badge {{
width: 60px;
height: 60px;
border-radius: 50%;
display: flex;
align-items: center;
justify-content: center;
font-size: 1.9rem;
margin: 0 auto 14px auto;
background: #DCFCE7;
color: #065F46;
border: 1.5px solid #A7F3D0;
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
margin-bottom: 16px;
min-height: 48px;
}}
.feature-pill-list {{
margin: 0 0 22px 0;
padding: 0;
list-style: none;
}}
.feature-pill-list li {{
font-size: 0.84rem;
color: #334155;
padding: 7px 0;
border-bottom: 1px solid #F1F5F9;
display: flex;
align-items: center;
gap: 8px;
}}
.portal-action-btn {{
display: block;
width: 100%;
text-align: center;
background: linear-gradient(135deg, #064E3B 0%, #065F46 100%);
color: #FFFFFF !important;
padding: 12px 20px;
border-radius: 8px;
font-weight: 700;
font-size: 0.95rem;
text-decoration: none !important;
transition: all 0.15s ease;
box-shadow: 0 4px 10px rgba(6, 78, 59, 0.2);
}}
.portal-action-btn:hover {{
background: linear-gradient(135deg, #047857 0%, #059669 100%);
box-shadow: 0 6px 14px rgba(6, 78, 59, 0.3);
color: #FFFFFF !important;
transform: translateY(-1px);
}}
.portal-action-btn-citizen {{
background: linear-gradient(135deg, #047857 0%, #059669 100%);
}}
.portal-action-btn-citizen:hover {{
background: linear-gradient(135deg, #065F46 0%, #047857 100%);
}}
</style>
<div class="landing-hero-band">
<div class="landing-lang-bar">
<a href="?lang=en" target="_self" class="lang-toggle-btn" style="{en_active}">🇬🇧 English</a>
<a href="?lang=hi" target="_self" class="lang-toggle-btn" style="{hi_active}">🇮🇳 हिन्दी</a>
</div>
<div class="landing-tricolor">
<div class="saffron"></div>
<div class="white"></div>
<div class="green"></div>
</div>
<div style="display:flex; justify-content:center; align-items:center; margin-bottom:8px;">
{logo_img_html}
</div>
<div class="landing-title">{title}</div>
<div class="landing-tagline">{tagline}</div>
<div class="landing-subtitle">{subtitle}</div>
<div class="landing-trust">{trust}</div>
</div>
<div class="cards-container">
<div class="role-select-card role-card-officer">
<div>
<div class="icon-badge">🔐</div>
<div class="role-card-heading">{t("officer_card_title", "Officer Portal")}</div>
<div class="role-card-desc">{t("officer_card_desc", "Role-based access for CALA, National Project Directors, MoSPI monitors, and SIH jury evaluation.")}</div>
<ul class="feature-pill-list">
<li><span>🤖</span> <strong>TreeSHAP AI:</strong> {t("feat_shap", "Delay cause attribution")}</li>
<li><span>📊</span> <strong>Risk Ranking:</strong> {t("feat_risk", "Portfolio-wide delay prediction")}</li>
<li><span>🗺️</span> <strong>GIS Corridor:</strong> {t("feat_gis", "Alignment risk mapping")}</li>
<li><span>🚨</span> <strong>Smart Alerts:</strong> {t("feat_alerts", "Section 24 lapsing risk warnings")}</li>
</ul>
</div>
<a href="/Officer_Login" target="_self" class="portal-action-btn">{t("officer_btn", "🔐 Go to Officer Login →")}</a>
</div>
<div class="role-select-card role-card-citizen">
<div>
<div class="icon-badge">🧑‍🌾</div>
<div class="role-card-heading">{t("citizen_card_title", "Citizen Land Tracker")}</div>
<div class="role-card-desc">{t("citizen_card_desc", "Public parcel tracking for landowners and affected families under RFCTLARR Act, 2013.")}</div>
<ul class="feature-pill-list">
<li><span>📱</span> <strong>OTP Verification:</strong> {t("feat_otp", "Direct mobile/email access")}</li>
<li><span>💰</span> <strong>Compensation Status:</strong> {t("feat_comp", "SLA tracking & payout")}</li>
<li><span>⚖️</span> <strong>Statutory Rights:</strong> {t("feat_rights", "Section 24 & grievance filing")}</li>
<li><span>📜</span> <strong>Land Records:</strong> {t("feat_records", "DILRMP ownership verification")}</li>
</ul>
</div>
<a href="/Citizen_Login" target="_self" class="portal-action-btn portal-action-btn-citizen">{t("citizen_btn", "🧑‍🌾 Go to Citizen Login →")}</a>
</div>
</div>"""
    st.markdown(html, unsafe_allow_html=True)


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
header[data-testid="stHeader"] {
display: none !important;
}
[data-testid="stSidebarNav"] { display: none !important; }
section[data-testid="stSidebar"] {
display: none !important;
min-width: 0 !important;
width: 0 !important;
}
[data-testid="collapsedControl"] { display: none !important; }
.main .block-container {
max-width: 100% !important;
padding-top: 1.5rem !important;
padding-bottom: 2rem !important;
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
    site_title: str = "",
    site_subtitle: str = ""
) -> None:
    """
    Renders a full-width sticky top navbar with brand, bilingual navigation items,
    active state highlight, officer session badge, language switcher, and Sign Out button.
    """
    import base64
    import os

    current_lang = get_current_lang()
    title = site_title if site_title else t("site_title", "BHOOMI AI")
    subtitle = site_subtitle if site_subtitle else t("site_subtitle", "Land Intelligence Platform")
    sign_out_label = t("sign_out", "🚪 Sign Out")

    logo_img_html = '<span style="font-size:1.8rem;">🌱</span>'
    if logo_path and os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(logo_path)[1].lstrip(".").lower()
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext
        logo_img_html = f'<img src="data:image/{mime};base64,{logo_b64}" style="height:44px; width:auto; object-fit:contain; border-radius:6px; background:rgba(255,255,255,0.12); padding:2px;">'

    nav_links_html = ""
    for item in get_nav_items():
        is_active = item["slug"] == current_slug
        active_style = "background:rgba(255,255,255,0.22); font-weight:700; border-bottom:3px solid #FF9933; color:#FFFFFF;" if is_active else "color:#E2E8F0; font-weight:500;"
        nav_links_html += f'<a href="{item["url"]}" target="_self" style="text-decoration:none; padding:8px 11px; border-radius:6px 6px 0 0; font-size:0.80rem; white-space:nowrap; display:inline-block; {active_style} transition: all 0.15s ease;">{item["label"]}</a>'

    user = st.session_state.get("user")
    session_badge_html = ""
    if user:
        name_short = user.get("name", "").split()[0]
        role_short = user.get("role", "")[:18]
        session_badge_html = f'<span style="background:rgba(255,255,255,0.18); border:1px solid rgba(255,255,255,0.3); padding:4px 10px; border-radius:20px; font-size:0.72rem; color:#D1FAE5; font-weight:600; white-space:nowrap;">🟢 {name_short} · {role_short}</span>'
    elif st.session_state.get("citizen_authenticated"):
        cid = st.session_state.get("citizen_identifier", "")
        masked = cid[-4:] if cid else ""
        session_badge_html = f'<span style="background:rgba(255,255,255,0.18); border:1px solid rgba(255,255,255,0.3); padding:4px 10px; border-radius:20px; font-size:0.72rem; color:#A7F3D0; font-weight:600; white-space:nowrap;">🌾 {masked}</span>'

    en_style = "background:rgba(255,255,255,0.28); color:#FFFFFF; font-weight:700;" if current_lang == "en" else "color:#D1FAE5; font-weight:500;"
    hi_style = "background:rgba(255,255,255,0.28); color:#FFFFFF; font-weight:700;" if current_lang == "hi" else "color:#D1FAE5; font-weight:500;"

    lang_toggle_html = f"""<div style="display:flex; align-items:center; background:rgba(0,0,0,0.2); border-radius:20px; padding:2px 4px; gap:2px; border:1px solid rgba(255,255,255,0.25);">
<a href="?lang=en" target="_self" style="text-decoration:none; padding:2px 7px; border-radius:12px; font-size:0.70rem; {en_style}">EN</a>
<a href="?lang=hi" target="_self" style="text-decoration:none; padding:2px 7px; border-radius:12px; font-size:0.70rem; {hi_style}">हिन्दी</a>
</div>"""

    navbar_html = f"""<div style="background:linear-gradient(135deg,#064E3B 0%,#065F46 50%,#047857 100%); padding:0 20px; box-shadow:0 4px 16px rgba(6,78,59,0.3); margin-bottom:12px; border-radius:0 0 4px 4px;">
<div style="display:flex; align-items:center; justify-content:space-between; min-height:58px; flex-wrap:wrap; gap:8px;">
<div style="display:flex; align-items:center; gap:10px; flex-shrink:0;">
{logo_img_html}
<div>
<div style="font-size:1.1rem; font-weight:800; color:#FFFFFF; letter-spacing:-0.3px; line-height:1.1;">{title}</div>
<div style="font-size:0.65rem; color:#A7F3D0; font-weight:500; letter-spacing:0.3px;">{subtitle}</div>
</div>
</div>
<div style="display:flex; align-items:flex-end; gap:2px; flex-wrap:wrap;">
{nav_links_html}
</div>
<div style="display:flex; align-items:center; gap:8px; flex-shrink:0;">
{lang_toggle_html}
{session_badge_html}
<a href="/Officer_Login" target="_self" style="background:#EF4444; color:#FFFFFF; padding:4px 10px; border-radius:14px; font-size:0.72rem; font-weight:700; text-decoration:none; display:inline-block; transition: background 0.15s ease;">{sign_out_label}</a>
</div>
</div>
<div style="display:flex; height:4px; width:100%;">
<div style="background:#FF9933; flex:1;"></div>
<div style="background:#FFFFFF; flex:1;"></div>
<div style="background:#138808; flex:1;"></div>
</div>
</div>"""
    st.markdown(navbar_html, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# render_citizen_navbar(logo_path, site_title, site_subtitle)
# ─────────────────────────────────────────────

def render_citizen_navbar(
    logo_path: str = "",
    site_title: str = "",
    site_subtitle: str = ""
) -> None:
    """
    Renders a dedicated, emerald-green citizen navbar with bilingual language toggle
    and citizen session status badge + sign out button.
    """
    import base64
    import os

    current_lang = get_current_lang()
    title = site_title if site_title else t("site_title", "BHOOMI AI")
    subtitle = site_subtitle if site_subtitle else t("citizen_card_title", "Citizen Land Acquisition Tracker")
    sign_out_label = t("sign_out", "🚪 Sign Out")

    logo_img_html = '<span style="font-size:1.8rem;">🌱</span>'
    if logo_path and os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(logo_path)[1].lstrip(".").lower()
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext
        logo_img_html = f'<img src="data:image/{mime};base64,{logo_b64}" style="height:44px; width:auto; object-fit:contain; border-radius:6px; background:rgba(255,255,255,0.12); padding:2px;">'

    cid = st.session_state.get("citizen_identifier", "")
    display_id = f"🌾 {cid}" if cid else t("welcome_citizen", "🌾 Welcome Citizen")

    en_style = "background:rgba(255,255,255,0.28); color:#FFFFFF; font-weight:700;" if current_lang == "en" else "color:#D1FAE5; font-weight:500;"
    hi_style = "background:rgba(255,255,255,0.28); color:#FFFFFF; font-weight:700;" if current_lang == "hi" else "color:#D1FAE5; font-weight:500;"

    lang_toggle_html = f"""<div style="display:flex; align-items:center; background:rgba(0,0,0,0.2); border-radius:20px; padding:2px 4px; gap:2px; border:1px solid rgba(255,255,255,0.25);">
<a href="?lang=en" target="_self" style="text-decoration:none; padding:2px 7px; border-radius:12px; font-size:0.70rem; {en_style}">EN</a>
<a href="?lang=hi" target="_self" style="text-decoration:none; padding:2px 7px; border-radius:12px; font-size:0.70rem; {hi_style}">हिन्दी</a>
</div>"""

    cit_nav_html = f"""<div style="background:linear-gradient(135deg,#064E3B 0%,#065F46 50%,#047857 100%); padding:0 20px; box-shadow:0 4px 16px rgba(6,78,59,0.3); margin-bottom:12px; border-radius:0 0 4px 4px;">
<div style="display:flex; align-items:center; justify-content:space-between; min-height:58px; flex-wrap:wrap; gap:8px;">
<div style="display:flex; align-items:center; gap:10px; flex-shrink:0;">
{logo_img_html}
<div>
<div style="font-size:1.1rem; font-weight:800; color:#FFFFFF; letter-spacing:-0.3px; line-height:1.1;">{title}</div>
<div style="font-size:0.65rem; color:#A7F3D0; font-weight:500; letter-spacing:0.3px;">{subtitle}</div>
</div>
</div>
<div style="display:flex; align-items:center; gap:8px; flex-shrink:0;">
{lang_toggle_html}
<span style="background:rgba(255,255,255,0.18); border:1px solid rgba(255,255,255,0.3); padding:4px 12px; border-radius:20px; font-size:0.75rem; color:#FFFFFF; font-weight:600;">{display_id}</span>
<a href="/Citizen_Login" target="_self" style="background:#EF4444; color:#FFFFFF; padding:4px 10px; border-radius:14px; font-size:0.72rem; font-weight:700; text-decoration:none; display:inline-block;">{sign_out_label}</a>
</div>
</div>
<div style="display:flex; height:4px; width:100%;">
<div style="background:#FF9933; flex:1;"></div>
<div style="background:#FFFFFF; flex:1;"></div>
<div style="background:#138808; flex:1;"></div>
</div>
</div>"""
    st.markdown(cit_nav_html, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# render_split_login_header(logo_path, title, subtitle)
# ─────────────────────────────────────────────

def render_split_login_header(
    logo_path: str = "",
    title: str = "",
    subtitle: str = ""
) -> None:
    """
    Renders a clean split-layout login header with bilingual language toggle.
    """
    import base64
    import os

    current_lang = get_current_lang()
    hdr_title = title if title else t("officer_login_title", "Officer Login")
    hdr_sub = subtitle if subtitle else t("officer_login_sub", "Role-based access for authorized government officials")
    platform_tag = t("platform_badge", "PM GatiShakti • SIH26017 Prototype")

    logo_html = '<span style="font-size:3.5rem;">🌱</span>'
    if logo_path and os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(logo_path)[1].lstrip(".").lower()
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext
        logo_html = f'<img src="data:image/{mime};base64,{logo_b64}" style="height:76px;width:auto;object-fit:contain;border-radius:8px;">'

    en_style = "background:rgba(255,255,255,0.28); color:#FFFFFF; font-weight:700;" if current_lang == "en" else "color:#D1FAE5; font-weight:500;"
    hi_style = "background:rgba(255,255,255,0.28); color:#FFFFFF; font-weight:700;" if current_lang == "hi" else "color:#D1FAE5; font-weight:500;"

    lang_toggle_html = f"""<div style="display:flex; align-items:center; background:rgba(0,0,0,0.2); border-radius:20px; padding:2px 4px; gap:2px; border:1px solid rgba(255,255,255,0.25);">
<a href="?lang=en" target="_self" style="text-decoration:none; padding:3px 10px; border-radius:12px; font-size:0.74rem; {en_style}">🇬🇧 EN</a>
<a href="?lang=hi" target="_self" style="text-decoration:none; padding:3px 10px; border-radius:12px; font-size:0.74rem; {hi_style}">🇮🇳 हिन्दी</a>
</div>"""

    split_header_html = f"""<div style="background:linear-gradient(135deg,#064E3B 0%,#065F46 55%,#047857 100%); padding:20px 28px 0 28px; box-shadow:0 4px 16px rgba(6,78,59,0.35); margin-top: 4px; border-radius:10px 10px 0 0;">
<div style="display:flex;align-items:center;justify-content:space-between;gap:20px;padding-bottom:16px;flex-wrap:wrap;">
<div style="display:flex;align-items:center;gap:18px;">
<div style="flex-shrink:0;background:rgba(255,255,255,0.12); border-radius:12px;padding:8px;border:1px solid rgba(255,255,255,0.2);">
{logo_html}
</div>
<div>
<div style="font-size:1.75rem;font-weight:800;color:#FFFFFF; letter-spacing:-0.5px;line-height:1.1;">{hdr_title}</div>
<div style="font-size:0.88rem;color:#A7F3D0;margin-top:4px;">{hdr_sub}</div>
<div style="font-size:0.72rem;color:#D1FAE5;margin-top:4px;font-style:italic;">{platform_tag}</div>
</div>
</div>
<div>
{lang_toggle_html}
</div>
</div>
<div style="display:flex;height:5px;width:100%;">
<div style="background:#FF9933;flex:1;"></div>
<div style="background:#FFFFFF;flex:1;"></div>
<div style="background:#138808;flex:1;"></div>
</div>
</div>
<div style="height:12px;"></div>"""
    st.markdown(split_header_html, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 1. apply_gov_theme()
# ─────────────────────────────────────────────

def apply_gov_theme() -> None:
    """
    Injects the GOI Government Portal CSS into the current Streamlit page,
    along with cache-invalidation meta tags and bfcache protection.
    """
    st.markdown("""
<!-- ── Anti-Caching Directives & bfcache Protection ────────────────────────── -->
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">

<script>
(function() {
try {
var targets = [document];
if (window.parent && window.parent.document && window.parent.document !== document) {
targets.push(window.parent.document);
}
var directives = [
{ httpEquiv: 'Cache-Control', content: 'no-cache, no-store, must-revalidate' },
{ httpEquiv: 'Pragma', content: 'no-cache' },
{ httpEquiv: 'Expires', content: '0' }
];
targets.forEach(function(doc) {
if (!doc.head) return;
directives.forEach(function(d) {
var existing = doc.querySelector('meta[http-equiv="' + d.httpEquiv + '"]');
if (!existing) {
var m = doc.createElement('meta');
m.httpEquiv = d.httpEquiv;
m.content = d.content;
doc.head.appendChild(m);
}
});
});
} catch (e) {}

try {
window.addEventListener('pageshow', function(event) {
if (event.persisted) {
window.location.reload();
}
});
if (window.parent && window.parent !== window) {
window.parent.addEventListener('pageshow', function(event) {
if (event.persisted) {
window.parent.location.reload();
}
});
}
} catch (e) {}
})();
</script>

<style>
/* ── Google Fonts ─────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* ── Base Reset ───────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
font-family: 'Plus Jakarta Sans', 'Noto Sans Devanagari', 'Noto Sans', sans-serif !important;
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
.status-in_progress { background: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }
.status-delayed     { background: #FEE2E2; color: #991B1B; border: 1px solid #FECACA; }
.status-not_started { background: #F1F5F9; color: #475569; border: 1px solid #CBD5E1; }

/* ── GOI Footer ──────────────────────────────────────────────────────────── */
.gov-footer {
margin-top: 40px;
background: linear-gradient(135deg, #064E3B 0%, #065F46 60%, #047857 100%);
border-radius: 8px;
padding: 16px 24px;
color: #D1FAE5;
font-size: 0.78rem;
box-shadow: 0 4px 12px rgba(6, 78, 59, 0.25);
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
color: #A7F3D0;
margin-top: 2px;
}
.gov-footer-links {
margin-top: 6px;
display: flex;
gap: 14px;
flex-wrap: wrap;
}
.gov-footer-links a {
color: #D1FAE5;
text-decoration: underline;
font-size: 0.72rem;
}
.gov-footer-disclaimer {
font-size: 0.68rem;
color: #D1FAE5;
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
    """Renders the GOI navy/emerald header bar with emblem and badges."""
    st.markdown(f"""
<div class="gov-header" style="background:linear-gradient(135deg,#064E3B 0%,#065F46 60%,#047857 100%); padding:18px 28px 14px 28px; color:#FFFFFF;">
<div style="display:flex; align-items:center; gap:16px;">
<div style="font-size:2.2rem; line-height:1; flex-shrink:0;">🏛️</div>
<div style="flex:1;">
<div style="font-size:1.55rem; font-weight:800; color:#FFFFFF; margin:0; line-height:1.2;">🌱 {t("site_title", "BHOOMI AI")} — {t("site_subtitle", "Land Intelligence Platform")}</div>
<div style="font-size:0.82rem; font-weight:500; color:#A7F3D0; margin-top:3px;">{ministry}</div>
<div style="font-size:0.72rem; color:#D1FAE5; margin-top:2px; font-style:italic;">{t("platform_badge", "PM GatiShakti National Master Plan • SIH26017 Prototype")}</div>
</div>
</div>
</div>
<div style="display:flex; height:5px; width:100%;">
<div style="background:#FF9933; flex:1;"></div>
<div style="background:#FFFFFF; flex:1;"></div>
<div style="background:#138808; flex:1;"></div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 3. render_breadcrumb(path: list[str])
# ─────────────────────────────────────────────

def render_breadcrumb(path: list[str]) -> None:
    """Renders a GOI-style breadcrumb navigation bar."""
    if not path:
        return

    crumbs_html = ""
    for i, crumb in enumerate(path):
        is_last = (i == len(path) - 1)
        if is_last:
            crumbs_html += f'<span style="color:#64748B; font-weight:500;">{crumb}</span>'
        else:
            prefix = "🏠 " if i == 0 else ""
            crumbs_html += f'<span style="color:#065F46; font-weight:600;">{prefix}{crumb}</span>'
            crumbs_html += '<span style="color:#94A3B8; font-size:0.72rem; margin:0 4px;">›</span>'

    st.markdown(f"""
<div style="background:#F0FDF4; border-bottom:1px solid #BBF7D0; padding:8px 28px; font-size:0.8rem; color:#475569; display:flex; align-items:center; gap:4px; flex-wrap:wrap;">
{crumbs_html}
</div>
<div style="margin-bottom: 16px;"></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 4. status_pill(label, status)
# ─────────────────────────────────────────────

StatusType = Literal["complete", "in_progress", "delayed", "not_started"]

def status_pill(label: str, status: StatusType) -> str:
    """Returns an HTML string for a status pill badge."""
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
    """Renders the standardized GOI-style bilingual footer."""
    from datetime import datetime
    current_year = datetime.now().year
    disclaimer = t("footer_prototype_note", "This is a Smart India Hackathon prototype (SIH26017). Data used is for demonstration purposes only. Governed by IT Act, 2000.")

    st.markdown(f"""
<div class="gov-footer">
<div class="gov-footer-inner">
<div class="gov-footer-left">
<div class="gov-footer-logo-text">🌱 {t("site_title", "BHOOMI AI")}</div>
<div class="gov-footer-subtitle">
{t("site_subtitle", "Land Acquisition Delay Prediction & Risk Management System")}<br>
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
<div style="font-size: 0.72rem; color: #A7F3D0;">
🏛️ Ministry of Road Transport &amp; Highways<br>
🧠 Powered by XGBoost + TreeSHAP<br>
📊 MoSPI Mega Infrastructure Dataset<br>
📜 RFCTLARR Act, 2013 Compliant<br>
🔐 Role-Based Access Control (RBAC)
</div>
</div>
</div>
<div class="gov-footer-disclaimer">
⚠️ {disclaimer} © {current_year} BHOOMI AI Team.
</div>
</div>
""", unsafe_allow_html=True)
