"""
i18n.py — Internationalization (English / हिन्दी) for BHOOMI AI
================================================================
Provides bilingual dictionary mappings and helper functions for
seamless switching between English and Hindi across the platform.
"""

import streamlit as st
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# Core Translation Dictionary
# ─────────────────────────────────────────────────────────────────────────────

TRANSLATIONS = {
    # ── Platform Identity & Landing Hero ─────────────────────────────────────
    "site_title": {
        "en": "BHOOMI AI",
        "hi": "भूमि एआई"
    },
    "site_subtitle": {
        "en": "Land Acquisition Delay Prediction & Risk Management System",
        "hi": "भूमि अधिग्रहण विलंब पूर्वानुमान एवं जोखिम प्रबंधन प्रणाली"
    },
    "hero_tagline": {
        "en": "LAND • DATA • BETTER TOMORROW",
        "hi": "भूमि • डेटा • बेहतर भविष्य"
    },
    "hero_trust": {
        "en": "PM GATISHAKTI • SIH26017 PROTOTYPE",
        "hi": "पीएम गतिशक्ति • एसआईएच26017 प्रोटोटाइप"
    },
    "platform_badge": {
        "en": "PM GatiShakti National Master Plan • SIH26017",
        "hi": "पीएम गतिशक्ति राष्ट्रीय मास्टर प्लान • एसआईएच26017"
    },

    # ── Role Selection Cards (Landing Page) ──────────────────────────────────
    "officer_card_title": {
        "en": "Officer Portal",
        "hi": "अधिकारी पोर्टल"
    },
    "officer_card_desc": {
        "en": "Role-based access for CALA, National Project Directors, MoSPI monitors, and SIH jury evaluation.",
        "hi": "सीएएलए, राष्ट्रीय परियोजना निदेशकों, एमओएसपीआई मॉनिटरों और जूरी के लिए भूमिका-आधारित पहुंच।"
    },
    "officer_btn": {
        "en": "🔐 Go to Officer Login →",
        "hi": "🔐 अधिकारी लॉगिन पर जाएं →"
    },
    "feat_shap": {
        "en": "Delay cause attribution",
        "hi": "विलंब कारण विश्लेषण (AI)"
    },
    "feat_risk": {
        "en": "Portfolio-wide delay prediction",
        "hi": "परियोजना-व्यापी विलंब पूर्वानुमान"
    },
    "feat_gis": {
        "en": "Alignment risk mapping",
        "hi": "संरेखण जोखिम मानचित्रण"
    },
    "feat_alerts": {
        "en": "Section 24 lapsing risk warnings",
        "hi": "धारा 24 चूक जोखिम चेतावनियां"
    },

    "citizen_card_title": {
        "en": "Citizen Land Tracker",
        "hi": "नागरिक भूमि ट्रैकर"
    },
    "citizen_card_desc": {
        "en": "Public parcel tracking for landowners and affected families under RFCTLARR Act, 2013.",
        "hi": "आरएफसीटीएलएआरआर अधिनियम, 2013 के तहत भूस्वामियों और प्रभावित परिवारों के लिए सार्वजनिक ट्रैकिंग।"
    },
    "citizen_btn": {
        "en": "🧑‍🌾 Go to Citizen Login →",
        "hi": "🧑‍🌾 नागरिक लॉगिन पर जाएं →"
    },
    "feat_otp": {
        "en": "Direct mobile/email access",
        "hi": "प्रत्यक्ष मोबाइल/ईमेल सत्यापन"
    },
    "feat_comp": {
        "en": "SLA tracking & payout",
        "hi": "मुआवजा स्थिति एवं भुगतान ट्रैकिंग"
    },
    "feat_rights": {
        "en": "Section 24 & grievance filing",
        "hi": "धारा 24 अधिकार एवं शिकायत निवारण"
    },
    "feat_records": {
        "en": "DILRMP ownership verification",
        "hi": "डीआईएलआरएमपी भूमि स्वामित्व सत्यापन"
    },

    # ── Top Navbar Tabs ───────────────────────────────────────────────────────
    "nav_dashboard": {
        "en": "🏛️ Dashboard",
        "hi": "🏛️ डैशबोर्ड"
    },
    "nav_projects": {
        "en": "📊 Projects",
        "hi": "📊 परियोजनाएं"
    },
    "nav_risk": {
        "en": "🏆 Risk Ranking",
        "hi": "🏆 जोखिम रैंकिंग"
    },
    "nav_capital": {
        "en": "💰 Capital Allocation",
        "hi": "💰 पूंजी आवंटन"
    },
    "nav_shap": {
        "en": "🧠 SHAP AI",
        "hi": "🧠 शेप एआई"
    },
    "nav_gis": {
        "en": "🗺️ GIS Map",
        "hi": "🗺️ जीआईएस मानचित्र"
    },
    "nav_alerts": {
        "en": "🚨 Alerts",
        "hi": "🚨 अलर्ट"
    },
    "nav_add": {
        "en": "➕ Add Project",
        "hi": "➕ परियोजना जोड़ें"
    },
    "nav_dilrmp": {
        "en": "📜 DILRMP",
        "hi": "📜 भूमि रिकॉर्ड"
    },
    "nav_citizen": {
        "en": "🧑‍🌾 Citizen",
        "hi": "🧑‍🌾 नागरिक"
    },
    "sign_out": {
        "en": "🚪 Sign Out",
        "hi": "🚪 साइन आउट"
    },

    # ── Officer Login Page ───────────────────────────────────────────────────
    "officer_login_title": {
        "en": "Officer Login",
        "hi": "अधिकारी लॉगिन"
    },
    "officer_login_sub": {
        "en": "Role-based access for authorized government officials",
        "hi": "अधिकृत सरकारी अधिकारियों के लिए भूमिका-आधारित पहुंच"
    },
    "tab_quick_login": {
        "en": "⚡ 1-Click Fast Login (Presentation / Jury)",
        "hi": "⚡ 1-क्लिक त्वरित लॉगिन (प्रस्तुति / जूरी)"
    },
    "tab_official_login": {
        "en": "🔐 Official Credentials Login",
        "hi": "🔐 आधिकारिक क्रेडेंशियल लॉगिन"
    },
    "role_director": {
        "en": "National Director",
        "hi": "राष्ट्रीय निदेशक"
    },
    "role_director_dept": {
        "en": "PM GatiShakti National Master Plan (DPIIT)",
        "hi": "पीएम गतिशक्ति राष्ट्रीय मास्टर प्लान (DPIIT)"
    },
    "role_cala": {
        "en": "CALA Officer",
        "hi": "सीएएलए अधिकारी"
    },
    "role_cala_dept": {
        "en": "Competent Authority Land Acquisition (Revenue)",
        "hi": "सक्षम प्राधिकारी भूमि अधिग्रहण (राजस्व)"
    },
    "role_mospi": {
        "en": "MoSPI Central Monitor",
        "hi": "एमओएसपीआई केंद्रीय मॉनिटर"
    },
    "role_mospi_dept": {
        "en": "Ministry of Statistics & Programme Implementation",
        "hi": "सांख्यिकी एवं कार्यक्रम कार्यान्वयन मंत्रालय"
    },
    "role_jury": {
        "en": "SIH Evaluation Jury",
        "hi": "एसआईएच मूल्यांकन जूरी"
    },
    "role_jury_dept": {
        "en": "Smart India Hackathon Grand Finale Jury",
        "hi": "स्मार्ट इंडिया हैकाथॉन ग्रैंड फिनाले जूरी"
    },
    "btn_login_director": {
        "en": "Log In as Director",
        "hi": "निदेशक के रूप में लॉगिन करें"
    },
    "btn_login_cala": {
        "en": "Log In as CALA",
        "hi": "सीएएलए के रूप में लॉगिन करें"
    },
    "btn_login_mospi": {
        "en": "Log In as MoSPI",
        "hi": "एमओएसपीआई के रूप में लॉगिन करें"
    },
    "btn_login_jury": {
        "en": "Log In as SIH Jury",
        "hi": "एसआईएच जूरी के रूप में लॉगिन करें"
    },
    "input_email": {
        "en": "Official Gov Email / Username",
        "hi": "आधिकारिक सरकारी ईमेल / उपयोगकर्ता नाम"
    },
    "input_password": {
        "en": "Password",
        "hi": "पासवर्ड"
    },
    "btn_auth_officer": {
        "en": "Authenticate Officer 🛡️",
        "hi": "अधिकारी प्रमाणित करें 🛡️"
    },

    # ── Citizen Login Page ───────────────────────────────────────────────────
    "citizen_login_title": {
        "en": "Citizen Land Tracker Login",
        "hi": "नागरिक भूमि ट्रैकर लॉगिन"
    },
    "citizen_login_sub": {
        "en": "Track your land acquisition status, compensation, and Section 24 rights",
        "hi": "अपनी भूमि अधिग्रहण स्थिति, मुआवजा और धारा 24 अधिकारों को ट्रैक करें"
    },
    "demo_citizen_btn": {
        "en": "⚡ 1-Click Demo Citizen Login (Instant Access)",
        "hi": "⚡ 1-क्लिक डेमो नागरिक लॉगिन (तत्काल पहुंच)"
    },
    "send_otp_btn": {
        "en": "📨 Send OTP",
        "hi": "📨 ओटीपी भेजें"
    },
    "verify_otp_btn": {
        "en": "✔️ Verify OTP",
        "hi": "✔️ ओटीपी सत्यापित करें"
    },
    "resend_otp_btn": {
        "en": "🔄 Resend OTP",
        "hi": "🔄 पुनः ओटीपी भेजें"
    },
    "enter_otp": {
        "en": "Enter 6-digit OTP",
        "hi": "6-अंकीय ओटीपी दर्ज करें"
    },
    "mobile_num": {
        "en": "Mobile Number (10 digits)",
        "hi": "मोबाइल नंबर (10 अंक)"
    },
    "email_addr": {
        "en": "Email Address",
        "hi": "ईमेल पता"
    },
    "welcome_citizen": {
        "en": "🌾 Welcome Citizen",
        "hi": "🌾 स्वागतम् नागरिक"
    },

    # ── Footer & Disclaimers ─────────────────────────────────────────────────
    "footer_prototype_note": {
        "en": "This is a Smart India Hackathon prototype (SIH26017). Data used is for demonstration purposes only. Governed by IT Act, 2000.",
        "hi": "यह स्मार्ट इंडिया हैकाथॉन प्रोटोटाइप (SIH26017) है। उपयोग किया गया डेटा केवल प्रदर्शन हेतु है। आईटी अधिनियम, 2000 द्वारा शासित।"
    }
}


