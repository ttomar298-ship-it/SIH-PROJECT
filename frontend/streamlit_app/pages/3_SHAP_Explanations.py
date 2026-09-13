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

st.set_page_config(page_title="AI Root Cause Analysis — Bhoomi AI", page_icon="🧠", layout="wide")

# Render Bhoomi AI logo & sidebar
render_sidebar_brand()

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .verdict-box {
        background: #F8FAFC;
        border-radius: 12px;
        padding: 20px 24px;
        border-left: 6px solid #3B82F6;
        margin-bottom: 24px;
    }
    .factor-card {
        background: white;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 10px;
        border: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧠 Explainable AI: Root-Cause Factor Analysis")
st.markdown("Clear, transparent explanation of **why** the AI model flagged a specific project for delay, powered by TreeSHAP feature attributions.")

if not client.check_health():
    st.error("⚠️ Backend API is offline. Please start backend via `python run_backend.py`.")
    st.stop()

# Fetch project list
try:
    projects = client.get_projects()
    projects_sorted = sorted(projects, key=lambda x: x["project_name"])
    proj_map = {f"{p['project_name']} ({p['district']}, {p['state']}) — [{p['project_id']}]": p["project_id"] for p in projects_sorted}
except Exception as e:
    st.error(f"Failed to fetch projects: {e}")
    st.stop()

chosen_label = st.selectbox("Select Project to Diagnose", list(proj_map.keys()))
chosen_id = proj_map[chosen_label]

if chosen_id:
    with st.spinner("Computing TreeSHAP root-cause contributions..."):
        risk_data = client.get_risk_score(chosen_id)
        pred_data = client.get_prediction(chosen_id)
        factors = risk_data["top_factors"]

    # Header summary
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Project ID", chosen_id)
    with c2:
        st.metric("Calibrated Risk", f"{risk_data['risk_score']} / 100", delta=risk_data['risk_category'], delta_color="inverse" if risk_data['risk_score'] > 60 else "normal")
    with c3:
        st.metric("Expected Delay", f"{pred_data['expected_delay_days']} Days", delta=pred_data['delay_label'], delta_color="inverse" if pred_data['delay_flag'] == 1 else "normal")
    with c4:
        st.metric("AI Confidence", f"{pred_data['confidence_score']}%")

    st.divider()

    # Plain-English Executive Verdict Box
    top_pos = [f for f in factors if f["shap_value"] > 0]
    top_neg = [f for f in factors if f["shap_value"] <= 0]
    
    reasons_html = "".join([f"<li>🔴 <b>{f['label']}:</b> {f['description']} <i>(+{f['shap_value']:.4f} delay impact)</i></li>" for f in top_pos[:3]])
    if top_neg:
        safeguards_html = "".join([f"<li>🟢 <b>{f['label']}:</b> {f['description']} <i>({f['shap_value']:.4f} risk mitigation)</i></li>" for f in top_neg[:2]])
    else:
        safeguards_html = "<li>None identified — project is heavily constrained across all parameters.</li>"

    st.markdown(f"""
    <div class="verdict-box">
        <h3 style="margin: 0 0 10px 0; color: #0F172A; font-size: 1.25rem;">🔍 AI Executive Diagnostic Summary</h3>
        <p style="color: #475569; font-size: 0.95rem; margin-bottom: 12px;">
            The machine learning model evaluated this project against 250+ national infrastructure benchmarks.
        </p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div>
                <h4 style="color: #DC2626; margin: 0 0 6px 0; font-size: 1rem;">Primary Drivers Increasing Delay:</h4>
                <ul style="padding-left: 20px; color: #334155; margin: 0; font-size: 0.9rem;">
                    {reasons_html}
                </ul>
            </div>
            <div>
                <h4 style="color: #059669; margin: 0 0 6px 0; font-size: 1rem;">Mitigating Factors Pulling Towards Schedule:</h4>
                <ul style="padding-left: 20px; color: #334155; margin: 0; font-size: 0.9rem;">
                    {safeguards_html}
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Interactive Plotly Waterfall / Horizontal Bar Chart
    st.subheader("📊 TreeSHAP Feature Attribution Chart")
    st.caption("Red bars indicate features that push the project towards delay; green bars indicate protective factors.")

    df_factors = pd.DataFrame(factors)
    df_factors["Effect"] = df_factors["impact"].map({
        "increases_delay": "Increases Delay Risk (+)",
        "reduces_delay": "Reduces Delay Risk (-)"
    })
    
    fig_shap = px.bar(
        df_factors,
        x="shap_value",
        y="label",
        orientation="h",
        color="Effect",
        color_discrete_map={
            "Increases Delay Risk (+)": "#EF4444",
            "Reduces Delay Risk (-)": "#10B981"
        },
        hover_data=["description", "raw_value"],
        text="shap_value"
    )
    fig_shap.update_layout(
        xaxis_title="SHAP Attribution (Impact on Delay Probability)",
        yaxis_title="",
        height=380,
        margin=dict(l=10, r=10, t=20, b=10)
    )
    st.plotly_chart(fig_shap, width="stretch")

    st.divider()

    # Detailed Root Cause Cards
    st.subheader("📋 Detailed Breakdown by Constraint")
    for f in factors:
        is_risky = f["shap_value"] > 0
        icon = "🔴" if is_risky else "🟢"
        color = "#DC2626" if is_risky else "#059669"
        impact_txt = f"+{f['shap_value']:.4f} (Heightened Delay Probability)" if is_risky else f"{f['shap_value']:.4f} (Mitigates Delay Risk)"
        
        with st.expander(f"{icon} {f['label']} — {impact_txt}"):
            c_e1, c_e2 = st.columns([3, 1])
            with c_e1:
                st.markdown(f"**Diagnostic Observation:** {f['description']}")
                st.markdown(f"**Actual Measured Metric:** `{f['raw_value']}`")
            with c_e2:
                st.metric("SHAP Contribution", f"{f['shap_value']:.4f}")

    # Risk Score Component Formula
    if risk_data.get("components"):
        st.divider()
        st.subheader("⚙️ Calibrated Risk Score Composition")
        comp = risk_data["components"]
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("1. Model Probability Component", f"{comp['probability_component']} / 50")
            st.caption("Derived from RF Classifier delay probability")
        with col_b:
            st.metric("2. Delay Severity Component", f"{comp['severity_component']} / 30")
            st.caption("Derived from RF Regressor expected delay days")
        with col_c:
            st.metric("3. Contextual Multipliers", f"{comp['context_component']} / 20")
            st.caption("Litigation, low compensation, low DILRMP land digitization")
