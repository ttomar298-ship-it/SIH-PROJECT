import sys
import os
import streamlit as st
import pandas as pd

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

st.set_page_config(page_title="Project Details — Bhoomi AI", page_icon="📊", layout="wide")

# Render Bhoomi AI logo & sidebar
render_sidebar_brand()

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .detail-hero {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border-radius: 14px;
        padding: 24px;
        color: white;
        margin-bottom: 20px;
        border: 1px solid #334155;
    }
    .metric-panel {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px 20px;
    }
    .stage-done {
        background: #D1FAE5;
        color: #065F46;
        border-left: 4px solid #10B981;
        padding: 10px 14px;
        border-radius: 6px;
        margin-bottom: 8px;
        font-size: 0.9rem;
    }
    .stage-active {
        background: #FEF3C7;
        color: #92400E;
        border-left: 4px solid #F59E0B;
        padding: 10px 14px;
        border-radius: 6px;
        margin-bottom: 8px;
        font-weight: 700;
        font-size: 0.95rem;
    }
    .stage-pending {
        background: #F1F5F9;
        color: #64748B;
        border-left: 4px solid #CBD5E1;
        padding: 10px 14px;
        border-radius: 6px;
        margin-bottom: 8px;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Project Deep-Dive & Timeline Inspection")
st.markdown("Detailed breakdown of statutory land acquisition stages, compensation disbursements, court disputes, and AI delay forecasts.")

if not client.check_health():
    st.error("⚠️ Backend API is offline. Please start backend via `python run_backend.py`.")
    st.stop()

# Load project list for dropdown
try:
    all_projects = client.get_projects()
    # Sort projects alphabetically
    all_projects_sorted = sorted(all_projects, key=lambda x: x["project_name"])
    project_options = {f"{p['project_name']} ({p['district']}, {p['state']}) — [{p['project_id']}]": p["project_id"] for p in all_projects_sorted}
except Exception as e:
    st.error(f"Failed to load projects: {e}")
    st.stop()

selected_label = st.selectbox("Select Project to Inspect", list(project_options.keys()))
selected_id = project_options[selected_label]

if selected_id:
    with st.spinner("Analyzing project parameters..."):
        p = client.get_project(selected_id)
        pred = client.get_prediction(selected_id)
        risk = client.get_risk_score(selected_id)

    # Hero card
    risk_col = risk['color_code']
    st.markdown(f"""
    <div class="detail-hero">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="background: #3B82F6; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: bold;">
                    {p.get('sector', 'Infrastructure')}
                </span>
                <h2 style="margin: 8px 0 4px 0; color: white; font-size: 1.7rem;">{p['project_name']}</h2>
                <p style="margin: 0; color: #94A3B8; font-size: 0.95rem;">
                    📍 {p['district']}, {p['state']} • Project ID: <code>{p['project_id']}</code> • State Land Records Digitalization: <b>{p.get('clr_completed_pct', 97.5)}%</b>
                </p>
            </div>
            <div style="text-align: right; background: rgba(255,255,255,0.08); padding: 14px 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.15);">
                <div style="font-size: 0.8rem; color: #94A3B8; text-transform: uppercase;">Calibrated Risk</div>
                <div style="font-size: 2.2rem; font-weight: 800; color: {risk_col};">{risk['risk_score']} <span style="font-size: 1rem; color: #94A3B8;">/100</span></div>
                <div style="font-size: 0.85rem; font-weight: bold; color: {risk_col};">{risk['risk_category'].upper()} RISK</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Summary Row
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Forecasted Delay", f"{pred['expected_delay_days']} Days", delta="Delayed" if pred['delay_flag'] == 1 else "On Schedule", delta_color="inverse" if pred['delay_flag'] == 1 else "normal")
    with k2:
        st.metric("Model Confidence", f"{pred['confidence_score']}%", help="AI model prediction certainty")
    with k3:
        st.metric("Project Budget", f"₹ {p['budget_crores']} Cr", delta=f"{p.get('cost_overrun_pct', 0.0)}% Overrun" if p.get('cost_overrun_pct', 0) > 0 else "On Budget", delta_color="inverse")
    with k4:
        st.metric("Displaced Families", f"{p['affected_families']} Families", help="Families requiring resettlement & compensation")

    st.divider()

    # Timeline & Progress Column
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.subheader("🏁 Statutory Land Acquisition Pipeline (RFCTLARR Act 2013)")
        
        STAGES = [
            ("Section 4 - Preliminary Notification", "Publication of intended acquisition & boundary survey"),
            ("Social Impact Assessment (SIA)", "Public hearings, appraisal of livelihood impact & affected families"),
            ("Section 11 Notification", "Preliminary notification of land required for public purpose"),
            ("Section 19 Declaration (R&R Scheme)", "Declaration of Resettlement & Rehabilitation scheme approval"),
            ("Award of Compensation (Section 23/30)", "Determination & disbursal of compensation to land owners"),
            ("Possession & Physical Transfer", "Final transfer of land right-of-way to project agency")
        ]

        current_stage = p["stage"]
        current_idx = [s[0] for s in STAGES].index(current_stage) if current_stage in [s[0] for s in STAGES] else 0

        st.progress((current_idx + 1) / len(STAGES))

        for i, (stg_name, stg_desc) in enumerate(STAGES):
            if i < current_idx:
                st.markdown(f"""
                <div class="stage-done">
                    ✅ <b>Stage {i+1}: {stg_name}</b> (Completed)<br>
                    <span style="font-size: 0.8rem; color: #047857;">{stg_desc}</span>
                </div>
                """, unsafe_allow_html=True)
            elif i == current_idx:
                st.markdown(f"""
                <div class="stage-active">
                    🔄 <b>Stage {i+1}: {stg_name}</b> (Active Stage)<br>
                    <span style="font-size: 0.8rem; color: #78350F;">{stg_desc}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="stage-pending">
                    ⚪ <b>Stage {i+1}: {stg_name}</b> (Upcoming)<br>
                    <span style="font-size: 0.8rem; color: #64748B;">{stg_desc}</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("💡 Recommended Action Plan for Competent Authority (CALA)")
        st.info(f"**Action Plan:** {risk['action_recommendation']}")

    with col_right:
        st.subheader("📈 Financial & Litigation Status")
        
        # Compensation Disbursal
        comp = p["compensation_pct"]
        st.write(f"**Compensation Disbursal Progress:** `{comp}%`")
        st.progress(min(1.0, max(0.0, comp / 100.0)))
        if comp < 35.0:
            st.error("🚨 **Critical Warning:** Compensation disbursement is below 35%. Severe risk of landowner protests and court stay.")
        elif comp < 70.0:
            st.warning("⚠️ **Moderate Progress:** Compensation ongoing. Accelerated disbursement needed before Section 23 Award.")
        else:
            st.success("✅ **Healthy Progress:** Over 70% compensation disbursed.")

        st.markdown("---")

        # Court Litigation
        st.write("**Legal Dispute / High Court Injunction Status:**")
        if p["legal_case"] == 1:
            st.error("🚨 **ACTIVE COURT CASE / STAY ORDER FILED**\n\nLand acquisition is held up in civil court or High Court tribunal. Physical transfer cannot proceed.")
        else:
            st.success("✅ **NO ACTIVE LITIGATION**\n\nClear legal title with no pending High Court stay orders.")

        st.markdown("---")

        # R&R Status
        st.write(f"**Resettlement & Rehabilitation (R&R):** `{p['rr_status']}`")
        if p["rr_status"] == "Pending":
            st.warning("⚠️ Resettlement colony site allotment or direct assistance pending.")
        elif p["rr_status"] == "In Progress":
            st.info("ℹ️ R&R scheme verification underway.")
        else:
            st.success("✅ R&R scheme fully executed.")

        # Key Project Dates
        st.markdown("---")
        st.markdown(f"""
        - 📅 **Start Date:** `{p['start_date']}`
        - 🎯 **Target Completion:** `{p['target_completion_date']}`
        - ⏱️ **Anticipated / Actual:** `{p.get('actual_or_projected_date', 'N/A')}`
        - ⏳ **Total Scheduled Duration:** `{p['planned_duration_days']} days`
        """)
