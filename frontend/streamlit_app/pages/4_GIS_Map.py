import sys
import os
import streamlit as st
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium
import pandas as pd

# Ensure application directory and root are in sys.path
PAGE_DIR = os.path.abspath(os.path.dirname(__file__))
STREAMLIT_DIR = os.path.abspath(os.path.join(PAGE_DIR, ".."))
ROOT_DIR = os.path.abspath(os.path.join(PAGE_DIR, "..", "..", ".."))
for p in [PAGE_DIR, STREAMLIT_DIR, ROOT_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from utils.api_client import client
from utils.auth import render_sidebar_brand, is_authenticated, get_current_user

st.set_page_config(
    page_title="GIS Map — Bhoomi AI",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Render global Bhoomi AI sidebar branding
render_sidebar_brand()

# Custom Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .gis-header {
        background: linear-gradient(135deg, #064E3B 0%, #065F46 45%, #0F766E 100%);
        border-radius: 16px;
        padding: 24px 30px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 10px 20px -5px rgba(6, 78, 59, 0.3);
    }
    .gis-title {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        background: linear-gradient(90deg, #FFFFFF, #6EE7B7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .gis-subtitle {
        font-size: 0.95rem;
        color: #D1FAE5;
        margin-top: 6px;
        max-width: 850px;
        line-height: 1.5;
    }
    
    /* 3-Color Visual Guide */
    .legend-banner {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 12px 18px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 12px;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .legend-dot-red {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: #EF4444;
        box-shadow: 0 0 8px rgba(239, 68, 68, 0.6);
    }
    .legend-dot-orange {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: #F59E0B;
        box-shadow: 0 0 8px rgba(245, 158, 11, 0.6);
    }
    .legend-dot-green {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: #10B981;
        box-shadow: 0 0 8px rgba(16, 185, 129, 0.6);
    }
    
    .inspector-card {
        background: white;
        border-radius: 14px;
        border: 1.5px solid #E2E8F0;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    .kpi-chip {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 10px 14px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .kpi-chip-title {
        font-size: 0.72rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-chip-val {
        font-size: 1.4rem;
        font-weight: 800;
        margin-top: 2px;
    }
</style>
""", unsafe_allow_html=True)

# Top Hero Banner
st.markdown("""
<div class="gis-header">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
        <div>
            <h1 class="gis-title">🗺️ Geospatial Risk Radar & Land Acquisition GIS</h1>
            <div class="gis-subtitle">
                Interactive spatial intelligence tracking land bottlenecks, court stay orders, and compensation disbursements across 250+ national infrastructure corridors.
            </div>
        </div>
        <div>
            <span style="background: rgba(255, 255, 255, 0.15); border: 1px solid rgba(255, 255, 255, 0.3); color: white; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 0.8rem; backdrop-filter: blur(4px);">
                🇮🇳 PM GatiShakti NMP
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Backend Health Check
if not client.check_health():
    st.error("⚠️ Backend API is offline. Please start backend via `python run_backend.py`.")
    st.stop()

# Fetch GIS Data
try:
    markers_data = client.get_gis_data()
except Exception as e:
    st.error(f"Failed to load GIS data from backend: {e}")
    st.stop()

if not markers_data:
    st.warning("No geospatial project data available.")
    st.stop()

# 3-Color Plain-English Visual Guide
st.markdown("""
<div class="legend-banner">
    <div style="font-weight: 700; font-size: 0.85rem; color: #1E293B;">
        🧭 <strong>Map Color Guide:</strong>
    </div>
    <div class="legend-item">
        <div class="legend-dot-red"></div>
        <span><strong>Red (70–100):</strong> Critical Bottleneck (Court Stay / Low Compensation)</span>
    </div>
    <div class="legend-item">
        <div class="legend-dot-orange"></div>
        <span><strong>Orange (40–69):</strong> Watchlist (Compensation or Milestones Overdue)</span>
    </div>
    <div class="legend-item">
        <div class="legend-dot-green"></div>
        <span><strong>Green (1–39):</strong> On Schedule (Clearances Progressing Smoothly)</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Regional Coordinates Pre-sets
REGIONS = {
    "All India": {"lat": 22.8000, "lon": 80.0000, "zoom": 5, "states": None},
    "North Zone": {"lat": 28.6139, "lon": 77.2090, "zoom": 6, "states": ["Delhi", "Uttar Pradesh", "Haryana", "Punjab", "Rajasthan", "Bihar", "Uttarakhand"]},
    "South Zone": {"lat": 13.0827, "lon": 79.2707, "zoom": 6, "states": ["Andhra Pradesh", "Telangana", "Tamil Nadu", "Karnataka", "Kerala"]},
    "West Zone": {"lat": 21.1702, "lon": 73.8311, "zoom": 6, "states": ["Gujarat", "Maharashtra", "Goa", "Madhya Pradesh"]},
    "East & Central": {"lat": 23.5120, "lon": 85.3215, "zoom": 6, "states": ["West Bengal", "Odisha", "Jharkhand", "Chhattisgarh", "Assam"]}
}

# Top Filter & Quick Controls Bar
st.markdown("#### ⚡ 1-Click Regional Fast Focus & Filters")

c_reg, c_state, c_risk, c_mode = st.columns([2, 1.5, 1.5, 1.5])

with c_reg:
    selected_region = st.selectbox(
        "📍 Economic Corridor / Zone",
        list(REGIONS.keys()),
        index=0,
        help="Quickly zoom and center map to major economic development corridors"
    )

# Filter markers by region first
region_states = REGIONS[selected_region]["states"]
if region_states:
    available_states = ["All in Zone"] + sorted(list(set(m["state"] for m in markers_data if m["state"] in region_states)))
else:
    available_states = ["All States"] + sorted(list(set(m["state"] for m in markers_data)))

with c_state:
    selected_state = st.selectbox("🏛️ State", available_states, index=0)

with c_risk:
    selected_risk = st.selectbox("⚠️ Risk Filter", ["All Risks", "🔴 High Risk Only (>70)", "🟠 Watchlist (40-70)", "🟢 Low Risk (<40)"])

with c_mode:
    view_mode = st.selectbox("🗺️ Map Layer Style", ["📍 Pins & Clusters", "🔥 Risk Heatmap", "⭕ Delay Circles"])

# Apply Filters
filtered_markers = markers_data

if region_states:
    filtered_markers = [m for m in filtered_markers if m["state"] in region_states]

if selected_state not in ["All States", "All in Zone"]:
    filtered_markers = [m for m in filtered_markers if m["state"] == selected_state]

if selected_risk == "🔴 High Risk Only (>70)":
    filtered_markers = [m for m in filtered_markers if m["risk_category"] == "High"]
elif selected_risk == "🟠 Watchlist (40-70)":
    filtered_markers = [m for m in filtered_markers if m["risk_category"] == "Medium"]
elif selected_risk == "🟢 Low Risk (<40)":
    filtered_markers = [m for m in filtered_markers if m["risk_category"] == "Low"]

# Metric Summary Chips
c1, c2, c3, c4, c5 = st.columns(5)
total_count = len(filtered_markers)
high_count = sum(1 for m in filtered_markers if m["risk_category"] == "High")
med_count = sum(1 for m in filtered_markers if m["risk_category"] == "Medium")
low_count = sum(1 for m in filtered_markers if m["risk_category"] == "Low")
avg_delay = int(sum(m["delay_days"] for m in filtered_markers) / total_count) if total_count > 0 else 0

with c1:
    st.markdown(f"""
    <div class="kpi-chip">
        <div class="kpi-chip-title">Total Projects</div>
        <div class="kpi-chip-val" style="color: #0F172A;">{total_count}</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="kpi-chip" style="border-left: 4px solid #EF4444;">
        <div class="kpi-chip-title">🔴 Critical Bottlenecks</div>
        <div class="kpi-chip-val" style="color: #DC2626;">{high_count}</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="kpi-chip" style="border-left: 4px solid #F59E0B;">
        <div class="kpi-chip-title">🟠 Watchlist Projects</div>
        <div class="kpi-chip-val" style="color: #D97706;">{med_count}</div>
    </div>
    """, unsafe_allow_html=True)
with c4:
    st.markdown(f"""
    <div class="kpi-chip" style="border-left: 4px solid #10B981;">
        <div class="kpi-chip-title">🟢 On Track</div>
        <div class="kpi-chip-val" style="color: #059669;">{low_count}</div>
    </div>
    """, unsafe_allow_html=True)
with c5:
    st.markdown(f"""
    <div class="kpi-chip">
        <div class="kpi-chip-title">Avg Forecasted Delay</div>
        <div class="kpi-chip-val" style="color: #2563EB;">+{avg_delay} d</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Interactive Project Spotlight Selector
project_options = ["-- Select a Project to Spotlight on Map --"] + [
    f"{m['project_id']} — {m['project_name']} ({m['state']}) [Score: {m['risk_score']}]"
    for m in filtered_markers
]
spotlight_selection = st.selectbox(
    "🎯 Spotlight & Jump to Project on Map:",
    project_options,
    index=0,
    help="Select any project to zoom directly into its exact GPS location and inspect live details."
)

spotlight_project = None
if spotlight_selection != "-- Select a Project to Spotlight on Map --":
    selected_id = spotlight_selection.split(" — ")[0]
    for m in filtered_markers:
        if m["project_id"] == selected_id:
            spotlight_project = m
            break

# Calculate Map Center
if spotlight_project:
    center_lat = spotlight_project["latitude"]
    center_lon = spotlight_project["longitude"]
    zoom = 9
elif selected_state not in ["All States", "All in Zone"] and filtered_markers:
    center_lat = sum(m["latitude"] for m in filtered_markers) / len(filtered_markers)
    center_lon = sum(m["longitude"] for m in filtered_markers) / len(filtered_markers)
    zoom = 7
else:
    center_lat = REGIONS[selected_region]["lat"]
    center_lon = REGIONS[selected_region]["lon"]
    zoom = REGIONS[selected_region]["zoom"]

# Build Folium Map
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=zoom,
    tiles="OpenStreetMap",
    control_scale=True
)

if view_mode == "🔥 Risk Heatmap":
    heat_data = [[m["latitude"], m["longitude"], m["risk_score"] / 100.0] for m in filtered_markers]
    HeatMap(heat_data, radius=18, blur=14, max_zoom=10).add_to(m)

elif view_mode == "⭕ Delay Circles":
    for proj in filtered_markers:
        rad = max(6, min(24, proj["delay_days"] / 20))
        folium.CircleMarker(
            location=[proj["latitude"], proj["longitude"]],
            radius=rad,
            color=proj["color_code"],
            fill=True,
            fill_color=proj["color_code"],
            fill_opacity=0.6,
            tooltip=f"{proj['project_name']} | Delay: +{proj['delay_days']}d | Score: {proj['risk_score']}",
            popup=f"<b>{proj['project_name']}</b><br>Delay: +{proj['delay_days']} days<br>Risk: {proj['risk_score']}/100"
        ).add_to(m)

else:
    # Standard Pins & Clusters
    cluster = MarkerCluster(name="Infrastructure Projects").add_to(m)
    for proj in filtered_markers:
        if proj["risk_category"] == "High":
            pin_color = "red"
            icon_name = "exclamation-triangle"
        elif proj["risk_category"] == "Medium":
            pin_color = "orange"
            icon_name = "clock-o"
        else:
            pin_color = "green"
            icon_name = "check"

        popup_html = f"""
        <div style="font-family: 'Segoe UI', Arial, sans-serif; min-width: 220px; padding: 4px;">
            <div style="font-weight: 800; color: #064E3B; font-size: 14px; margin-bottom: 4px;">{proj['project_name']}</div>
            <div style="font-size: 11px; color: #64748B; margin-bottom: 8px;">ID: <b>{proj['project_id']}</b> | {proj['district']}, {proj['state']}</div>
            <div style="background: #F1F5F9; border-radius: 6px; padding: 6px 10px; margin-bottom: 8px; font-size: 12px;">
                <b>Risk Score:</b> <span style="color: {proj['color_code']}; font-weight: 800;">{proj['risk_score']}/100 ({proj['risk_category']})</span><br>
                <b>Forecasted Delay:</b> +{proj['delay_days']} days<br>
                <b>Compensation Paid:</b> {proj['compensation_pct']}%<br>
                <b>Litigation:</b> {'⚠️ Active Court Stay' if proj['legal_case'] == 1 else '⚖️ Clear'}
            </div>
            <div style="font-size: 11px; color: #475569;">
                <b>Stage:</b> {proj['stage']}
            </div>
        </div>
        """

        folium.Marker(
            location=[proj["latitude"], proj["longitude"]],
            popup=folium.Popup(popup_html, max_width=320),
            tooltip=f"{proj['project_name']} — Risk: {proj['risk_score']}/100 (+{proj['delay_days']} days)",
            icon=folium.Icon(color=pin_color, icon=icon_name, prefix="fa")
        ).add_to(cluster)

# If a project is spotlighted, add a high-visibility pulsing beacon
if spotlight_project:
    folium.CircleMarker(
        location=[spotlight_project["latitude"], spotlight_project["longitude"]],
        radius=28,
        color="#EF4444",
        fill=True,
        fill_color="#F87171",
        fill_opacity=0.35,
        weight=3,
        tooltip="📍 SPOTLIGHTED PROJECT"
    ).add_to(m)

# Two-Column Layout: Left Map (65%), Right Inspector (35%)
col_map, col_inspector = st.columns([65, 35])

with col_map:
    st_folium(m, use_container_width=True, height=600)
    st.caption("💡 **Easy Navigation Tip:** Click any pin to open its data bubble, or scroll/drag to pan anywhere across India.")

with col_inspector:
    st.markdown("### 🎯 Live Project Inspector")
    
    # Use spotlight project if selected, else default to the top-risk project
    active_p = spotlight_project
    if not active_p and filtered_markers:
        # Default to highest risk project in view
        active_p = sorted(filtered_markers, key=lambda x: x["risk_score"], reverse=True)[0]

    if active_p:
        is_high = active_p["risk_category"] == "High"
        is_med = active_p["risk_category"] == "Medium"
        badge_bg = "#FEE2E2" if is_high else ("#FEF3C7" if is_med else "#D1FAE5")
        badge_fg = "#DC2626" if is_high else ("#D97706" if is_med else "#059669")

        st.markdown(f"""
        <div class="inspector-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <span style="background: {badge_bg}; color: {badge_fg}; font-size: 0.75rem; font-weight: 800; padding: 4px 10px; border-radius: 12px;">
                    {active_p['risk_category'].upper()} RISK ({active_p['risk_score']}/100)
                </span>
                <span style="font-size: 0.75rem; color: #64748B; font-weight: 600;">{active_p.get('sector', 'Infrastructure')}</span>
            </div>
            <h3 style="margin: 10px 0 4px 0; color: #0F172A; font-size: 1.25rem;">{active_p['project_name']}</h3>
            <div style="font-size: 0.8rem; color: #64748B; margin-bottom: 12px;">
                📍 {active_p['district']}, {active_p['state']} • Code: <code>{active_p['project_id']}</code>
            </div>
            
            <div style="background: #F8FAFC; border-radius: 10px; padding: 12px; margin-bottom: 12px; border: 1px solid #E2E8F0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 0.82rem;">
                    <span style="color: #475569;">Forecasted Delay:</span>
                    <strong style="color: #DC2626;">+{active_p['delay_days']} days</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 0.82rem;">
                    <span style="color: #475569;">Acquisition Stage:</span>
                    <strong style="color: #1E293B;">{active_p['stage']}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 0.82rem;">
                    <span style="color: #475569;">Disbursed Compensation:</span>
                    <strong style="color: {'#16A34A' if active_p['compensation_pct'] >= 70 else '#DC2626'};">{active_p['compensation_pct']}%</strong>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.82rem;">
                    <span style="color: #475569;">Litigation / Stay Order:</span>
                    <strong style="color: {'#DC2626' if active_p['legal_case'] == 1 else '#16A34A'};">
                        {'⚠️ Active Injunction' if active_p['legal_case'] == 1 else '⚖️ No Active Disputes'}
                    </strong>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Plain-English AI Diagnosis
        st.markdown("**🧠 Plain-English AI Root Cause:**")
        if active_p["legal_case"] == 1 and active_p["compensation_pct"] < 40:
            st.warning("⚠️ **Severe Impediment:** Land possession is stalled by an active High Court injunction and low compensation disbursement (<40%). Rapid settlement via CALA tribunal recommended.")
        elif active_p["compensation_pct"] < 30:
            st.warning("⚠️ **Financial Disbursement Lag:** Affected landholders have received under 30% of statutory compensation, risking civil unrest and work stoppages.")
        elif active_p["legal_case"] == 1:
            st.info("⚖️ **Legal Injunction:** Court stay order in effect. Requires state advocate general fast-track petition.")
        else:
            st.success("✅ **Smooth Progression:** Compensation disbursement is proceeding steadily with no major legal impediments.")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Quick Action buttons
        c_act1, c_act2 = st.columns(2)
        with c_act1:
            if st.button("📊 TreeSHAP Why?", key="btn_insp_shap", width="stretch"):
                st.session_state["selected_project_id"] = active_p["project_id"]
                st.switch_page("pages/3_SHAP_Explanations.py")
        with c_act2:
            if st.button("📄 Full Dossier", key="btn_insp_dossier", width="stretch"):
                st.session_state["selected_project_id"] = active_p["project_id"]
                st.switch_page("pages/1_Project_Details.py")


# Top Hotspots Quick Table Below
st.markdown("---")
st.markdown("### 🔥 Top 5 High-Risk Bottlenecks in Current View")
top_5 = sorted(filtered_markers, key=lambda x: x["risk_score"], reverse=True)[:5]

top_cols = st.columns(5)
for idx, p in enumerate(top_5):
    with top_cols[idx]:
        st.markdown(f"""
        <div style="background: white; border: 1px solid #E2E8F0; border-top: 4px solid #EF4444; border-radius: 10px; padding: 12px; height: 100%;">
            <div style="font-size: 0.72rem; color: #EF4444; font-weight: 800;">SCORE: {p['risk_score']}/100</div>
            <div style="font-weight: 700; font-size: 0.85rem; color: #0F172A; margin: 4px 0; min-height: 40px;">{p['project_name']}</div>
            <div style="font-size: 0.75rem; color: #64748B;">📍 {p['state']}</div>
            <div style="font-size: 0.75rem; color: #DC2626; font-weight: 600; margin-top: 4px;">+{p['delay_days']} days delay</div>
        </div>
        """, unsafe_allow_html=True)
