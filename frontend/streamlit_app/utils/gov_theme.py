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
# NAV_ITEMS — horizontal navbar page list with SPA page links
# ─────────────────────────────────────────────

NAV_ITEMS = [
    {"label": "🏛️ Dashboard", "slug": "Officer_Dashboard", "url": "/Officer_Dashboard"},
    {"label": "📊 Projects", "slug": "Project_Details", "url": "/Project_Details"},
    {"label": "🏆 Risk Ranking", "slug": "Risk_Ranking", "url": "/Risk_Ranking"},
    {"label": "💰 Capital Allocation", "slug": "Capital_Allocation", "url": "/Capital_Allocation"},
    {"label": "🧠 SHAP AI", "slug": "SHAP_Explanations", "url": "/SHAP_Explanations"},
    {"label": "🗺️ GIS Map", "slug": "GIS_Map", "url": "/GIS_Map"},
    {"label": "🚨 Alerts", "slug": "Alerts", "url": "/Alerts"},
    {"label": "➕ Add Project", "slug": "Add_Project", "url": "/Add_Project"},
    {"label": "📜 DILRMP", "slug": "DILRMP_Land_Records", "url": "/DILRMP_Land_Records"},
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
    Renders the clean role-selection landing hero & cards (Officer Login / Citizen Login).
    """
    import base64
    import os

    logo_img_html = '<span style="font-size:3.2rem;">🌱</span>'
    if logo_path and os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(logo_path)[1].lstrip(".").lower()
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext
        logo_img_html = f'<img src="data:image/{mime};base64,{logo_b64}" style="height:64px; width:auto; object-fit:contain; border-radius:8px; background:rgba(255,255,255,0.12); padding:4px; border:1px solid rgba(255,255,255,0.2);">'

    html = f"""<style>
.landing-hero-band {{
background: linear-gradient(135deg, #064E3B 0%, #065F46 50%, #047857 100%);
border-radius: 12px;
padding: 28px 32px 24px 32px;
color: #FFFFFF;
box-shadow: 0 10px 25px -5px rgba(6, 78, 59, 0.25);
margin-top: 10px;
margin-bottom: 28px;
text-align: center;
}}
.landing-tricolor {{
display: flex;
height: 5px;
width: 100%;
margin-bottom: 18px;
border-radius: 3px;
overflow: hidden;
}}
.landing-tricolor .saffron {{ background: #FF9933; flex: 1; }}
.landing-tricolor .white {{ background: #FFFFFF; flex: 1; }}
.landing-tricolor .green {{ background: #138808; flex: 1; }}
.landing-title {{
font-size: 2.3rem;
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
font-size: 1.05rem;
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
padding: 28px 24px;
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
width: 64px;
height: 64px;
border-radius: 50%;
display: flex;
align-items: center;
justify-content: center;
font-size: 2rem;
margin: 0 auto 16px auto;
background: #DCFCE7;
color: #065F46;
border: 1.5px solid #A7F3D0;
}}
.role-card-heading {{
font-size: 1.4rem;
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
margin: 0 0 24px 0;
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
<div class="landing-tricolor">
<div class="saffron"></div>
<div class="white"></div>
<div class="green"></div>
</div>
<div style="display:flex; justify-content:center; align-items:center; margin-bottom:10px;">
{logo_img_html}
</div>
<div class="landing-title">{site_title}</div>
<div class="landing-tagline">LAND • DATA • BETTER TOMORROW</div>
<div class="landing-subtitle">{site_subtitle}</div>
<div class="landing-trust">PM GATISHAKTI • SIH26017 PROTOTYPE</div>
</div>
<div class="cards-container">
<div class="role-select-card role-card-officer">
<div>
<div class="icon-badge">🔐</div>
<div class="role-card-heading">Officer Portal</div>
<div class="role-card-desc">Role-based access for CALA, National Project Directors, MoSPI monitors, and SIH jury evaluation.</div>
<ul class="feature-pill-list">
<li><span>🤖</span> <strong>TreeSHAP AI:</strong> Delay cause attribution</li>
<li><span>📊</span> <strong>Risk Ranking:</strong> Portfolio-wide delay prediction</li>
<li><span>🗺️</span> <strong>GIS Corridor:</strong> Alignment risk mapping</li>
<li><span>🚨</span> <strong>Smart Alerts:</strong> Section 24 lapsing risk warnings</li>
</ul>
</div>
<a href="/Officer_Login" target="_self" class="portal-action-btn">🔐 Go to Officer Login →</a>
</div>
<div class="role-select-card role-card-citizen">
<div>
<div class="icon-badge">🧑‍🌾</div>
<div class="role-card-heading">Citizen Land Tracker</div>
<div class="role-card-desc">Public parcel tracking for landowners and affected families under RFCTLARR Act, 2013.</div>
<ul class="feature-pill-list">
<li><span>📱</span> <strong>OTP Verification:</strong> Direct mobile/email access</li>
<li><span>💰</span> <strong>Compensation Status:</strong> SLA tracking & payout</li>
<li><span>⚖️</span> <strong>Statutory Rights:</strong> Section 24 & grievance filing</li>
<li><span>📜</span> <strong>Land Records:</strong> DILRMP ownership verification</li>
</ul>
</div>
<a href="/Citizen_Login" target="_self" class="portal-action-btn portal-action-btn-citizen">🧑‍🌾 Go to Citizen Login →</a>
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
padding-top: 1rem !important;
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
    site_title: str = "BHOOMI AI",
    site_subtitle: str = "Land Intelligence Platform"
) -> None:
    """
    Renders a full-width sticky top navbar with brand, full navigation items,
    active state highlight, officer session badge, and Sign Out button.
    """
    import base64
    import os

    logo_img_html = '<span style="font-size:1.8rem;">🌱</span>'
    if logo_path and os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(logo_path)[1].lstrip(".").lower()
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext
        logo_img_html = f'<img src="data:image/{mime};base64,{logo_b64}" style="height:44px; width:auto; object-fit:contain; border-radius:6px; background:rgba(255,255,255,0.12); padding:2px;">'

    nav_links_html = ""
    for item in NAV_ITEMS:
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
        session_badge_html = f'<span style="background:rgba(255,255,255,0.18); border:1px solid rgba(255,255,255,0.3); padding:4px 10px; border-radius:20px; font-size:0.72rem; color:#A7F3D0; font-weight:600; white-space:nowrap;">🌾 Citizen ···{masked}</span>'

    navbar_html = f"""<div style="background:linear-gradient(135deg,#064E3B 0%,#065F46 50%,#047857 100%); padding:0 20px; box-shadow:0 4px 16px rgba(6,78,59,0.3); margin-bottom:12px; border-radius:0 0 4px 4px;">
<div style="display:flex; align-items:center; justify-content:space-between; min-height:58px; flex-wrap:wrap; gap:8px;">
<div style="display:flex; align-items:center; gap:10px; flex-shrink:0;">
{logo_img_html}
<div>
<div style="font-size:1.1rem; font-weight:800; color:#FFFFFF; letter-spacing:-0.3px; line-height:1.1;">{site_title}</div>
<div style="font-size:0.65rem; color:#A7F3D0; font-weight:500; letter-spacing:0.3px;">{site_subtitle}</div>
</div>
</div>
<div style="display:flex; align-items:flex-end; gap:2px; flex-wrap:wrap;">
{nav_links_html}
</div>
<div style="display:flex; align-items:center; gap:8px; flex-shrink:0;">
{session_badge_html}
<a href="/Officer_Login" target="_self" style="background:#EF4444; color:#FFFFFF; padding:4px 10px; border-radius:14px; font-size:0.72rem; font-weight:700; text-decoration:none; display:inline-block; transition: background 0.15s ease;">🚪 Sign Out</a>
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
    site_title: str = "BHOOMI AI",
    site_subtitle: str = "Citizen Land Acquisition Tracker"
) -> None:
    """
    Renders a dedicated, emerald-green citizen navbar with zero officer information,
    and an isolated citizen session status badge + sign out button.
    """
    import base64
    import os

    logo_img_html = '<span style="font-size:1.8rem;">🌱</span>'
    if logo_path and os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(logo_path)[1].lstrip(".").lower()
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext
        logo_img_html = f'<img src="data:image/{mime};base64,{logo_b64}" style="height:44px; width:auto; object-fit:contain; border-radius:6px; background:rgba(255,255,255,0.12); padding:2px;">'

    cid = st.session_state.get("citizen_identifier", "")
    display_id = f"🌾 Welcome: {cid}" if cid else "🌾 Welcome Citizen"

    cit_nav_html = f"""<div style="background:linear-gradient(135deg,#064E3B 0%,#065F46 50%,#047857 100%); padding:0 20px; box-shadow:0 4px 16px rgba(6,78,59,0.3); margin-bottom:12px; border-radius:0 0 4px 4px;">
<div style="display:flex; align-items:center; justify-content:space-between; min-height:58px; flex-wrap:wrap; gap:8px;">
<div style="display:flex; align-items:center; gap:10px; flex-shrink:0;">
{logo_img_html}
<div>
<div style="font-size:1.1rem; font-weight:800; color:#FFFFFF; letter-spacing:-0.3px; line-height:1.1;">{site_title}</div>
<div style="font-size:0.65rem; color:#A7F3D0; font-weight:500; letter-spacing:0.3px;">{site_subtitle}</div>
</div>
</div>
<div style="display:flex; align-items:center; gap:10px; flex-shrink:0;">
<span style="background:rgba(255,255,255,0.18); border:1px solid rgba(255,255,255,0.3); padding:4px 12px; border-radius:20px; font-size:0.75rem; color:#FFFFFF; font-weight:600;">{display_id}</span>
<a href="/Citizen_Login" target="_self" style="background:#EF4444; color:#FFFFFF; padding:4px 10px; border-radius:14px; font-size:0.72rem; font-weight:700; text-decoration:none; display:inline-block;">🚪 Sign Out</a>
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
    title: str = "Officer Login",
    subtitle: str = "Role-based access for authorized government officials"
) -> None:
    """
    Renders a clean split-layout login header.
    """
    import base64
    import os

    logo_html = '<span style="font-size:3.5rem;">🌱</span>'
    if logo_path and os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(logo_path)[1].lstrip(".").lower()
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext
        logo_html = f'<img src="data:image/{mime};base64,{logo_b64}" style="height:80px;width:auto;object-fit:contain;border-radius:8px;">'

    split_header_html = f"""<div style="background:linear-gradient(135deg,#064E3B 0%,#065F46 55%,#047857 100%); padding:24px 28px 0 28px; box-shadow:0 4px 16px rgba(6,78,59,0.35); margin-top: 10px;">
<div style="display:flex;align-items:center;gap:20px;padding-bottom:16px;">
<div style="flex-shrink:0;background:rgba(255,255,255,0.12); border-radius:12px;padding:10px;border:1px solid rgba(255,255,255,0.2);">
{logo_html}
</div>
<div>
<div style="font-size:1.8rem;font-weight:800;color:#FFFFFF; letter-spacing:-0.5px;line-height:1.1;">{title}</div>
<div style="font-size:0.9rem;color:#A7F3D0;margin-top:4px;">{subtitle}</div>
<div style="font-size:0.72rem;color:#D1FAE5;margin-top:4px;font-style:italic;">PM GatiShakti • SIH26017 Prototype</div>
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
# Injects GOI-standard CSS: navy palette, typography, card styles, tricolor strip.
# ─────────────────────────────────────────────

def apply_gov_theme() -> None:
    """
    Injects the GOI Government Portal CSS into the current Streamlit page,
    along with cache-invalidation meta tags and bfcache protection.
    Must be called immediately after st.set_page_config().
    """
    st.markdown("""

<!-- ── Anti-Caching Directives & bfcache Protection ────────────────────────── -->
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">

<script>
(function() {
// 1. Inject no-cache headers into parent and local <head>
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

// 2. bfcache (back-forward cache) protection — force fresh reload when restored
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
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* ── Base Reset ───────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
font-family: 'Noto Sans', 'Plus Jakarta Sans', sans-serif !important;
}

/* ── BHOOMI AI Top Navbar Styling ────────────────────────────────────────── */
div[data-testid="stHorizontalBlock"]:has(.bhoomi-tricolor-nav) {
background: linear-gradient(135deg, #064E3B 0%, #065F46 55%, #047857 100%) !important;
border-radius: 8px 8px 0 0 !important;
padding: 6px 14px 2px 14px !important;
box-shadow: 0 4px 16px rgba(6, 78, 59, 0.35) !important;
align-items: center !important;
}

.bhoomi-tricolor-nav {
display: flex;
height: 4px;
width: 100%;
margin-top: 2px;
border-radius: 0 0 4px 4px;
overflow: hidden;
}

/* Page Link base in Top Navbar */
div[data-testid="stHorizontalBlock"]:has(.bhoomi-tricolor-nav) div[data-testid="stPageLink-NavLink"] {
background: transparent !important;
border: none !important;
color: #FFFFFF !important;
padding: 6px 6px !important;
border-radius: 6px 6px 0 0 !important;
font-size: 0.76rem !important;
font-weight: 600 !important;
white-space: nowrap !important;
display: inline-flex !important;
align-items: center !important;
justify-content: center !important;
text-decoration: none !important;
transition: all 0.15s ease !important;
min-height: 34px !important;
}

div[data-testid="stHorizontalBlock"]:has(.bhoomi-tricolor-nav) div[data-testid="stPageLink-NavLink"]:hover {
background: rgba(255, 255, 255, 0.18) !important;
color: #A7F3D0 !important;
}

/* Active tab highlight */
.bhoomi-nav-active-wrap div[data-testid="stPageLink-NavLink"],
div[data-testid="stHorizontalBlock"]:has(.bhoomi-tricolor-nav) div[data-testid="stPageLink-NavLink"][aria-current="page"] {
background: rgba(255, 255, 255, 0.24) !important;
font-weight: 800 !important;
border-bottom: 3px solid #FF9933 !important;
color: #FFFFFF !important;
}

/* Sign Out button */
div[data-testid="stHorizontalBlock"]:has(.bhoomi-tricolor-nav) div[data-testid="column"]:last-child div[data-testid="stPageLink-NavLink"] {
background: #EF4444 !important;
color: #FFFFFF !important;
border-radius: 12px !important;
padding: 2px 8px !important;
font-size: 0.68rem !important;
font-weight: 700 !important;
min-height: 24px !important;
margin-top: 2px !important;
}
div[data-testid="stHorizontalBlock"]:has(.bhoomi-tricolor-nav) div[data-testid="column"]:last-child div[data-testid="stPageLink-NavLink"]:hover {
background: #DC2626 !important;
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

/* ── Emerald GOI Header ─────────────────────────────────────────────────── */
.gov-header {
background: linear-gradient(135deg, #064E3B 0%, #065F46 60%, #047857 100%);
padding: 18px 28px 14px 28px;
border-radius: 0 0 0 0;
color: #FFFFFF;
margin-bottom: 0;
box-shadow: 0 4px 12px rgba(6, 78, 59, 0.25);
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
color: #A7F3D0;
margin-top: 3px;
letter-spacing: 0.4px;
}
.gov-header-tagline {
font-size: 0.72rem;
color: #D1FAE5;
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
color: #ECFDF5;
backdrop-filter: blur(4px);
}

/* ── Breadcrumb Nav ──────────────────────────────────────────────────────── */
.gov-breadcrumb {
background: #F0FDF4;
border-bottom: 1px solid #BBF7D0;
padding: 8px 28px;
font-size: 0.8rem;
color: #475569;
display: flex;
align-items: center;
gap: 4px;
flex-wrap: wrap;
}
.gov-breadcrumb a, .gov-breadcrumb .bc-item {
color: #065F46;
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
⚠️ This is a Smart India Hackathon prototype (SIH26017). Data used is for demonstration purposes only.
Not an official Government of India publication. © {current_year} BHOOMI AI Team.
Governed by IT Act, 2000 | Data Protection Standards.
</div>
</div>

""", unsafe_allow_html=True)

