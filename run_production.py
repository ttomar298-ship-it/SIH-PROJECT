import os
import sys
import subprocess
import time
import requests

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    port = os.getenv("PORT", "8501")
    
    env = os.environ.copy()
    existing_pp = env.get("PYTHONPATH", "")
    sep = ";" if sys.platform.startswith("win") else ":"
    st_app_dir = os.path.join(base_dir, "frontend", "streamlit_app")
    env["PYTHONPATH"] = f"{base_dir}{sep}{st_app_dir}{sep}{existing_pp}"
    env["API_BASE_URL"] = "http://127.0.0.1:8000"
    
    # Suppress Streamlit email prompt and configure server in environment
    env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    env["STREAMLIT_SERVER_HEADLESS"] = "true"
    env["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
    env["STREAMLIT_SERVER_PORT"] = str(port)
    env["STREAMLIT_SERVER_ENABLE_CORS"] = "false"
    env["STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION"] = "false"
    
    print("=========================================================")
    print("  BHOOMI AI (SIH26017) — PRODUCTION SERVICE RUNNER")
    print("=========================================================")
    print(f"Detected Platform: {sys.platform}")
    print(f"Target Public Port: {port}")
    
    # 1. Start FastAPI Backend in background on 127.0.0.1:8000
    print("\n[Step 1/2] Starting FastAPI backend on http://127.0.0.1:8000 ...")
    backend_proc = subprocess.Popen(
        [
            sys.executable, "-m", "uvicorn", "backend.app.main:app",
            "--host", "127.0.0.1",
            "--port", "8000",
            "--no-access-log"
        ],
        env=env
    )
    
    # Wait for backend health
    time.sleep(2)
    backend_ready = False
    for attempt in range(1, 15):
        try:
            r = requests.get("http://127.0.0.1:8000/health", timeout=1)
            if r.status_code == 200:
                print(f"  [PASS] FastAPI Backend is live and healthy! (Attempt {attempt})")
                backend_ready = True
                break
        except Exception:
            time.sleep(1)
            
    if not backend_ready:
        print("  [WARN] Backend taking longer to initialize; proceeding with frontend startup...")

    # 2. Start Streamlit Frontend on public Render port
    app_path = os.path.join(base_dir, "frontend", "streamlit_app", "app.py")
    print(f"\n[Step 2/2] Starting Streamlit frontend on port {port} (0.0.0.0) ...")
    frontend_cmd = [
        sys.executable, "-m", "streamlit", "run", app_path,
        "--server.port", str(port),
        "--server.address", "0.0.0.0",
        "--server.headless", "true"
    ]
    
    try:
        subprocess.run(frontend_cmd, env=env, check=True)
    except KeyboardInterrupt:
        print("\nShutdown requested by user.")
    finally:
        print("Terminating backend process...")
        backend_proc.terminate()
        try:
            backend_proc.wait(timeout=3)
        except Exception:
            backend_proc.kill()
        print("Shutdown complete.")

if __name__ == "__main__":
    main()
