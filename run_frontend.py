import sys
import subprocess
import os

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(base_dir, "frontend", "streamlit_app", "Home.py")
    st_app_dir = os.path.join(base_dir, "frontend", "streamlit_app")
    
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{base_dir};{st_app_dir};{existing_pythonpath}"
    
    print(f"Launching Streamlit App from {app_path}...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", app_path, "--server.port=8501"], env=env)
