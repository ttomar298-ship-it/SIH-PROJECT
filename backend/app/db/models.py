from sqlalchemy import Column, String, Integer, Float
from backend.app.db.database import Base

class ProjectModel(Base):
    __tablename__ = "projects"

    project_id = Column(String, primary_key=True, index=True)
    project_name = Column(String, index=True)
    state = Column(String, index=True)
    district = Column(String, index=True)
    stage = Column(String, index=True)
    start_date = Column(String)
    target_completion_date = Column(String)
    actual_or_projected_date = Column(String, nullable=True)
    planned_duration_days = Column(Integer)
    compensation_pct = Column(Float)
    legal_case = Column(Integer, default=0)
    rr_status = Column(String, default="Pending")
    affected_families = Column(Integer, default=0)
    budget_crores = Column(Float, default=0.0)
    latitude = Column(Float)
    longitude = Column(Float)
    delay_days = Column(Integer, default=0)
    delay_flag = Column(Integer, default=0)
    clr_completed_pct = Column(Float, default=97.5)
    sector = Column(String, default="Road Transport and Highways")
    cost_overrun_pct = Column(Float, default=0.0)

    def to_dict(self):
        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "state": self.state,
            "district": self.district,
            "stage": self.stage,
            "start_date": self.start_date,
            "target_completion_date": self.target_completion_date,
            "actual_or_projected_date": self.actual_or_projected_date,
            "planned_duration_days": self.planned_duration_days,
            "compensation_pct": self.compensation_pct,
            "legal_case": self.legal_case,
            "rr_status": self.rr_status,
            "affected_families": self.affected_families,
            "budget_crores": self.budget_crores,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "delay_days": self.delay_days,
            "delay_flag": self.delay_flag,
            "clr_completed_pct": self.clr_completed_pct or 97.5,
            "sector": self.sector or "Infrastructure",
            "cost_overrun_pct": self.cost_overrun_pct or 0.0
        }

