import sys
import os
import streamlit as st
from datetime import date, timedelta

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

st.set_page_config(page_title="Project Simulator — Bhoomi AI", page_icon="➕", layout="wide")

# Render Bhoomi AI logo & sidebar
render_sidebar_brand()

st.title("➕ Project Risk Simulator & Ingestion Sandbox")
st.markdown("""
Run **'What-If' scenarios** to observe how accelerating compensation disbursements, resolving court disputes, or improving land record digitalization reduces delay forecasts.
""")

if not client.check_health():
    st.error("⚠️ Backend API is offline. Please start backend via `python run_backend.py`.")
    st.stop()

STAGES = [
    "Section 4 - Preliminary Notification",
    "Social Impact Assessment (SIA)",
    "Section 11 Notification",
    "Section 19 Declaration (R&R Scheme)",
    "Award of Compensation (Section 23/30)",
    "Possession & Physical Transfer"
]

STATES = [
    "Andhra Pradesh", "Maharashtra", "Gujarat", "Uttar Pradesh", "Tamil Nadu", "Karnataka",
    "Odisha", "Rajasthan", "West Bengal", "Madhya Pradesh", "Bihar", "Assam", "Manipur"
]

SECTORS = [
    "Road Transport and Highways",
    "Railways",
    "Civil Aviation",
    "Petroleum",
    "Water Resources",
    "Health and Family Welfare",
    "Higher Education"
]

tab_sim, tab_ingest = st.tabs(["🧪 Interactive 'What-If' Delay Simulator", "💾 Save New Project to National Registry"])

with tab_sim:
    st.subheader("⚡ Live Delay Sensitivity Playground")
    st.caption("Adjust the sliders below to see the AI model update risk score and expected delay instantly.")

    s_col1, s_col2 = st.columns(2)
    with s_col1:
        sim_state = st.selectbox("State of Project", STATES, index=0, key="sim_state")
        sim_stage = st.selectbox("Current Milestone Stage", STAGES, index=3, key="sim_stage")
        sim_comp = st.slider("Compensation Disbursed (%)", 0.0, 100.0, 30.0, step=1.0, key="sim_comp")
        sim_legal = st.radio("Court Injunction / Legal Dispute", ["No Legal Dispute", "Active High Court Stay Order"], key="sim_legal")

    with s_col2:
        sim_sector = st.selectbox("Sector / Ministry", SECTORS, index=0, key="sim_sector")
        sim_families = st.slider("Displaced / Affected Families", 10, 5000, 850, step=50, key="sim_families")
        sim_budget = st.number_input("Project Budget (₹ Crores)", 50.0, 50000.0, 1200.0, step=50.0, key="sim_budget")
        sim_rr = st.selectbox("R&R Scheme Execution", ["Pending", "In Progress", "Completed"], key="sim_rr")

    # Construct simulation payload
    is_legal = 1 if "Active" in sim_legal else 0
    sim_payload = {
        "project_name": f"Simulation Corridor ({sim_state})",
        "state": sim_state,
        "district": "Capital Region",
        "stage": sim_stage,
        "start_date": "2024-01-01",
        "target_completion_date": "2025-06-01",
        "planned_duration_days": 517,
        "compensation_pct": float(sim_comp),
        "legal_case": is_legal,
        "rr_status": sim_rr,
        "affected_families": int(sim_families),
        "budget_crores": float(sim_budget),
        "latitude": 17.5,
        "longitude": 78.5,
        "sector": sim_sector
    }

    # Run instant local prediction via backend
    try:
        from backend.app.api.routes import run_project_prediction
        from backend.app.ml.risk_scoring import calculate_calibrated_risk_score
        
        sim_pred = run_project_prediction(sim_payload)
        sim_risk = calculate_calibrated_risk_score(
            delay_prob=sim_pred["delay_probability"],
            expected_delay_days=sim_pred["expected_delay_days"],
            legal_case=is_legal,
            compensation_pct=float(sim_comp),
            stage=sim_stage,
            affected_families=int(sim_families)
        )

        st.markdown("---")
        st.subheader("🎯 Real-Time Simulated Output")
        
        r1, r2, r3 = st.columns(3)
        with r1:
            col = sim_risk["color_code"]
            st.metric("Forecasted Risk Score", f"{sim_risk['risk_score']} / 100")
            st.markdown(f"**Risk Level:** <span style='color: {col}; font-weight: bold; font-size: 1.1rem;'>{sim_risk['risk_category'].upper()}</span>", unsafe_allow_html=True)
        with r2:
            st.metric("Forecasted Delay", f"{sim_pred['expected_delay_days']} Days")
            st.caption(f"Status: **{sim_pred['delay_label']}** (Certainty: {sim_pred['confidence_score']}%)")
        with r3:
            st.metric("Delay Probability", f"{sim_pred['delay_probability'] * 100:.1f}%")
            st.caption(f"Based on {sim_sector} benchmarks")

        st.info(f"💡 **AI Recommendation:** {sim_risk['action_recommendation']}")

    except Exception as e:
        st.warning(f"Live preview calculation: {e}")

with tab_ingest:
    st.subheader("💾 Ingest & Register New Infrastructure Project")
    with st.form("new_project_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            in_name = st.text_input("Project Name", value="Amaravati High-Speed Freight Link")
            in_sector = st.selectbox("Sector / Ministry", SECTORS, index=1)
        with c2:
            in_state = st.selectbox("State", STATES, index=0)
            in_district = st.text_input("District", value="Guntur")
        with c3:
            in_stage = st.selectbox("Current Stage", STAGES, index=2)
            in_budget = st.number_input("Budget (₹ Crores)", min_value=1.0, value=750.0)

        c4, c5, c6 = st.columns(3)
        with c4:
            in_start = st.date_input("Start Date", value=date.today() - timedelta(days=90))
            in_target = st.date_input("Target Date", value=date.today() + timedelta(days=360))
        with c5:
            in_comp = st.slider("Compensation Disbursal %", 0.0, 100.0, 42.0)
            in_legal = st.selectbox("Litigation", ["No Litigation", "Active Court Litigation"])
        with c6:
            in_rr = st.selectbox("R&R Scheme", ["Pending", "In Progress", "Completed"])
            in_fam = st.number_input("Affected Families", min_value=1, value=650)

        submitted = st.form_submit_button("🚀 Submit to National Registry")

    if submitted:
        planned_dur = max(30, (in_target - in_start).days)
        payload = {
            "project_name": in_name,
            "sector": in_sector,
            "state": in_state,
            "district": in_district,
            "stage": in_stage,
            "start_date": in_start.strftime("%Y-%m-%d"),
            "target_completion_date": in_target.strftime("%Y-%m-%d"),
            "planned_duration_days": planned_dur,
            "compensation_pct": float(in_comp),
            "legal_case": 1 if "Active" in in_legal else 0,
            "rr_status": in_rr,
            "affected_families": int(in_fam),
            "budget_crores": float(in_budget),
            "latitude": 16.4,
            "longitude": 80.5
        }
        try:
            res = client.create_project(payload)
            st.success(f"🎉 Project saved to database! Generated ID: **{res['project_id']}** (Forecasted Delay: {res.get('delay_days')} days)")
        except Exception as e:
            st.error(f"Failed to submit: {e}")
