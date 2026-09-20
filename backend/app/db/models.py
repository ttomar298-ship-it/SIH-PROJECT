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


class LandParcelModel(Base):
    __tablename__ = "land_parcels"

    parcel_id = Column(String, primary_key=True, index=True)
    project_id = Column(String, index=True)
    khasra_number = Column(String, index=True)
    village = Column(String, index=True)
    district = Column(String, index=True)
    state = Column(String, index=True)
    landowner_name = Column(String)
    mobile_number = Column(String, index=True)
    area_acres = Column(Float, default=0.0)
    land_type = Column(String, default="Agricultural")
    market_value_inr = Column(Float, default=0.0)
    solatium_inr = Column(Float, default=0.0)
    additional_multiplier_inr = Column(Float, default=0.0)
    total_compensation_inr = Column(Float, default=0.0)
    payment_status = Column(String, default="Pending")
    payment_disbursement_date = Column(String, nullable=True)
    expected_payment_date = Column(String, nullable=True)
    possession_status = Column(String, default="Pending")
    possession_date = Column(String, nullable=True)
    award_date = Column(String, nullable=True)
    objection_deadline = Column(String, nullable=True)
    objection_status = Column(String, default="Open")
    rr_entitlements = Column(String, default="Standard RFCTLARR Schedule II Package")

    def to_dict(self):
        return {
            "parcel_id": self.parcel_id,
            "project_id": self.project_id,
            "khasra_number": self.khasra_number,
            "village": self.village,
            "district": self.district,
            "state": self.state,
            "landowner_name": self.landowner_name,
            "mobile_number": self.mobile_number,
            "area_acres": self.area_acres,
            "land_type": self.land_type,
            "market_value_inr": self.market_value_inr,
            "solatium_inr": self.solatium_inr,
            "additional_multiplier_inr": self.additional_multiplier_inr,
            "total_compensation_inr": self.total_compensation_inr,
            "payment_status": self.payment_status,
            "payment_disbursement_date": self.payment_disbursement_date,
            "expected_payment_date": self.expected_payment_date,
            "possession_status": self.possession_status,
            "possession_date": self.possession_date,
            "award_date": self.award_date,
            "objection_deadline": self.objection_deadline,
            "objection_status": self.objection_status,
            "rr_entitlements": self.rr_entitlements
        }


class CitizenObjectionModel(Base):
    __tablename__ = "citizen_objections"

    objection_id = Column(String, primary_key=True, index=True)
    project_id = Column(String, index=True, nullable=True)
    parcel_id = Column(String, index=True, nullable=True)
    khasra_number = Column(String, index=True, nullable=True)
    village = Column(String, nullable=True)
    district = Column(String, nullable=True)
    citizen_name = Column(String)
    mobile_number = Column(String, index=True)
    email = Column(String, nullable=True)
    objection_category = Column(String)
    reason = Column(String)
    document_filename = Column(String, nullable=True)
    status = Column(String, default="Submitted")
    filed_at = Column(String)

    def to_dict(self):
        return {
            "objection_id": self.objection_id,
            "project_id": self.project_id,
            "parcel_id": self.parcel_id,
            "khasra_number": self.khasra_number,
            "village": self.village,
            "district": self.district,
            "citizen_name": self.citizen_name,
            "mobile_number": self.mobile_number,
            "email": self.email,
            "objection_category": self.objection_category,
            "reason": self.reason,
            "document_filename": self.document_filename,
            "status": self.status,
            "filed_at": self.filed_at
        }

