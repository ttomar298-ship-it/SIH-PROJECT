import sys
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Ensure application directory and root are in sys.path
STREAMLIT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(STREAMLIT_DIR, "..", ".."))
for p in [STREAMLIT_DIR, ROOT_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

import logging
logger = logging.getLogger("bhoomi_ai.home")

try:
    from utils.api_client import client
    from utils.auth import render_sidebar_brand, is_authenticated, get_current_user, LOGO_PATH
    from utils.config import USE_LIVE_API, get_dataset_metadata
except ImportError:
    from frontend.streamlit_app.utils.api_client import client
    from frontend.streamlit_app.utils.auth import render_sidebar_brand, is_authenticated, get_current_user, LOGO_PATH
    from frontend.streamlit_app.utils.config import USE_LIVE_API, get_dataset_metadata

st.set_page_config(
    page_title="BHOOMI AI — PM GatiShakti Land Intelligence",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Render global Bhoomi AI sidebar branding & logo
render_sidebar_brand()


# Premium Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #1E3A8A 100%);
        border-radius: 16px;
        padding: 28px 36px;
        margin-bottom: 24px;
        color: white;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        background: linear-gradient(90deg, #FFFFFF, #93C5FD);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #94A3B8;
        margin-top: 6px;
        max-width: 800px;
        line-height: 1.5;
    }
    .hero-badges {
        display: flex;
        gap: 10px;
        margin-top: 14px;
        flex-wrap: wrap;
    }
    .gov-badge {
        background: rgba(255, 255, 255, 0.12);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(4px);
    }

    /* Metric Cards */
    .stat-card {
        background: white;
        border-radius: 14px;
        padding: 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }
    .stat-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: 800;
        color: #0F172A;
        margin: 6px 0;
    }
    .stat-caption {
        font-size: 0.85rem;
        color: #475569;
        font-weight: 500;
    }

    /* Explain Card */
    .explain-box {
        background: #F8FAFC;
        border-left: 4px solid #3B82F6;
        padding: 16px 20px;
        border-radius: 0 12px 12px 0;
        margin-bottom: 20px;
    }
    
    /* Risk Badges */
    .risk-pill-high {
        background: #FEE2E2;
        color: #DC2626;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .risk-pill-med {
        background: #FEF3C7;
        color: #D97706;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .risk-pill-low {
        background: #D1FAE5;
        color: #059669;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Hero Header Banner with Bhoomi AI branding & accurate dataset status
curr_user = get_current_user()
welcome_msg = f"Welcome back, <strong>{curr_user['name']}</strong> ({curr_user['role']})" if curr_user else "Welcome, Officer / Observer • <a href='pages/0_🔐_Officer_Login.py' style='color: #6EE7B7; text-decoration: underline;'>Sign in for official clearance</a>"

dataset_meta = get_dataset_metadata()
if dataset_meta["use_live_api"]:
    status_badge_html = '<span style="background: rgba(16, 185, 129, 0.2); color: #34D399; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 0.82rem; border: 1px solid rgba(52, 211, 153, 0.4);">🟢 LIVE API CONNECTED</span>'
else:
    status_badge_html = '<span style="background: rgba(148, 163, 184, 0.2); color: #CBD5E1; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 0.82rem; border: 1px solid rgba(148, 163, 184, 0.4);" title="Static benchmark dataset — no external live streaming feed connected">📦 BENCHMARK DATASET (Static)</span>'

st.markdown(f"""
<div class="hero-container">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
        <div>
            <div style="font-size: 0.82rem; font-weight: 800; letter-spacing: 2px; color: #4ADE80; margin-bottom: 4px;">
                🌱 BHOOMI AI • LAND • DATA • BETTER TOMORROW
            </div>
            <h1 class="hero-title">PM GatiShakti • National Land & Delay Intelligence</h1>
            <p class="hero-subtitle">
                AI decision-support system forecasting infrastructure delays, mitigating land acquisition bottlenecks, and integrating DILRMP land digitization.
            </p>
            <div style="margin-top: 6px; font-size: 0.85rem; color: #CBD5E1;">
                👤 {welcome_msg}
            </div>
            <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 8px; background: rgba(0,0,0,0.25); padding: 4px 10px; border-radius: 6px; display: inline-block;">
                📅 <strong>Data As Of:</strong> {dataset_meta['last_updated']} • <strong>Coverage:</strong> {dataset_meta['record_count']} National Mega-Projects • <strong>Source:</strong> {dataset_meta['source_attribution']}
            </div>
            <div class="hero-badges" style="margin-top: 10px;">
                <span class="gov-badge">🤖 TreeSHAP Explainable AI</span>
                <span class="gov-badge">📊 {dataset_meta['record_count']} National Mega Projects</span>
                <span class="gov-badge">📜 34 States DILRMP Data</span>
                <span class="gov-badge">🚨 Automated Priority Alerts</span>
            </div>
        </div>
        <div style="text-align: right;">
            {status_badge_html}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Data Refresh controls
c_refresh_left, c_refresh_btn = st.columns([5, 1])
with c_refresh_btn:
    if st.button("🔄 Refresh Data", key="btn_refresh_dashboard", help="Reload latest cached records"):
        st.cache_data.clear()
        st.rerun()

# Check API health
if not client.check_health():
    st.error("⚠️ Backend API service is offline. Please launch the backend via `python run_backend.py`.")
    st.stop()

# Fetch dashboard data
data = None
with st.spinner("Loading infrastructure portfolio dataset..."):
    try:
        data = client.get_dashboard_data()
    except Exception as e:
        logger.error("Error loading dashboard data: %s", e, exc_info=True)
        st.error("⚠️ Unable to load portfolio dashboard data. Please verify the backend service is running.")
        st.stop()


# 1. Plain English Guide
with st.expander("💡 **How to Read This Dashboard in 30 Seconds** (Click to Expand)", expanded=False):
    st.markdown("""
    - **What does this system do?** It continuously evaluates project risks using machine learning trained on **real Indian infrastructure history** (MoSPI & state data).
    - **What does the Risk Score mean?**
      - 🟢 **1 to 39 (Low Risk):** Land acquisition and compensation are proceeding smoothly. No critical delays anticipated.
      - 🟠 **40 to 69 (Medium Risk / Watchlist):** Compensation or R&R is lagging behind schedule. Requires proactive monitoring.
      - 🔴 **70 to 100 (Critical High Alert):** Imminent multi-month delay risk. Usually driven by active court stays, severe compensation deficits, or non-digitized land boundaries.
    - **Why does Land Record Digitization (DILRMP) matter?** In states where land records are computerized (>99%), title search takes days. In states with paper records (<90%), title verification takes months, causing severe delay.
    """)

# 2. Executive KPI Cards
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="stat-card" style="border-top: 4px solid #3B82F6;">
        <div class="stat-title">Total Monitored Projects</div>
        <div class="stat-value">{data['total_projects']}</div>
        <div class="stat-caption">Highways, Railways, Ports, Irrigation</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    delayed_pct = data['delayed_projects_pct']
    st.markdown(f"""
    <div class="stat-card" style="border-top: 4px solid #EF4444;">
        <div class="stat-title">Projects Facing Delay</div>
        <div class="stat-value" style="color: #DC2626;">{data['delayed_projects_count']} <span style="font-size: 1.1rem; color: #64748B;">({delayed_pct}%)</span></div>
        <div class="stat-caption">Exceeding planned completion date</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    avg_score = data['avg_risk_score']
    color = "#EF4444" if avg_score > 70 else ("#F59E0B" if avg_score > 40 else "#10B981")
    st.markdown(f"""
    <div class="stat-card" style="border-top: 4px solid {color};">
        <div class="stat-title">National Average Risk Score</div>
        <div class="stat-value" style="color: {color};">{avg_score} <span style="font-size: 1.1rem; color: #64748B;">/ 100</span></div>
        <div class="stat-caption">{'Elevated Risk Zone' if avg_score > 60 else 'Stable'}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    critical_alerts = data['high_risk_count']
    st.markdown(f"""
    <div class="stat-card" style="border-top: 4px solid #DC2626;">
        <div class="stat-title">Urgent Action Alerts</div>
        <div class="stat-value" style="color: #DC2626;">{critical_alerts}</div>
        <div class="stat-caption">Threshold ≥ 70 requiring officer review</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# 3. Interactive Charts Row
df_projects = pd.DataFrame(data["projects"])

col_chart_left, col_chart_right = st.columns([3, 2])

with col_chart_left:
    st.subheader("📊 Acquisition Milestone Progression")
    stage_counts = df_projects["stage"].value_counts().reset_index()
    stage_counts.columns = ["Milestone Stage", "Number of Projects"]
    
    fig_bar = px.bar(
        stage_counts,
        x="Number of Projects",
        y="Milestone Stage",
        orientation="h",
        color="Number of Projects",
        color_continuous_scale=["#93C5FD", "#1E3A8A"],
        text="Number of Projects"
    )
    fig_bar.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Active Projects Count",
        yaxis_title="",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_bar, width="stretch")

with col_chart_right:
    st.subheader("🎯 Portfolio Risk Health")
    risk_df = pd.DataFrame({
        "Status": ["Critical Risk (70-100)", "Watchlist (40-69)", "On Track (1-39)"],
        "Count": [data["high_risk_count"], data["medium_risk_count"], data["low_risk_count"]],
        "Color": ["#EF4444", "#F59E0B", "#10B981"]
    })
    
    fig_donut = go.Figure(data=[go.Pie(
        labels=risk_df["Status"],
        values=risk_df["Count"],
        hole=.55,
        marker_colors=risk_df["Color"],
        textinfo='label+percent',
        insidetextorientation='radial'
    )])
    fig_donut.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False
    )
    st.plotly_chart(fig_donut, width="stretch")

st.divider()

# 4. Interactive Filterable Project Portfolio
st.subheader("📋 National Project Registry & Delay Predictions")

# Sector Pills / Quick Filter
sectors_available = ["All Sectors"] + sorted(list(df_projects["sector"].dropna().unique()))
chosen_sector = st.segmented_control("Filter by Sector / Ministry", sectors_available, default="All Sectors")

f_col1, f_col2, f_col3 = st.columns(3)
with f_col1:
    states = ["All States"] + sorted(list(df_projects["state"].unique()))
    sel_state = st.selectbox("State / Region", states)
with f_col2:
    stages = ["All Stages"] + sorted(list(df_projects["stage"].unique()))
    sel_stage = st.selectbox("Milestone Stage", stages)
with f_col3:
    risk_options = ["All Risk Levels", "Critical High (≥70)", "Watchlist (40-69)", "Low (<40)"]
    sel_risk = st.selectbox("Risk Filter", risk_options)

# Apply filters
filtered_df = df_projects.copy()

if chosen_sector and chosen_sector != "All Sectors":
    filtered_df = filtered_df[filtered_df["sector"] == chosen_sector]
if sel_state != "All States":
    filtered_df = filtered_df[filtered_df["state"] == sel_state]
if sel_stage != "All Stages":
    filtered_df = filtered_df[filtered_df["stage"] == sel_stage]
if sel_risk == "Critical High (≥70)":
    filtered_df = filtered_df[filtered_df["risk_score"] >= 70]
elif sel_risk == "Watchlist (40-69)":
    filtered_df = filtered_df[(filtered_df["risk_score"] >= 40) & (filtered_df["risk_score"] < 70)]
elif sel_risk == "Low (<40)":
    filtered_df = filtered_df[filtered_df["risk_score"] < 40]

st.caption(f"Showing **{len(filtered_df)}** of {len(df_projects)} projects matching filter criteria.")

# Formatted table columns
table_cols = [
    "project_id",
    "project_name",
    "sector",
    "state",
    "district",
    "risk_score",
    "expected_delay_days",
    "compensation_pct",
    "stage"
]

display_table = filtered_df[table_cols].rename(columns={
    "project_id": "Project ID",
    "project_name": "Project Name",
    "sector": "Sector / Ministry",
    "state": "State",
    "district": "District",
    "risk_score": "Risk Score (1-100)",
    "expected_delay_days": "Forecasted Delay (Days)",
    "compensation_pct": "Compensation %",
    "stage": "Current Acquisition Stage"
})

st.dataframe(
    display_table,
    width="stretch",
    height=420,
    column_config={
        "Risk Score (1-100)": st.column_config.ProgressColumn(
            "Risk Score",
            help="Calibrated risk index (1-100)",
            format="%d",
            min_value=0,
            max_value=100
        ),
        "Compensation %": st.column_config.NumberColumn(
            "Disbursed %",
            format="%.1f%%"
        ),
        "Forecasted Delay (Days)": st.column_config.NumberColumn(
            "Exp. Delay",
            format="%d days"
        )
    }
)

st.write("")
st.info("💡 **Next Steps:** Use the sidebar on the left to view **Project Details**, **Risk Rankings**, **SHAP AI Explanations**, **GIS Map**, **Alerts**, or the **DILRMP Digital Land Records Registry**.")

