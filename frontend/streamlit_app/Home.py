import sys
import os
import streamlit as st

# Ensure application directory and root are in sys.path
STREAMLIT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(STREAMLIT_DIR, "..", ".."))
for p in [STREAMLIT_DIR, ROOT_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

LOGO_PATH = os.path.join(STREAMLIT_DIR, "assets", "logo.png")

try:
    from utils.gov_theme import (
        apply_gov_theme,
        hide_default_sidebar_nav,
        render_role_selection_landing,
        render_gov_footer,
    )
except ImportError:
    from frontend.streamlit_app.utils.gov_theme import (
        apply_gov_theme,
        hide_default_sidebar_nav,
        render_role_selection_landing,
        render_gov_footer,
    )

st.set_page_config(
    page_title="BHOOMI AI — PM GatiShakti Land Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_gov_theme()
hide_default_sidebar_nav()
render_role_selection_landing(logo_path=LOGO_PATH)
render_gov_footer()
