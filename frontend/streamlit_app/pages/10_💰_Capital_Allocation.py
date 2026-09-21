import os
import sys
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Path setup
PAGE_DIR = os.path.abspath(os.path.dirname(__file__))
STREAMLIT_DIR = os.path.abspath(os.path.join(PAGE_DIR, ".."))
ROOT_DIR = os.path.abspath(os.path.join(PAGE_DIR, "..", "..", ".."))
for p in [PAGE_DIR, STREAMLIT_DIR, ROOT_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

LOGO_PATH = os.path.join(STREAMLIT_DIR, "assets", "logo.png")

try:
    from utils.api_client import client
    from utils.gov_theme import (
        apply_gov_theme,
        hide_default_sidebar_nav,
        render_top_navbar,
        render_gov_footer,
        status_pill
    )
    from auth_guards import require_officer_login
except ImportError:
    from frontend.streamlit_app.utils.api_client import client
    from frontend.streamlit_app.utils.gov_theme import (
        apply_gov_theme,
        hide_default_sidebar_nav,
        render_top_navbar,
        render_gov_footer,
        status_pill
    )
    from frontend.streamlit_app.auth_guards import require_officer_login

st.set_page_config(
    page_title="Capital Allocation & Cost Forecasting — BHOOMI AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_gov_theme()
hide_default_sidebar_nav()
render_top_navbar(current_slug="Capital_Allocation", logo_path=LOGO_PATH)
require_officer_login()

# ── Custom Styling ────────────────────────────────────────────────────────────
st.markdown("""

<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
* { font-family: 'Plus Jakarta Sans', sans-serif; }

.hero-container-green {
background: linear-gradient(135deg, #064E3B 0%, #065F46 50%, #047857 100%);
border-radius: 16px;
padding: 26px 32px;
margin-bottom: 22px;
color: white;
box-shadow: 0 10px 25px -5px rgba(6, 78, 59, 0.25);
border: 1px solid rgba(255, 255, 255, 0.15);
}
.hero-title-green {
font-size: 2.1rem;
font-weight: 800;
letter-spacing: -0.5px;
margin: 0;
background: linear-gradient(90deg, #FFFFFF, #A7F3D0);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
}
.hero-subtitle-green {
font-size: 1.02rem;
color: #D1FAE5;
margin-top: 6px;
max-width: 820px;
line-height: 1.5;
}
.kpi-card {
background: white;
border-radius: 12px;
padding: 18px 20px;
border: 1px solid #E2E8F0;
box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03);
height: 100%;
display: flex;
flex-direction: column;
justify-content: space-between;
}
.kpi-label {
font-size: 0.78rem;
font-weight: 700;
color: #64748B;
text-transform: uppercase;
letter-spacing: 0.5px;
}
.kpi-val {
font-size: 1.75rem;
font-weight: 800;
margin: 6px 0 2px 0;
}
.kpi-sub {
font-size: 0.80rem;
color: #64748B;
}
.overrun-badge-green {
background: #DCFCE7;
color: #166534;
padding: 3px 10px;
border-radius: 12px;
font-weight: 700;
font-size: 0.75rem;
border: 1px solid #BBF7D0;
display: inline-block;
}
.overrun-badge-amber {
background: #FEF3C7;
color: #92400E;
padding: 3px 10px;
border-radius: 12px;
font-weight: 700;
font-size: 0.75rem;
border: 1px solid #FDE68A;
display: inline-block;
}
.overrun-badge-red {
background: #FEE2E2;
color: #991B1B;
padding: 3px 10px;
border-radius: 12px;
font-weight: 700;
font-size: 0.75rem;
border: 1px solid #FECACA;
display: inline-block;
}
.detail-card-box {
background: #F8FAFC;
border-radius: 10px;
padding: 16px 20px;
border: 1px solid #E2E8F0;
margin-top: 10px;
}
</style>

""", unsafe_allow_html=True)

# ── Hero Banner ───────────────────────────────────────────────────────────────
st.markdown("""

<div class="hero-container-green">
<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
<div>
<div style="font-size:0.80rem; font-weight:800; letter-spacing:1.5px; color:#4ADE80; margin-bottom:4px;">
PM GATISHAKTI • NATIONAL CAPITAL EXPENDITURE FORECASTING
</div>
<div class="hero-title-green">💰 AI-Based Capital Allocation & Expenditure Forecasting</div>
<div class="hero-subtitle-green">
Predictive modeling of total final project expenditure and cost overrun based on learned historical patterns of acquisition delay, court litigation, and RFCTLARR compensation progress.
</div>
</div>
<div style="text-align:right;">
<span style="background:rgba(255,255,255,0.18); color:#FFFFFF; padding:6px 14px; border-radius:20px; font-weight:700; font-size:0.80rem; border:1px solid rgba(255,255,255,0.3);">
🤖 Random Forest Regressor • R²: 0.87
</span>
</div>
</div>
</div>

""", unsafe_allow_html=True)

# ── Load Capital Allocation Data ─────────────────────────────────────────────
with st.spinner("Fetching AI capital expenditure predictions..."):
    cap_data = client.get_capital_allocation()
    projects = cap_data.get("projects", [])

if not projects:
    st.error("⚠️ Unable to load Capital Allocation dataset. Please verify backend service.")
    render_gov_footer()
    st.stop()

df_projects = pd.DataFrame(projects)

# ── Filter Controls ──────────────────────────────────────────────────────────
col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns([2, 2, 2, 2, 3])

all_states = ["All States"] + sorted(list(df_projects["state"].dropna().unique()))
with col_f1:
    selected_state = st.selectbox("🗺️ State / UT", all_states)

all_sectors = ["All Sectors"] + sorted(list(df_projects["sector"].dropna().unique()))
with col_f2:
    selected_sector = st.selectbox("🏭 Sector / Ministry", all_sectors)

all_stages = ["All Stages"] + sorted(list(df_projects["stage"].dropna().unique()))
with col_f3:
    selected_stage = st.selectbox("📜 Milestone Stage", all_stages)

tier_options = ["All Overrun Tiers", "🔴 High Overrun (>20%)", "🟡 Moderate Overrun (5–20%)", "🟢 On Budget (≤5%)"]
with col_f4:
    selected_tier = st.selectbox("⚖️ Overrun Risk Tier", tier_options)

with col_f5:
    search_query = st.text_input("🔍 Search Project / ID", placeholder="e.g. Varanasi, High-Speed, PRJ-BI").strip()

# Apply Filters
df_filtered = df_projects.copy()

if selected_state != "All States":
    df_filtered = df_filtered[df_filtered["state"] == selected_state]

if selected_sector != "All Sectors":
    df_filtered = df_filtered[df_filtered["sector"] == selected_sector]

if selected_stage != "All Stages":
    df_filtered = df_filtered[df_filtered["stage"] == selected_stage]

if selected_tier == "🔴 High Overrun (>20%)":
    df_filtered = df_filtered[df_filtered["overrun_tier"] == "High Overrun"]
elif selected_tier == "🟡 Moderate Overrun (5–20%)":
    df_filtered = df_filtered[df_filtered["overrun_tier"] == "Moderate Overrun"]
elif selected_tier == "🟢 On Budget (≤5%)":
    df_filtered = df_filtered[df_filtered["overrun_tier"] == "On Budget"]

if search_query:
    q = search_query.lower()
    df_filtered = df_filtered[
        df_filtered["project_name"].astype(str).str.lower().str.contains(q, regex=False, na=False) |
        df_filtered["project_id"].astype(str).str.lower().str.contains(q, regex=False, na=False)
    ]

# ── Dynamic Aggregate Summary Row (Requirement 3) ───────────────────────────
total_sanctioned_filtered = df_filtered["sanctioned_budget_crores"].sum()
total_estimated_filtered = df_filtered["estimated_total_cost_crores"].sum()
net_overrun_filtered = total_estimated_filtered - total_sanctioned_filtered
overrun_pct_filtered = (net_overrun_filtered / total_sanctioned_filtered * 100.0) if total_sanctioned_filtered > 0 else 0.0

high_count_f = (df_filtered["overrun_tier"] == "High Overrun").sum()
mod_count_f = (df_filtered["overrun_tier"] == "Moderate Overrun").sum()
low_count_f = (df_filtered["overrun_tier"] == "On Budget").sum()

kpi_c1, kpi_c2, kpi_c3, kpi_c4 = st.columns(4)

with kpi_c1:
    st.markdown(f"""

<div class="kpi-card" style="border-top: 4px solid #065F46;">
<div class="kpi-label">🏛️ Total Sanctioned Budget</div>
<div class="kpi-val" style="color:#0F172A;">₹{total_sanctioned_filtered:,.2f} Cr</div>
<div class="kpi-sub">Baseline government allocation for {len(df_filtered)} projects</div>
</div>

""", unsafe_allow_html=True)

with kpi_c2:
    st.markdown(f"""

<div class="kpi-card" style="border-top: 4px solid #059669;">
<div class="kpi-label">🤖 Total AI-Estimated National Expenditure</div>
<div class="kpi-val" style="color:#065F46;">₹{total_estimated_filtered:,.2f} Cr</div>
<div class="kpi-sub">Realistic predicted final expenditure footprint</div>
</div>

""", unsafe_allow_html=True)

with kpi_c3:
    overrun_color = "#EF4444" if overrun_pct_filtered > 15 else ("#F59E0B" if overrun_pct_filtered > 5 else "#10B981")
    st.markdown(f"""

<div class="kpi-card" style="border-top: 4px solid {overrun_color};">
<div class="kpi-label">📈 Estimated Overrun Gap</div>
<div class="kpi-val" style="color:{overrun_color};">+₹{net_overrun_filtered:,.2f} Cr</div>
<div class="kpi-sub"><strong>+{overrun_pct_filtered:.2f}%</strong> estimated budget deviation</div>
</div>

""", unsafe_allow_html=True)

with kpi_c4:
    st.markdown(f"""

<div class="kpi-card" style="border-top: 4px solid #F59E0B;">
<div class="kpi-label">⚠️ Overrun Risk Distribution</div>
<div style="margin: 8px 0 2px 0; font-size:1.1rem; font-weight:700;">
<span style="color:#EF4444;">🔴 {high_count_f} High</span> •
<span style="color:#F59E0B;">🟡 {mod_count_f} Mod</span> •
<span style="color:#10B981;">🟢 {low_count_f} Low</span>
</div>
<div class="kpi-sub">{len(df_filtered)} projects in active view</div>
</div>

""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Visual Analytics Comparison ──────────────────────────────────────────────
col_chart_left, col_chart_right = st.columns([3, 2])

with col_chart_left:
    st.subheader("📊 Sanctioned Budget vs AI-Estimated Final Cost by Sector")
    if not df_filtered.empty:
        sector_agg = df_filtered.groupby("sector")[["sanctioned_budget_crores", "estimated_total_cost_crores"]].sum().reset_index()
        fig_sec = go.Figure()
        fig_sec.add_trace(go.Bar(
            name="Sanctioned Budget",
            x=sector_agg["sector"],
            y=sector_agg["sanctioned_budget_crores"],
            marker_color="#94A3B8"
        ))
        fig_sec.add_trace(go.Bar(
            name="AI-Estimated Cost",
            x=sector_agg["sector"],
            y=sector_agg["estimated_total_cost_crores"],
            marker_color="#065F46"
        ))
        fig_sec.update_layout(
            barmode="group",
            height=290,
            margin=dict(l=10, r=10, t=20, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis_title="₹ Crores"
        )
        st.plotly_chart(fig_sec, use_container_width=True)
    else:
        st.info("No projects match the selected filters.")

with col_chart_right:
    st.subheader("🎯 Overrun Severity Breakdown")
    if not df_filtered.empty:
        tier_counts = df_filtered["overrun_tier"].value_counts().reset_index()
        tier_counts.columns = ["Tier", "Count"]
        color_map = {"High Overrun": "#EF4444", "Moderate Overrun": "#F59E0B", "On Budget": "#10B981"}
        fig_pie = px.pie(
            tier_counts,
            names="Tier",
            values="Count",
            color="Tier",
            color_discrete_map=color_map,
            hole=0.45
        )
        fig_pie.update_layout(
            height=290,
            margin=dict(l=10, r=10, t=20, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# ── Per-Project Breakdown Table (Requirement 2) ──────────────────────────────
st.subheader(f"📋 Per-Project Capital Allocation & Overrun Estimates ({len(df_filtered)} Projects)")
st.caption("Side-by-side comparison of baseline government sanction against AI predictive expenditure modeling.")

if df_filtered.empty:
    st.warning("No projects found matching the active filter criteria. Try broadening your filter selection.")
else:
    # Build clean display table
    display_rows = []
    for _, row in df_filtered.iterrows():
        p_id = row["project_id"]
        p_name = row["project_name"]
        budget = row["sanctioned_budget_crores"]
        est_cost = row["estimated_total_cost_crores"]
        overrun_cr = row["estimated_overrun_crores"]
        overrun_pct = row["estimated_overrun_pct"]
        tier = row["overrun_tier"]
        
        if overrun_pct > 20.0:
            badge_html = f'<span class="overrun-badge-red">🔴 +₹{overrun_cr:,.1f} Cr (+{overrun_pct:.1f}%)</span>'
        elif overrun_pct > 5.0:
            badge_html = f'<span class="overrun-badge-amber">🟡 +₹{overrun_cr:,.1f} Cr (+{overrun_pct:.1f}%)</span>'
        else:
            badge_html = f'<span class="overrun-badge-green">🟢 +₹{overrun_cr:,.1f} Cr (+{overrun_pct:.1f}%)</span>'
            
        display_rows.append({
            "Project ID": p_id,
            "Project Name": p_name,
            "State": row["state"],
            "Sector": row["sector"],
            "Acquisition Stage": row["stage"],
            "Total Budget (Sanctioned)": f"₹{budget:,.2f} Cr",
            "AI-Estimated Total Cost": f"₹{est_cost:,.2f} Cr",
            "Estimated Overrun": badge_html,
            "_raw_budget": budget,
            "_raw_est": est_cost,
            "_raw_overrun": overrun_cr,
            "_raw_pct": overrun_pct,
            "_summary": row.get("explanation_summary", ""),
            "_factors": row.get("top_driving_factors", [])
        })

    # Render interactive table with HTML badge formatting
    table_df = pd.DataFrame(display_rows)
    table_cols = [
        "Project ID", "Project Name", "State", "Sector", "Acquisition Stage",
        "Total Budget (Sanctioned)", "AI-Estimated Total Cost", "Estimated Overrun"
    ]
    
    st.write(
        table_df[table_cols].to_html(escape=False, index=False),
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Per-Project Expandable Detail View (Requirement 2) ───────────────────
    st.markdown("### 🔍 Project Cost Driver Deep-Dive")
    st.caption("Select a project below to inspect the top factors pushing its estimated total expenditure:")
    
    project_selector = st.selectbox(
        "Choose project for root-cause cost breakdown:",
        options=list(df_filtered["project_id"] + " — " + df_filtered["project_name"]),
        key="cost_proj_selector"
    )
    
    selected_id = project_selector.split(" — ")[0]
    selected_proj = df_filtered[df_filtered["project_id"] == selected_id].iloc[0]
    
    with st.container():
        p_b = selected_proj["sanctioned_budget_crores"]
        p_est = selected_proj["estimated_total_cost_crores"]
        p_ov = selected_proj["estimated_overrun_crores"]
        p_ov_pct = selected_proj["estimated_overrun_pct"]
        
        st.markdown(f"""

<div class="detail-card-box">
<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
<div>
<h3 style="margin:0 0 4px 0; color:#065F46; font-size:1.3rem;">{selected_proj['project_name']} ({selected_proj['project_id']})</h3>
<div style="font-size:0.85rem; color:#64748B;">📍 {selected_proj['state']} • {selected_proj['sector']} • 📜 {selected_proj['stage']}</div>
</div>
<div>
<span style="background:{'#FEE2E2' if p_ov_pct>20 else ('#FEF3C7' if p_ov_pct>5 else '#DCFCE7')}; color:{'#991B1B' if p_ov_pct>20 else ('#92400E' if p_ov_pct>5 else '#166534')}; font-weight:800; padding:6px 16px; border-radius:20px; font-size:0.85rem;">
{selected_proj['overrun_tier']} ({'+' if p_ov_pct>0 else ''}{p_ov_pct:.1f}%)
</span>
</div>
</div>
<div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:14px; margin-bottom:16px;">
<div style="background:white; padding:12px 16px; border-radius:8px; border:1px solid #CBD5E1;">
<div style="font-size:0.75rem; color:#64748B; font-weight:600;">SANCTIONED BUDGET</div>
<div style="font-size:1.35rem; font-weight:800; color:#0F172A;">₹{p_b:,.2f} Cr</div>
</div>
<div style="background:white; padding:12px 16px; border-radius:8px; border:1px solid #CBD5E1;">
<div style="font-size:0.75rem; color:#065F46; font-weight:600;">AI-ESTIMATED TOTAL COST</div>
<div style="font-size:1.35rem; font-weight:800; color:#065F46;">₹{p_est:,.2f} Cr</div>
</div>
<div style="background:white; padding:12px 16px; border-radius:8px; border:1px solid #CBD5E1;">
<div style="font-size:0.75rem; color:#EF4444; font-weight:600;">ESTIMATED OVERRUN</div>
<div style="font-size:1.35rem; font-weight:800; color:{'#EF4444' if p_ov_pct>15 else '#D97706'};">+₹{p_ov:,.2f} Cr (+{p_ov_pct:.1f}%)</div>
</div>
</div>
<div style="background:#ECFDF5; border-left:4px solid #059669; padding:12px 16px; border-radius:6px; margin-bottom:14px;">
<strong style="color:#065F46;">🧠 AI Cost Attribution Summary:</strong> {selected_proj['explanation_summary']}
</div>
</div>

""", unsafe_allow_html=True)
        
        st.markdown("#### 📌 Key Drivers Pushing Estimated Expenditure:")
        factors = selected_proj.get("top_driving_factors", [])
        if isinstance(factors, list) and factors:
            for idx, factor in enumerate(factors, start=1):
                if isinstance(factor, dict):
                    f_name = factor.get("factor", "")
                    f_imp = factor.get("impact", "")
                    f_bdg = factor.get("badge", "Cost Driver")
                    st.markdown(f"**{idx}. {f_name}** (`{f_bdg}`): {f_imp}")
                else:
                    st.markdown(f"**{idx}.** {str(factor)}")
        else:
            st.info("No significant risk factors flagged; project capital allocation is progressing as planned.")

# ── Statutory Prediction Disclaimer ──────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""

<div style="background: #F1F5F9; border-radius: 10px; padding: 12px 18px; border: 1px solid #CBD5E1; font-size: 0.78rem; color: #475569;">
⚠️ <strong>Statutory Prediction Notice:</strong> All figures labeled <em>AI-Estimated Total Cost</em> and <em>Estimated Overrun</em> are predictive econometric estimates produced by the BHOOMI AI Random Forest Regressor trained on historical MoSPI infrastructure cost escalation patterns. These figures are advisory planning benchmarks and do not constitute certified CAG audit disbursements or approved revised budget sanctions.
</div>

""", unsafe_allow_html=True)

render_gov_footer()

