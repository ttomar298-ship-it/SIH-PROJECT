import sys
import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Ensure application directory and root are in sys.path
PAGE_DIR = os.path.abspath(os.path.dirname(__file__))
STREAMLIT_DIR = os.path.abspath(os.path.join(PAGE_DIR, ".."))
ROOT_DIR = os.path.abspath(os.path.join(PAGE_DIR, "..", "..", ".."))
for p in [PAGE_DIR, STREAMLIT_DIR, ROOT_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from utils.api_client import client
    from utils.auth import render_sidebar_brand
except ImportError:
    from frontend.streamlit_app.utils.api_client import client
    from frontend.streamlit_app.utils.auth import render_sidebar_brand

st.set_page_config(page_title="Risk Leaderboard — Bhoomi AI", page_icon="🏆", layout="wide")

# Render Bhoomi AI logo & sidebar
render_sidebar_brand()

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
</style>
""", unsafe_allow_html=True)

import logging
logger = logging.getLogger(__name__)

st.title("🏆 National Project Risk Ranking & Criticality Leaderboard")
st.markdown("Comprehensive prioritization matrix ranking infrastructure projects by land acquisition bottleneck severity.")

if not client.check_health():
    st.error("⚠️ Backend API is offline. Please start backend via `python run_backend.py`.")
    st.stop()

try:
    dashboard_data = client.get_dashboard_data()
    projects = dashboard_data.get("projects", [])
    df = pd.DataFrame(projects)
except Exception as exc:
    logger.error("Failed to load risk rankings", exc_info=True)
    st.error("Unable to load risk ranking leaderboard. Please ensure the backend service is operational.")
    st.stop()

if df.empty:
    st.info("No project records available to generate leaderboard.")
    st.stop()

# Controls & Filters
c_slider, c_state, c_sector = st.columns([2, 1, 1])
with c_slider:
    min_score = st.slider("Filter by Minimum Calibrated Risk Score", min_value=1, max_value=100, value=50)
with c_state:
    all_states = ["All States"] + sorted(list(df["state"].dropna().unique()))
    chosen_state = st.selectbox("State / UT", all_states)
with c_sector:
    all_sectors = ["All Sectors"] + sorted(list(df["sector"].dropna().unique()))
    chosen_sector = st.selectbox("Sector / Ministry", all_sectors)

# Filter
filtered = df[df["risk_score"] >= min_score]
if chosen_state != "All States":
    filtered = filtered[filtered["state"] == chosen_state]
if chosen_sector != "All Sectors":
    filtered = filtered[filtered["sector"] == chosen_sector]

# Sorted High -> Low
filtered = filtered.sort_values(by="risk_score", ascending=False).reset_index(drop=True)
filtered["Rank"] = filtered.index + 1

st.divider()

# High-level summary metrics
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Total Filtered Projects", len(filtered))
with m2:
    st.metric("Highest Risk Score", f"{filtered['risk_score'].max() if len(filtered) > 0 else 0} / 100")
with m3:
    critical_in_filter = len(filtered[filtered["risk_score"] >= 70])
    st.metric("Critical Projects (Score ≥ 70)", critical_in_filter, delta="Action Required", delta_color="inverse")
with m4:
    max_delay = filtered['expected_delay_days'].max() if len(filtered) > 0 else 0
    st.metric("Maximum Forecasted Delay", f"{max_delay:.0f} Days")

# Top 10 Critical Projects Bar Chart
if len(filtered) > 0:
    st.subheader("🔥 Top 10 Most Vulnerable Infrastructure Projects")
    top_10 = filtered.head(10)
    fig_top = px.bar(
        top_10,
        x="risk_score",
        y="project_name",
        orientation="h",
        color="risk_score",
        color_continuous_scale="Reds",
        hover_data=["project_id", "state", "stage", "expected_delay_days", "sector"],
        text="risk_score"
    )
    fig_top.update_layout(yaxis=dict(autorange="reversed"), height=380, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="Risk Score (1-100)", yaxis_title="")
    st.plotly_chart(fig_top, width="stretch")

# Full Leaderboard Table
st.subheader("📋 Prioritized Project Leaderboard")

display_cols = [
    "Rank",
    "project_id",
    "project_name",
    "sector",
    "state",
    "district",
    "risk_score",
    "expected_delay_days",
    "compensation_pct",
    "legal_case"
]

formatted_table = filtered[display_cols].rename(columns={
    "project_id": "Project ID",
    "project_name": "Project Name",
    "sector": "Sector",
    "state": "State",
    "district": "District",
    "risk_score": "Risk Score",
    "expected_delay_days": "Forecasted Delay",
    "compensation_pct": "Compensation %",
    "legal_case": "Litigation"
})

st.dataframe(
    formatted_table,
    width="stretch",
    height=450,
    column_config={
        "Risk Score": st.column_config.ProgressColumn(
            "Risk Score (1-100)",
            format="%d",
            min_value=0,
            max_value=100
        ),
        "Compensation %": st.column_config.NumberColumn(
            "Compensation",
            format="%.1f%%"
        ),
        "Forecasted Delay": st.column_config.NumberColumn(
            "Delay (Days)",
            format="%d days"
        ),
        "Litigation": st.column_config.CheckboxColumn(
            "Court Case Active",
            help="Active High Court litigation flag"
        )
    }
)
