# Backward-compatibility alias for Home.py
import os
import runpy
import sys

# Ensure application directory and root are in sys.path
STREAMLIT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(STREAMLIT_DIR, "..", ".."))
for p in [STREAMLIT_DIR, ROOT_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

home_file = os.path.join(STREAMLIT_DIR, "Home.py")
runpy.run_path(home_file, run_name="__main__")
