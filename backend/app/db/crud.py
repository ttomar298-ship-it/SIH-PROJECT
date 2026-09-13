import os
import pandas as pd
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from backend.app.db.models import ProjectModel
from backend.app.db.database import Base, engine, SessionLocal

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

def init_and_seed_db():
    """
    Creates DB tables and seeds records from clean_data.csv if the database table is empty.
    """
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        count = db.query(ProjectModel).count()
        if count == 0:
            csv_path = os.path.join(BASE_DIR, "backend", "data", "processed", "clean_data.csv")
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                for _, row in df.iterrows():
                    proj = ProjectModel(
                        project_id=str(row["project_id"]),
                        project_name=str(row["project_name"]),
                        state=str(row["state"]),
                        district=str(row["district"]),
                        stage=str(row["stage"]),
                        start_date=str(row["start_date"]),
                        target_completion_date=str(row["target_completion_date"]),
                        actual_or_projected_date=str(row.get("actual_or_projected_date", "")),
                        planned_duration_days=int(row["planned_duration_days"]),
                        compensation_pct=float(row["compensation_pct"]),
                        legal_case=int(row["legal_case"]),
                        rr_status=str(row["rr_status"]),
                        affected_families=int(row["affected_families"]),
                        budget_crores=float(row["budget_crores"]),
                        latitude=float(row["latitude"]),
                        longitude=float(row["longitude"]),
                        delay_days=int(row["delay_days"]),
                        delay_flag=int(row["delay_flag"]),
                        clr_completed_pct=float(row.get("clr_completed_pct", 97.5)),
                        sector=str(row.get("sector", "Infrastructure")),
                        cost_overrun_pct=float(row.get("cost_overrun_pct", 0.0)),
                    )
                    db.merge(proj)
                db.commit()
                print(f"Database initialized and synchronized with {len(df)} project records.")
    finally:
        db.close()

def get_projects(
    db: Session,
    state: Optional[str] = None,
    stage: Optional[str] = None,
    skip: int = 0,
    limit: int = 1000
) -> List[ProjectModel]:
    query = db.query(ProjectModel)
    if state and state.lower() != "all":
        query = query.filter(ProjectModel.state.ilike(f"%{state}%"))
    if stage and stage.lower() != "all":
        query = query.filter(ProjectModel.stage.ilike(f"%{stage}%"))
    return query.offset(skip).limit(limit).all()

def get_project_by_id(db: Session, project_id: str) -> Optional[ProjectModel]:
    return db.query(ProjectModel).filter(ProjectModel.project_id == project_id).first()

def create_or_update_project(db: Session, project_dict: Dict[str, Any]) -> ProjectModel:
    project_id = project_dict.get("project_id")
    existing = db.query(ProjectModel).filter(ProjectModel.project_id == project_id).first()
    if existing:
        for key, value in project_dict.items():
            if hasattr(existing, key):
                setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        return existing
    else:
        new_project = ProjectModel(**project_dict)
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        return new_project

