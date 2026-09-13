import os
import sys
import uvicorn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if __name__ == "__main__":
    print("Starting SIH26017 FastAPI Server on http://127.0.0.1:8000 ...")
    uvicorn.run(
        "backend.app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=[os.path.join(BASE_DIR, "backend", "app")],
        reload_excludes=["*.db", "*.db-journal", "*.sqlite", "*.csv", "*.log", "projects.db*"]
    )
