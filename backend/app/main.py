import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.app.core.config import settings
from backend.app.db.crud import init_and_seed_db
from backend.app.api.routes import router as api_router
from backend.app.api.public_routes import router as public_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database and seed sample records
    print("[INFO] Initializing SQLite database and loading seed data...")
    init_and_seed_db()
    print("[INFO] Database ready. ML Models ready.")
    yield
    # Shutdown
    print("[INFO] Shutting down application...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FastAPI REST Backend for Land Acquisition Delay Prediction & Risk Management (SIH26017)",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(api_router, tags=["SIH26017 Core Endpoints"])
app.include_router(public_router, prefix="/api/public", tags=["Citizen Public Portal"])

@app.get("/", tags=["System"])
def root():
    return {
        "status": "online",
        "system": settings.PROJECT_NAME,
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": [
            "/projects",
            "/projects/{id}",
            "/predict/{id}",
            "/risk-score/{id}",
            "/dashboard-data",
            "/alerts",
            "/gis-data"
        ]
    }

@app.get("/health", tags=["System"])
def health():
    return {"status": "healthy", "service": "sih26017-backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)

