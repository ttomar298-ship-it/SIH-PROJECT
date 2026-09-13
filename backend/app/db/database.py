import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DB_PATH = os.path.join(BASE_DIR, "backend", "app", "db", "projects.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Normalize SQLite path for cross-platform and Windows compatibility
normalized_db_path = DB_PATH.replace(os.sep, "/")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{normalized_db_path}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
