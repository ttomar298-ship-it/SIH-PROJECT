import os
import sys
import streamlit as st
from datetime import datetime

# Path setup
STREAMLIT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ROOT_DIR = os.path.abspath(os.path.join(STREAMLIT_DIR, "..", ".."))
for p in [STREAMLIT_DIR, ROOT_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from utils.api_client import client
except ImportError:
    from frontend.streamlit_app.utils.api_client import client

st.set_page_config(
    page_title="Citizen Land Acquisition Tracker | BHOOMI AI",
    page_icon="🧑‍🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Citizen Portal (Warm earth / Government service portal theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Sans+Devanagari:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', 'Noto Sans Devanagari', sans-serif;
    }
    
    /* Citizen Hero Banner */
    .citizen-hero {
        background: linear-gradient(135deg, #064E3B 0%, #065F46 45%, #047857 100%);
        border-radius: 16px;
        padding: 26px 32px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(6, 78, 59, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .citizen-hero h1 {
        color: #FFFFFF;
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .citizen-hero p {
        color: #A7F3D0;
        font-size: 1.05rem;
        margin-top: 6px;
        margin-bottom: 12px;
    }
    .citizen-badge {
        background: rgba(255, 255, 255, 0.18);
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.25);
        display: inline-block;
        margin-right: 8px;
    }

    /* Timeline Step Card */
    .timeline-card {
        background: white;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid #E2E8F0;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
    }
    .timeline-active {
        border: 2px solid #059669 !important;
        background: #F0FDF4 !important;
        box-shadow: 0 6px 16px -2px rgba(5, 150, 105, 0.15);
    }
    .timeline-completed {
        border-left: 4px solid #10B981 !important;
        background: #F8FAFC;
    }
    .timeline-upcoming {
        opacity: 0.7;
        background: #FAFAFA;
    }

    /* Compensation Card */
    .comp-card {
        background: white;
        border-radius: 14px;
        padding: 22px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }
    .comp-metric-label {
        font-size: 0.82rem;
        color: #64748B;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .comp-metric-val {
        font-size: 1.7rem;
        font-weight: 800;
        color: #0F172A;
        margin: 4px 0 2px 0;
    }
    .solatium-tag {
        background: #DCFCE7;
        color: #166534;
        font-size: 0.72rem;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 700;
    }

    /* Rights Card */
    .rights-card {
        background: #F8FAFC;
        border-radius: 12px;
        padding: 16px 18px;
        border-left: 4px solid #059669;
        margin-bottom: 12px;
    }

    /* Section 24 Lapse Warning Alert */
    .lapse-alert {
        background: #FFFBEB;
        border-left: 6px solid #D97706;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 20px;
        color: #92400E;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar: Dedicated Citizen Portal Controls (zero officer session coupling)
with st.sidebar:
    st.markdown("### 🌾 **BHOOMI AI**")
    st.markdown(
        """
        <div style="font-size: 0.75rem; letter-spacing: 1.5px; color: #047857; font-weight: 800; margin-top: -8px;">
            CITIZEN LAND ACCESS PORTAL
        </div>
        <div style="font-size: 0.70rem; color: #64748B; margin-bottom: 16px;">
            RFCTLARR Act, 2013 Public Transparency Service
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("#### 🌐 **Language / भाषा चुनें**")
    lang = st.radio(
        "Display Language",
        ["English", "हिंदी (Hindi)"],
        index=0,
        label_visibility="collapsed"
    )
    is_hi = "हिंदी" in lang

    st.markdown("---")
    st.markdown("#### 📞 **Citizen Grievance Helpline**")
    st.markdown(
        """
        <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; padding: 12px; font-size: 0.82rem; color: #166534;">
            <strong>Toll-Free Helpline:</strong><br>
            📞 1800-11-2013 (MoRTH Land Cell)<br><br>
            <strong>Email Redressal:</strong><br>
            ✉️ grievance.rfctlarr@gov.in<br><br>
            <strong>Working Hours:</strong><br>
            Mon – Fri: 09:30 AM – 06:00 PM
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("#### ⚖️ **Statutory Mandate**")
    st.caption(
        "Governed by the Right to Fair Compensation and Transparency in Land Acquisition, "
        "Rehabilitation and Resettlement Act, 2013 (RFCTLARR)."
    )

# Header Text Dictionaries
TEXTS = {
    "en": {
        "badge": "NATIONAL CITIZEN PORTAL • RFCTLARR ACT, 2013",
        "title": "Track Your Land Acquisition & Compensation Status",
        "subtitle": "Check the official progress of your land parcel, verify 100% solatium calculation, check Section 24 lapse status, and file statutory objections before the CALA.",
        "search_label": "Search Your Land Record",
        "tab_khasra": "By Khasra / Survey Number",
        "tab_mobile": "By Registered Mobile",
        "tab_project": "By Project ID",
        "khasra_input": "Khasra / Plot / Survey Number",
        "khasra_help": "E.g. 142/2, 89A, 204/1, 512/3",
        "village_input": "Village Name (Optional)",
        "village_help": "E.g. Danapur, Phulwari, Rohania, Rajarhat",
        "district_input": "District Name (Optional)",
        "district_help": "E.g. Patna, Varanasi, Kolkata, Thane",
        "mobile_input": "10-Digit Registered Mobile Number",
        "mobile_help": "E.g. 9876543210, 9811223344, 9922334455",
        "proj_input": "Project Identifier (ID)",
        "proj_help": "E.g. PRJ-BI-1001, PRJ-UT-1002, PRJ-WE-1007",
        "search_btn": "🔍 Track My Land Record",
        "quick_test_hint": "💡 Quick test examples: Click one below to auto-populate:",
        "timeline_heading": "Statutory Acquisition Progress (RFCTLARR Pipeline)",
        "comp_heading": "Your Entitled Compensation Breakdown",
        "rights_heading": "Know Your Rights Under RFCTLARR Act, 2013",
        "objection_heading": "File an Objection or Grievance (Section 15)",
        "faq_heading": "Frequently Asked Questions (Citizen Guidance)"
    },
    "hi": {
        "badge": "राष्ट्रीय नागरिक पोर्टल • RFCTLARR अधिनियम, 2013",
        "title": "अपनी भूमि अधिग्रहण एवं मुआवजा स्थिति ट्रैक करें",
        "subtitle": "अपने खसरा भूखंड की आधिकारिक प्रगति देखें, 100% तोषणा (Solatium) गणना सत्यापित करें, धारा 24 व्यपगत स्थिति जांचें, और सीएएलए के समक्ष आपत्ति दर्ज करें।",
        "search_label": "अपने भूमि रिकॉर्ड की खोज करें",
        "tab_khasra": "खसरा / सर्वे संख्या द्वारा",
        "tab_mobile": "पंजीकृत मोबाइल नंबर द्वारा",
        "tab_project": "परियोजना आईडी द्वारा",
        "khasra_input": "खसरा / प्लॉट / सर्वे नंबर",
        "khasra_help": "उदा. 142/2, 89A, 204/1, 512/3",
        "village_input": "ग्राम का नाम (वैकल्पिक)",
        "village_help": "उदा. दानापुर, फुलवारी, रोहनिया, राजारहाट",
        "district_input": "जिला का नाम (वैकल्पिक)",
        "district_help": "उदा. पटना, वाराणसी, कोलकाता, ठाणे",
        "mobile_input": "10-अंकों का पंजीकृत मोबाइल नंबर",
        "mobile_help": "उदा. 9876543210, 9811223344, 9922334455",
        "proj_input": "परियोजना पहचान संख्या (ID)",
        "proj_help": "उदा. PRJ-BI-1001, PRJ-UT-1002, PRJ-WE-1007",
        "search_btn": "🔍 मेरा भूमि रिकॉर्ड खोजें",
        "quick_test_hint": "💡 त्वरित परीक्षण उदाहरण: नीचे दिए गए विकल्प पर क्लिक करें:",
        "timeline_heading": "वैधानिक अधिग्रहण प्रगति (RFCTLARR चरण)",
        "comp_heading": "आपके मुआवजे का विस्तृत विवरण",
        "rights_heading": "RFCTLARR अधिनियम, 2013 के अंतर्गत आपके अधिकार",
        "objection_heading": "आपत्ति या शिकायत दर्ज करें (धारा 15)",
        "faq_heading": "अक्सर पूछे जाने वाले प्रश्न (नागरिक मार्गदर्शिका)"
    }
}
t = TEXTS["hi"] if is_hi else TEXTS["en"]

# Top Hero Banner
st.markdown(f"""
<div class="citizen-hero">
    <span class="citizen-badge">🏛️ {t['badge']}</span>
    <span class="citizen-badge">🔒 Whitelisted Public Data</span>
    <span class="citizen-badge">⚖️ 100% Solatium Guaranteed</span>
    <h1 style="margin-top: 10px;">{t['title']}</h1>
    <p>{t['subtitle']}</p>
</div>
""", unsafe_allow_html=True)

# Quick Demo Preset Helper
if "search_khasra" not in st.session_state:
    st.session_state["search_khasra"] = "142/2"
if "search_village" not in st.session_state:
    st.session_state["search_village"] = "Danapur"
if "search_district" not in st.session_state:
    st.session_state["search_district"] = "Patna"
if "search_mobile" not in st.session_state:
    st.session_state["search_mobile"] = ""
if "search_project_id" not in st.session_state:
    st.session_state["search_project_id"] = ""

st.markdown(f"**{t['quick_test_hint']}**")
q_c1, q_c2, q_c3, q_c4 = st.columns(4)
with q_c1:
    if st.button("🌾 Khasra 142/2 (Patna, Disbursed)", use_container_width=True):
        st.session_state["search_khasra"] = "142/2"
        st.session_state["search_village"] = "Danapur"
        st.session_state["search_district"] = "Patna"
        st.session_state["search_mobile"] = ""
        st.session_state["search_project_id"] = ""
        st.rerun()
with q_c2:
    if st.button("🏢 Khasra 89A (Patna, Open Objection)", use_container_width=True):
        st.session_state["search_khasra"] = "89A"
        st.session_state["search_village"] = "Phulwari"
        st.session_state["search_district"] = "Patna"
        st.session_state["search_mobile"] = ""
        st.session_state["search_project_id"] = ""
        st.rerun()
with q_c3:
    if st.button("🚂 Khasra 204/1 (Varanasi DFC)", use_container_width=True):
        st.session_state["search_khasra"] = "204/1"
        st.session_state["search_village"] = "Rohania"
        st.session_state["search_district"] = "Varanasi"
        st.session_state["search_mobile"] = ""
        st.session_state["search_project_id"] = ""
        st.rerun()
with q_c4:
    if st.button("⚠️ Khasra 512/3 (Sec 24 Lapse Warning)", use_container_width=True):
        st.session_state["search_khasra"] = "512/3"
        st.session_state["search_village"] = "Rajarhat"
        st.session_state["search_district"] = "Kolkata"
        st.session_state["search_mobile"] = ""
        st.session_state["search_project_id"] = ""
        st.rerun()

st.write("")

# Search Tabs
search_tab1, search_tab2, search_tab3 = st.tabs([
    f"📍 {t['tab_khasra']}",
    f"📱 {t['tab_mobile']}",
    f"🏗️ {t['tab_project']}"
])

do_search = False
search_params = {}

with search_tab1:
    s_col1, s_col2, s_col3 = st.columns(3)
    with s_col1:
        in_khasra = st.text_input(t["khasra_input"], value=st.session_state["search_khasra"], help=t["khasra_help"])
    with s_col2:
        in_village = st.text_input(t["village_input"], value=st.session_state["search_village"], help=t["village_help"])
    with s_col3:
        in_district = st.text_input(t["district_input"], value=st.session_state["search_district"], help=t["district_help"])
    
    if st.button(t["search_btn"], key="btn_search_khasra", type="primary", use_container_width=True):
        if in_khasra.strip():
            search_params = {
                "khasra_number": in_khasra.strip(),
                "village": in_village.strip() if in_village.strip() else None,
                "district": in_district.strip() if in_district.strip() else None
            }
            do_search = True
        else:
            st.warning("Please enter a Khasra / Survey Number.")

with search_tab2:
    in_mobile = st.text_input(t["mobile_input"], value=st.session_state["search_mobile"], help=t["mobile_help"])
    if st.button(t["search_btn"], key="btn_search_mobile", type="primary", use_container_width=True):
        if in_mobile.strip():
            search_params = {"mobile_number": in_mobile.strip()}
            do_search = True
        else:
            st.warning("Please enter a 10-digit mobile number.")

with search_tab3:
    in_proj = st.text_input(t["proj_input"], value=st.session_state["search_project_id"], help=t["proj_help"])
    if st.button(t["search_btn"], key="btn_search_proj", type="primary", use_container_width=True):
        if in_proj.strip():
            search_params = {"project_id": in_proj.strip()}
            do_search = True
        else:
            st.warning("Please enter a Project ID.")

# Auto-execute default search on first load
if "citizen_data" not in st.session_state and not do_search:
    search_params = {
        "khasra_number": st.session_state["search_khasra"],
        "village": st.session_state["search_village"],
        "district": st.session_state["search_district"]
    }
    do_search = True

if do_search and search_params:
    with st.spinner("Fetching verified statutory land record from CALA database..."):
        try:
            result = client.track_citizen_status(**search_params)
            st.session_state["citizen_data"] = result
        except Exception as err:
            st.error(f"⚠️ Search failed: {err}")
            st.session_state["citizen_data"] = None

data = st.session_state.get("citizen_data")

if data:
    st.divider()

    # Section 24 Lapse Warning Alert Banner (if triggered)
    if data.get("section_24_lapse_risk"):
        lapse_text = data.get("section_24_details_hi" if is_hi else "section_24_details")
        st.markdown(f"""
        <div class="lapse-alert">
            <div style="display: flex; align-items: flex-start; gap: 12px;">
                <span style="font-size: 1.8rem;">🚨</span>
                <div>
                    <strong style="font-size: 1.05rem; letter-spacing: 0.3px;">
                        {'वैधानिक सूचना: धारा 24(2) के तहत अधिग्रहण व्यपगत जोखिम' if is_hi else 'STATUTORY NOTICE: Section 24(2) Acquisition Lapse Flag'}
                    </strong>
                    <p style="margin: 6px 0 0 0; font-size: 0.92rem; line-height: 1.5;">
                        {lapse_text}
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Land Parcel Details Header
    parcel_info = data.get("parcel_info")
    col_p1, col_p2, col_p3 = st.columns([3, 2, 2])
    
    with col_p1:
        st.markdown(f"### 📍 **{data['project_name']}**")
        st.caption(f"Project ID: `{data['project_id']}` • State/District: **{data['district']}, {data['state']}**")
        if parcel_info:
            st.markdown(f"""
            **{'खसरा / भूखंड' if is_hi else 'Khasra / Plot'}:** `{parcel_info['khasra_number']}` &nbsp;|&nbsp; 
            **{'ग्राम' if is_hi else 'Village'}:** {parcel_info['village']} &nbsp;|&nbsp;
            **{'क्षेत्रफल' if is_hi else 'Area'}:** {parcel_info['area_acres']} {'एकड़' if is_hi else 'Acres'} ({parcel_info['land_type']})
            """)
    
    with col_p2:
        st.markdown(f"**{'वर्तमान चरण' if is_hi else 'Current Stage'}:**")
        stage_name = data["current_stage_hi"] if is_hi else data["current_stage"]
        st.markdown(f"""
        <div style="background: #E0F2FE; border-left: 4px solid #0284C7; padding: 8px 12px; border-radius: 0 8px 8px 0; font-weight: 700; color: #0369A1;">
            {stage_name}
        </div>
        """, unsafe_allow_html=True)

    with col_p3:
        st.markdown(f"**{'आपत्ति विंडो' if is_hi else 'Objection Window'}:**")
        if data.get("objection_window_open"):
            deadline = data.get("objection_deadline") or "Open"
            st.markdown(f"""
            <span style="background: #DCFCE7; color: #15803D; padding: 4px 10px; border-radius: 20px; font-weight: 700; font-size: 0.85rem;">
                🟢 {'खुली है' if is_hi else 'OPEN'} (अंतिम तिथि: {deadline})
            </span>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <span style="background: #F1F5F9; color: #64748B; padding: 4px 10px; border-radius: 20px; font-weight: 600; font-size: 0.85rem;">
                ⚪ {'समाप्त' if is_hi else 'CLOSED / CONCLUDED'}
            </span>
            """, unsafe_allow_html=True)

    # 1. RFCTLARR 6-Stage Timeline Progression
    st.write("")
    st.subheader(f"🗺️ {t['timeline_heading']}")
    st.caption("Right to Fair Compensation and Transparency in Land Acquisition, Rehabilitation and Resettlement Act, 2013")

    timeline = data.get("timeline_stages", [])
    if timeline:
        cols = st.columns(len(timeline))
        for i, stage in enumerate(timeline):
            with cols[i]:
                s_name = stage["stage_name_hi"] if is_hi else stage["stage_name_en"]
                s_desc = stage["plain_hindi_description"] if is_hi else stage["plain_english_description"]
                s_sec = stage["rfctlarr_section"]
                
                if stage["is_current"]:
                    badge = "🔵 " + ("सक्रिय चरण" if is_hi else "Current Active")
                    card_cls = "timeline-active"
                elif stage["is_completed"]:
                    badge = "✅ " + ("पूर्ण" if is_hi else "Completed")
                    card_cls = "timeline-completed"
                else:
                    badge = "⚪ " + ("आगामी" if is_hi else "Upcoming")
                    card_cls = "timeline-upcoming"

                st.markdown(f"""
                <div class="timeline-card {card_cls}">
                    <div>
                        <div style="font-size: 0.72rem; font-weight: 700; color: #059669; margin-bottom: 2px;">{s_sec}</div>
                        <div style="font-size: 0.88rem; font-weight: 700; color: #0F172A; line-height: 1.25; margin-bottom: 6px;">{s_name}</div>
                        <div style="font-size: 0.75rem; color: #475569; line-height: 1.35;">{s_desc}</div>
                    </div>
                    <div style="margin-top: 10px; font-size: 0.75rem; font-weight: 700;">
                        {badge}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.write("")

    # 2. Compensation & R&R Entitlements Section
    st.subheader(f"💰 {t['comp_heading']}")
    comp = data.get("compensation")
    
    if comp:
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown(f"""
            <div class="comp-card" style="border-top: 4px solid #3B82F6;">
                <div class="comp-metric-label">{'आधार बाजार मूल्य' if is_hi else 'Base Market Value'}</div>
                <div class="comp-metric-val">₹{comp['market_value_inr']:,.0f}</div>
                <div style="font-size: 0.75rem; color: #64748B;">{'सर्किल रेट / पंजीकृत दर पर आधारित' if is_hi else 'Based on official Circle / Stamp rate'}</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="comp-card" style="border-top: 4px solid #10B981;">
                <div class="comp-metric-label">
                    {'100% तोषणा (Solatium)' if is_hi else '100% Solatium (Mandatory)'}
                    <span class="solatium-tag">Sec 30(1)</span>
                </div>
                <div class="comp-metric-val" style="color: #059669;">+ ₹{comp['solatium_inr']:,.0f}</div>
                <div style="font-size: 0.75rem; color: #64748B;">{'100% अनिवार्य अतिरिक्त राशि' if is_hi else 'Mandatory 100% statutory addition'}</div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="comp-card" style="border-top: 4px solid #8B5CF6;">
                <div class="comp-metric-label">{'गुणक एवं वृक्ष/संपत्ति मूल्य' if is_hi else 'Multiplier & Asset Value'}</div>
                <div class="comp-metric-val">+ ₹{comp['additional_multiplier_inr']:,.0f}</div>
                <div style="font-size: 0.75rem; color: #64748B;">{'ग्रामीण गुणक एवं पेड़ों का मूल्यांकन' if is_hi else 'Rural factor & standing assets'}</div>
            </div>
            """, unsafe_allow_html=True)

        with c4:
            st.markdown(f"""
            <div class="comp-card" style="border-top: 4px solid #059669; background: #F0FDF4;">
                <div class="comp-metric-label" style="color: #166534;">{'कुल देय मुआवजा' if is_hi else 'Total Entitled Amount'}</div>
                <div class="comp-metric-val" style="color: #15803D;">₹{comp['total_compensation_inr']:,.0f}</div>
                <div style="font-size: 0.75rem; font-weight: bold; color: #166534;">
                    {'स्थिति:' if is_hi else 'Status:'} {comp['payment_status']}
                    {f" ({comp['disbursement_date']})" if comp['disbursement_date'] else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.caption(f"ℹ️ {comp['calculation_formula_note']}")
    else:
        st.info("ℹ️ Compensation determination is currently under preparation by CALA. Formal award will be published under Section 23/30.")

    # R&R Entitlements
    rr = data.get("rr_details")
    if rr:
        with st.expander(f"🏡 **{'पुनर्वास एवं पुनर्व्यवस्था (R&R) अधिकार' if is_hi else 'Rehabilitation & Resettlement (R&R) Entitlements'}** (Schedule II)", expanded=True):
            st.markdown(f"""
            - **{'योजना स्थिति' if is_hi else 'Scheme Status'}:** `{rr['status']}`
            - **{'स्वीकृत पैकेज' if is_hi else 'Approved Entitlements'}:** {rr['entitlements']}
            - **{'कानूनी गारंटी' if is_hi else 'Statutory Guarantees'}:** {rr['mandatory_provisions']}
            """)

    st.write("")

    # 3. Know Your Rights Statutory Panel
    st.subheader(f"⚖️ {t['rights_heading']}")
    st.caption("Guaranteed legal protections for Indian citizens under the Land Acquisition Act, 2013")

    r_col1, r_col2 = st.columns(2)
    with r_col1:
        st.markdown(f"""
        <div class="rights-card">
            <strong style="color: #065F46; font-size: 0.95rem;">1. 100% Solatium (Section 30(1))</strong>
            <p style="margin: 4px 0 0 0; font-size: 0.84rem; color: #334155;">
                {'कलेक्टर द्वारा बाजार मूल्य के समतुल्य 100% अतिरिक्त तोषणा (Solatium) राशि जोड़ना कानूनी रूप से अनिवार्य है।' if is_hi else 'The Collector is legally mandated to award an additional solatium equal to 100% of the market value of the land.'}
            </p>
        </div>
        <div class="rights-card">
            <strong style="color: #065F46; font-size: 0.95rem;">2. Informed Consent Requirement (Section 2(2))</strong>
            <p style="margin: 4px 0 0 0; font-size: 0.84rem; color: #334155;">
                {'पीपीपी परियोजनाओं के लिए न्यूनतम 70% तथा निजी कंपनियों के लिए 80% प्रभावित भूस्वामियों की पूर्व लिखित सहमति अनिवार्य है।' if is_hi else 'Mandatory prior written consent of at least 70% of affected families for PPP projects and 80% for private projects is mandatory.'}
            </p>
        </div>
        <div class="rights-card">
            <strong style="color: #065F46; font-size: 0.95rem;">3. Section 10 Multi-Crop Agricultural Protection</strong>
            <p style="margin: 4px 0 0 0; font-size: 0.84rem; color: #334155;">
                {'सिंचित बहुफसली कृषि भूमि का अधिग्रहण केवल असाधारण परिस्थितियों में किया जा सकता है और समतुल्य बंजर भूमि को कृषि योग्य बनाना अनिवार्य है।' if is_hi else 'Irrigated multi-cropped agricultural land cannot normally be acquired, and equal fallow land must be developed if acquired.'}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with r_col2:
        st.markdown(f"""
        <div class="rights-card">
            <strong style="color: #065F46; font-size: 0.95rem;">4. Section 24 Lapsing of Old Proceedings</strong>
            <p style="margin: 4px 0 0 0; font-size: 0.84rem; color: #334155;">
                {'यदि अवार्ड घोषित हुए 5 वर्ष या अधिक हो चुके हैं और भौतिक कब्जा नहीं लिया गया अथवा मुआवजा नहीं दिया गया, तो अधिग्रहण प्रक्रिया निरस्त मानी जाती है।' if is_hi else 'Where an award was made 5+ years ago and physical possession was not taken or compensation not paid, the acquisition legally lapses.'}
            </p>
        </div>
        <div class="rights-card">
            <strong style="color: #065F46; font-size: 0.95rem;">5. Section 101 Return of Unused Land</strong>
            <p style="margin: 4px 0 0 0; font-size: 0.84rem; color: #334155;">
                {'यदि अधिग्रहित भूमि 5 वर्ष तक उपयोग में नहीं लाई जाती, तो इसे मूल भूस्वामियों अथवा राज्य भूमि बैंक को वापस करना अनिवार्य है।' if is_hi else 'If land acquired remains unutilized for 5 years from possession date, it must be returned to the original owners or State Land Bank.'}
            </p>
        </div>
        <div class="rights-card">
            <strong style="color: #065F46; font-size: 0.95rem;">6. Section 38 Prior Payment Before Possession</strong>
            <p style="margin: 4px 0 0 0; font-size: 0.84rem; color: #334155;">
                {'जब तक संपूर्ण मुआवजा एवं पुनर्वास राशि भूस्वामी के बैंक खाते में जमा नहीं हो जाती, तब तक भौतिक कब्जा नहीं लिया जा सकता।' if is_hi else 'The Collector cannot take physical possession of land until full compensation and monetary R&R entitlements have been disbursed.'}
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # 4. Interactive "File an Objection / Grievance" Form
    st.subheader(f"📝 {t['objection_heading']}")
    st.caption("Lodge an official objection before the Competent Authority Land Acquisition (CALA). You will receive an instant tracking ID and SMS/email receipt.")

    with st.form("form_citizen_objection"):
        st.markdown(f"**{'आपत्ति विवरण' if is_hi else 'Grievance Submission Form'}**")
        
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            obj_citizen_name = st.text_input(
                "Full Name of Landowner / Claimant *" if not is_hi else "भूस्वामी / दावेदार का पूरा नाम *",
                value=""
            )
            obj_mobile = st.text_input(
                "Mobile Number for SMS Tracking *" if not is_hi else "एसएमएस ट्रैकिंग हेतु मोबाइल नंबर *",
                value="",
                max_chars=10
            )
            obj_email = st.text_input(
                "Email Address (for Official Digital Receipt)" if not is_hi else "ईमेल पता (आधिकारिक पावती रसीद हेतु)",
                value=""
            )

        with f_col2:
            obj_category = st.selectbox(
                "Objection Category *" if not is_hi else "आपत्ति की श्रेणी *",
                [
                    "Section 15 Hearing: Land Suitability / Public Purpose",
                    "Compensation Dispute: Circle Rate / Solatium Calculation",
                    "R&R Grievance: Schedule II Housing / Subsistence Entitlement",
                    "Possession Dispute: Possession Taken Without Full Payment (Sec 38)",
                    "Measurement / Boundary / Khasra Area Error",
                    "Section 24 Lapsing Petition (Award > 5 Years Unsettled)"
                ]
            )
            obj_khasra = st.text_input(
                "Khasra / Plot Number *" if not is_hi else "खसरा / प्लॉट नंबर *",
                value=parcel_info["khasra_number"] if parcel_info else ""
            )
            obj_proj_id = st.text_input(
                "Project ID" if not is_hi else "परियोजना आईडी",
                value=data.get("project_id", "")
            )

        obj_reason = st.text_area(
            "Detailed Grounds of Objection / Grievance (Minimum 10 characters) *" if not is_hi else "आपत्ति / शिकायत के विस्तृत आधार (न्यूनतम 10 अक्षर) *",
            placeholder="Please explain in detail your grievance regarding valuation, boundary measurement, or R&R entitlements..."
        )

        submitted = st.form_submit_button(
            "🚀 Submit Formal Objection / शिकायत दर्ज करें",
            type="primary",
            use_container_width=True
        )

        if submitted:
            if not obj_citizen_name.strip() or len(obj_citizen_name.strip()) < 2:
                st.error("Please enter a valid full name.")
            elif not obj_mobile.strip() or len(obj_mobile.strip()) < 10 or not obj_mobile.strip().isdigit():
                st.error("Please enter a valid 10-digit mobile number.")
            elif not obj_reason.strip() or len(obj_reason.strip()) < 10:
                st.error("Please provide at least 10 characters describing the grounds of objection.")
            else:
                payload = {
                    "project_id": obj_proj_id.strip() if obj_proj_id.strip() else None,
                    "parcel_id": parcel_info["parcel_id"] if parcel_info else None,
                    "khasra_number": obj_khasra.strip() if obj_khasra.strip() else None,
                    "village": parcel_info["village"] if parcel_info else None,
                    "district": data.get("district"),
                    "citizen_name": obj_citizen_name.strip(),
                    "mobile_number": obj_mobile.strip(),
                    "email": obj_email.strip() if obj_email.strip() else None,
                    "objection_category": obj_category,
                    "reason": obj_reason.strip()
                }
                
                try:
                    res = client.submit_citizen_objection(payload)
                    st.success(f"✅ **{res['message']}**")
                    st.markdown(f"""
                    <div style="background: #F0FDF4; border: 1px solid #86EFAC; border-radius: 8px; padding: 14px; margin-top: 10px;">
                        <strong>📌 {'आधिकारिक ट्रैकिंग संदर्भ' if is_hi else 'Official Tracking Reference'}:</strong> 
                        <span style="font-size: 1.2rem; color: #15803D; font-weight: bold; margin-left: 8px;">{res['objection_id']}</span><br>
                        <strong>⏱️ {'वैधानिक सुनवाई समयसीमा' if is_hi else 'Mandated Resolution Window'}:</strong> {res['expected_resolution_days']} {'दिन (RFCTLARR धारा 15)' if is_hi else 'Days (RFCTLARR Section 15)'}<br>
                        <strong>📱 SMS Status:</strong> {res['sms_status']} &nbsp;|&nbsp; 
                        <strong>✉️ Email Status:</strong> {res['email_status']}
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as ex:
                    st.error(f"⚠️ Failed to lodge objection: {ex}")

    st.write("")

    # 5. FAQ Accordion
    st.subheader(f"❓ {t['faq_heading']}")
    
    if is_hi:
        faqs = [
            ("क्या मेरी भूमि मेरी जानकारी के बिना अधिग्रहित की जा सकती है?", "नहीं। RFCTLARR अधिनियम 2013 के अंतर्गत धारा 4 (एसआईए) और धारा 11 (प्रारंभिक अधिसूचना) का स्थानीय समाचार पत्रों और ग्राम सभा में अनिवार्य प्रकाशन आवश्यक है।"),
            ("100% तोषणा (Solatium) क्या है?", "धारा 30(1) के तहत, अनिवार्य अधिग्रहण से होने वाली असुविधा के लिए सरकार द्वारा कुल बाजार मूल्य का 100% अतिरिक्त रूप से देना कानूनी रूप से अनिवार्य है।"),
            ("यदि मैं मुआवजा राशि से संतुष्ट न होऊं तो क्या कर सकता हूँ?", "आप धारा 64 के तहत भूमि अधिग्रहण, पुनर्वास एवं पुनर्व्यवस्था प्राधिकरण (LARR Authority) के समक्ष 6 सप्ताह के भीतर संदर्भ (Reference) याचिका प्रस्तुत कर सकते हैं।"),
            ("कब्जा कब तक नहीं लिया जा सकता?", "धारा 38 के अनुसार जब तक आपके बैंक खाते में 100% मुआवजा राशि और पुनर्वास लाभ जमा नहीं हो जाते, तब तक सरकार आपकी भूमि का भौतिक कब्जा नहीं ले सकती।"),
            ("धारा 24 के तहत प्रक्रिया कब व्यपगत (Lapse) मानी जाती है?", "यदि अवार्ड पारित हुए 5 वर्ष या उससे अधिक समय बीत चुका है और भौतिक कब्जा नहीं लिया गया अथवा मुआवजा भुगतान नहीं हुआ है, तो कार्यवाही कानूनी रूप से व्यपगत मानी जाती है।")
        ]
    else:
        faqs = [
            ("Can my land be acquired without my prior knowledge?", "No. The RFCTLARR Act 2013 strictly mandates public hearing during the Social Impact Assessment (Section 4) and gazette publication of Preliminary Notification (Section 11) in two local daily newspapers and the Gram Sabha."),
            ("What is 100% Solatium and is it mandatory?", "Yes. Under Section 30(1) of the Act, the Collector must add a solatium amount equivalent to 100% of the total land market value to compensate for the compulsory nature of the acquisition."),
            ("What recourse do I have if I disagree with the compensation amount?", "You can accept the compensation amount 'under protest' and file an application before the Land Acquisition, Rehabilitation and Resettlement Authority (LARR Authority) under Section 64 within 6 weeks of the award."),
            ("When am I required to vacate my land?", "Under Section 38, physical possession cannot be taken until full monetary compensation and R&R allowances are credited into your bank account."),
            ("When does an acquisition lapse under Section 24?", "Where an award was made 5 or more years prior, and either physical possession has not been taken or compensation has not been paid, the acquisition proceedings legally lapse under Section 24(2).")
        ]

    for question, answer in faqs:
        with st.expander(f"📌 {question}"):
            st.markdown(f"<span style='color: #334155; font-size: 0.92rem;'>{answer}</span>", unsafe_allow_html=True)

    # Footer Disclaimer
    st.markdown("---")
    st.caption(f"🔒 {data['disclaimer']} • Last Synced: `{data['last_updated']}`")

