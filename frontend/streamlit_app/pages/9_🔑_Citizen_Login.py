import sys
import os
import random
import streamlit as st
from datetime import datetime, timedelta

# ── Path setup ──────────────────────────────────────────────────────────────
PAGE_DIR = os.path.abspath(os.path.dirname(__file__))
STREAMLIT_DIR = os.path.abspath(os.path.join(PAGE_DIR, ".."))
ROOT_DIR = os.path.abspath(os.path.join(PAGE_DIR, "..", "..", ".."))
for p in [PAGE_DIR, STREAMLIT_DIR, ROOT_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from utils.gov_theme import (
        apply_gov_theme,
        hide_default_sidebar_nav,
        render_split_login_header,
        render_gov_footer,
    )
except ImportError:
    from frontend.streamlit_app.utils.gov_theme import (
        apply_gov_theme,
        hide_default_sidebar_nav,
        render_split_login_header,
        render_gov_footer,
    )

LOGO_PATH = os.path.join(STREAMLIT_DIR, "assets", "logo.png")

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Citizen Login — BHOOMI AI",
    page_icon="🔑",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_gov_theme()
hide_default_sidebar_nav()
render_split_login_header(
    logo_path=LOGO_PATH,
    title="Citizen Login",
    subtitle="Track your land acquisition status",
)


# ── Session isolation note ───────────────────────────────────────────────────
# Officer keys ('authenticated', 'user') are NEVER read or written here.
# Citizen keys: 'citizen_authenticated', 'citizen_identifier',
#               'citizen_otp', 'citizen_otp_ts', 'citizen_pending_id'

# ── Already logged in? ───────────────────────────────────────────────────────
if st.session_state.get("citizen_authenticated", False):
    cid = st.session_state.get("citizen_identifier", "")
    st.success(f"✅ You are already logged in as **{cid}**.")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.info("You can now access the Citizen Tracker to check your land parcel status.")
    with col_b:
        if st.button("🧑‍🌾 Go to Citizen Tracker", type="primary", use_container_width=True):
            try:
                st.switch_page("pages/8_🧑‍🌾_Citizen_Tracker.py")
            except Exception:
                st.markdown(
                    '<meta http-equiv="refresh" content="0; url=/Citizen_Tracker">',
                    unsafe_allow_html=True,
                )
        if st.button("🚪 Citizen Logout", use_container_width=True):
            # Clear ONLY citizen keys — officer keys ('authenticated', 'user') untouched
            for k in ["citizen_authenticated", "citizen_identifier",
                      "citizen_otp", "citizen_otp_ts", "citizen_pending_id"]:
                st.session_state.pop(k, None)
            st.rerun()
    render_gov_footer()
    st.stop()

# ── Login Form ───────────────────────────────────────────────────────────────
_, col_form, _ = st.columns([1, 2, 1])

with col_form:
    # ── Fast 1-Click Demo Login for Evaluators / SIH Jury ─────────────────────
    if st.button("⚡ 1-Click Demo Citizen Login (Instant Access)", type="secondary", use_container_width=True):
        st.session_state["citizen_authenticated"] = True
        st.session_state["citizen_identifier"] = "9876543210 (Demo Landowner)"
        st.query_params["citizen_session"] = "1"
        st.query_params["citizen_id"] = "9876543210"
        st.switch_page("pages/8_🧑‍🌾_Citizen_Tracker.py")

    st.markdown("<div style='text-align:center;color:#64748B;font-size:0.8rem;margin:8px 0;'>— OR ENTER DETAILS BELOW —</div>", unsafe_allow_html=True)

    login_method = st.radio(
        "Login via",
        ["📱 Mobile Number", "📧 Email Address"],
        horizontal=True,
        key="citizen_login_method",
    )
    is_mobile = "Mobile" in login_method

    identifier = st.text_input(
        "Mobile Number (10 digits)" if is_mobile else "Email Address",
        placeholder="9876543210" if is_mobile else "citizen@example.com",
        key="citizen_identifier_input",
    ).strip()

    # ── Send OTP ─────────────────────────────────────────────────────────────
    if st.button("📨 Send OTP", type="primary", use_container_width=True):
        if is_mobile:
            if not identifier.isdigit() or len(identifier) != 10:
                st.error("❌ Please enter a valid 10-digit mobile number.")
                st.stop()
        else:
            if "@" not in identifier or "." not in identifier.split("@")[-1]:
                st.error("❌ Please enter a valid email address.")
                st.stop()

        otp = str(random.randint(100000, 999999))
        st.session_state["citizen_otp"] = otp
        st.session_state["citizen_otp_ts"] = datetime.now().isoformat()
        st.session_state["citizen_pending_id"] = identifier

        # TODO: integrate real SMS/email OTP provider before production
        st.info(
            f"📲 **DEMO MODE** — OTP (would normally be sent by "
            f"{'SMS' if is_mobile else 'email'}): **{otp}**\n\n"
            f"*In production this message would be delivered to `{identifier}`.*"
        )
        st.success("✅ OTP generated! Enter it below to verify.")

    # ── OTP Verification ──────────────────────────────────────────────────────
    stored_otp = st.session_state.get("citizen_otp", "")
    if stored_otp:
        st.markdown("---")
        st.markdown("#### ✅ Verify OTP")
        entered_otp = st.text_input(
            "Enter 6-digit OTP",
            max_chars=6,
            placeholder="------",
            key="citizen_otp_input",
        ).strip()

        col_verify, col_resend = st.columns([1, 1])

        with col_verify:
            if st.button("✔️ Verify OTP", type="primary", use_container_width=True):
                otp_ts_str = st.session_state.get("citizen_otp_ts", "")
                expired = True
                if otp_ts_str:
                    otp_ts = datetime.fromisoformat(otp_ts_str)
                    expired = (datetime.now() - otp_ts) > timedelta(minutes=5)

                if expired:
                    st.error("⏰ OTP has expired (5-minute window). Please request a new OTP.")
                    for k in ["citizen_otp", "citizen_otp_ts"]:
                        st.session_state.pop(k, None)
                elif entered_otp == stored_otp:
                    # ✅ Successful citizen login
                    cit_id = st.session_state.get("citizen_pending_id", identifier)
                    st.session_state["citizen_authenticated"] = True
                    st.session_state["citizen_identifier"] = cit_id
                    st.query_params["citizen_session"] = "1"
                    st.query_params["citizen_id"] = cit_id
                    # Clear OTP from session state after successful use
                    for k in ["citizen_otp", "citizen_otp_ts", "citizen_pending_id"]:
                        st.session_state.pop(k, None)
                    st.switch_page("pages/8_🧑‍🌾_Citizen_Tracker.py")
                else:
                    st.error("❌ Incorrect OTP. Please try again or request a new one.")


        with col_resend:
            if st.button("🔄 Resend OTP", use_container_width=True):
                for k in ["citizen_otp", "citizen_otp_ts"]:
                    st.session_state.pop(k, None)
                st.rerun()

    st.markdown("---")
    st.caption(
        "🔒 Your data is protected under the IT Act, 2000. "
        "OTPs expire in 5 minutes. "
        "This is a demo portal — no real SMS or email is sent in this version."
    )

render_gov_footer()

