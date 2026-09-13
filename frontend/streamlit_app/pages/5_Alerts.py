import sys
import os
import streamlit as st

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

st.set_page_config(page_title="Alerts Hub — Bhoomi AI", page_icon="🚨", layout="wide")

# Render Bhoomi AI logo & sidebar
render_sidebar_brand()

st.title("🚨 Priority Alert & Early Warning Hub")
st.markdown("Immediate notification stream for projects breaching risk and delay thresholds. Direct notification dispatch to district authorities.")

if not client.check_health():
    st.error("⚠️ Backend API is offline. Please start backend via `python run_backend.py`.")
    st.stop()

# Threshold filter
c_thresh, c_refresh = st.columns([3, 1])
with c_thresh:
    threshold = st.slider("Alert Trigger Risk Score Threshold", min_value=40, max_value=90, value=70, step=5)
with c_refresh:
    st.write("")
    st.write("")
    if st.button("🔄 Refresh Alerts"):
        st.rerun()

try:
    with st.spinner("Scanning project alerts..."):
        alerts = client.get_alerts(threshold=threshold)
except Exception as e:
    st.error(f"Failed to retrieve alerts: {e}")
    st.stop()

st.divider()

# Metric summary
critical_count = sum(1 for a in alerts if a["severity"] == "CRITICAL")
warning_count = sum(1 for a in alerts if a["severity"] == "WARNING")

m1, m2, m3 = st.columns(3)
m1.metric("Total Active Alerts", len(alerts))
m2.metric("Critical Alerts (Red)", critical_count, delta="Immediate Action", delta_color="inverse")
m3.metric("Warning Alerts (Amber)", warning_count)

st.divider()

if not alerts:
    st.success("🎉 No active alerts above the selected threshold. All projects are within normal operating parameters!")
else:
    st.subheader(f"Active Alert Stream ({len(alerts)} Projects)")
    
    for idx, alert in enumerate(alerts):
        is_critical = alert["severity"] == "CRITICAL"
        border_color = "#EF4444" if is_critical else "#F59E0B"
        badge_bg = "#FEE2E2" if is_critical else "#FEF3C7"
        badge_fg = "#991B1B" if is_critical else "#92400E"

        with st.container():
            st.markdown(
                f"""
                <div style="border-left: 5px solid {border_color}; padding: 12px 16px; background-color: #F9FAFB; border-radius: 4px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 1.15rem; font-weight: bold; color: #111827;">{alert['project_name']}</span>
                        <span style="background-color: {badge_bg}; color: {badge_fg}; font-weight: bold; padding: 4px 10px; border-radius: 12px; font-size: 0.85rem;">
                            {alert['severity']} ALERT (Risk: {alert['risk_score']}/100)
                        </span>
                    </div>
                    <p style="margin: 4px 0; color: #4B5563; font-size: 0.9rem;">
                        <strong>ID:</strong> {alert['project_id']} | 📍 <strong>Location:</strong> {alert['district']}, {alert['state']} | ⏱️ <strong>Evaluated:</strong> {alert['evaluated_at']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Bottleneck messages
            st.markdown("**Identified Bottleneck Drivers:**")
            for msg in alert["alert_messages"]:
                st.markdown(f"- ⚠️ {msg}")

            # Email dispatch action
            col_email_btn, col_custom_email = st.columns([2, 3])
            with col_custom_email:
                recip_key = f"recip_{alert['project_id']}_{idx}"
                recipient_val = st.text_input("Recipient Email", value="district.collector@gov.in", key=recip_key)
            with col_email_btn:
                st.write("")
                btn_key = f"dispatch_{alert['project_id']}_{idx}"
                if st.button(f"📧 Send Email Alert for {alert['project_id']}", key=btn_key):
                    with st.spinner("Dispatching alert..."):
                        res = client.send_alert_email(alert["project_id"], recipient=recipient_val)
                        if res.get("status") == "success":
                            st.success(f"✅ Alert dispatched! ({res.get('mode')}) to {res.get('recipient')}")
                            with st.expander("📄 View Email Content Preview"):
                                import streamlit.components.v1 as components
                                components.html(res.get("html_preview", "<p>No preview</p>"), height=400, scrolling=True)
                        else:
                            st.error(f"Failed to dispatch email: {res.get('message')}")

            st.markdown("---")