# ─────────────────────────────────────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────────────────────────────────────

def get_current_lang() -> str:
    """Returns the current language code: 'en' or 'hi'."""
    # Check query params first if available
    if "lang" in st.query_params:
        q_lang = st.query_params.get("lang", "en").lower()
        if q_lang in ("en", "hi"):
            st.session_state["lang"] = q_lang
    return st.session_state.get("lang", "en")


def set_lang(lang: str) -> None:
    """Sets the active language ('en' or 'hi') in session state and query params."""
    if lang in ("en", "hi"):
        st.session_state["lang"] = lang
        st.query_params["lang"] = lang


def t(key: str, default: Optional[str] = None) -> str:
    """
    Translates a key into the active language ('en' or 'hi').
    Falls back to English text or the provided default if key is not found.
    """
    lang = get_current_lang()
    entry = TRANSLATIONS.get(key)
    if not entry:
        return default if default is not None else key
    return entry.get(lang, entry.get("en", default or key))


def render_language_toggle() -> None:
    """
    Renders an elegant language switcher button group in the UI.
    """
    current_lang = get_current_lang()
    col_en, col_hi = st.columns([1, 1])
    
    with col_en:
        btn_type = "primary" if current_lang == "en" else "secondary"
        if st.button("🇬🇧 English", key="_lang_btn_en", type=btn_type, use_container_width=True):
            set_lang("en")
            st.rerun()
            
    with col_hi:
        btn_type = "primary" if current_lang == "hi" else "secondary"
        if st.button("🇮🇳 हिन्दी", key="_lang_btn_hi", type=btn_type, use_container_width=True):
            set_lang("hi")
            st.rerun()

