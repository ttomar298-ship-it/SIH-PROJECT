import os
import pandas as pd
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from backend.app.db.models import ProjectModel, LandParcelModel, CitizenObjectionModel
from backend.app.db.database import Base, engine, SessionLocal

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

SAMPLE_LAND_PARCELS = [
    {
        "parcel_id": "PARCEL-BI-001",
        "project_id": "PRJ-BI-1001",
        "khasra_number": "142/2",
        "village": "Danapur",
        "district": "Patna",
        "state": "Bihar",
        "landowner_name": "Rameshwar Prasad Singh",
        "mobile_number": "9876543210",
        "area_acres": 1.25,
        "land_type": "Agricultural (Irrigated Multi-crop)",
        "market_value_inr": 4500000.0,
        "solatium_inr": 4500000.0,
        "additional_multiplier_inr": 900000.0,
        "total_compensation_inr": 9900000.0,
        "payment_status": "Disbursed",
        "payment_disbursement_date": "2024-11-15",
        "expected_payment_date": "2024-11-15",
        "possession_status": "Physical Possession Taken",
        "possession_date": "2024-12-01",
        "award_date": "2024-06-20",
        "objection_deadline": "2024-08-20",
        "objection_status": "Closed",
        "rr_entitlements": "Constructed house in R&R Colony Danapur + ₹5,00,000 subsistence allowance + Cattle shed grant."
    },
    {
        "parcel_id": "PARCEL-BI-002",
        "project_id": "PRJ-BI-1001",
        "khasra_number": "89A",
        "village": "Phulwari",
        "district": "Patna",
        "state": "Bihar",
        "landowner_name": "Sunita Kumari Devi",
        "mobile_number": "9811223344",
        "area_acres": 0.75,
        "land_type": "Semi-Urban / Commercial",
        "market_value_inr": 6000000.0,
        "solatium_inr": 6000000.0,
        "additional_multiplier_inr": 1200000.0,
        "total_compensation_inr": 13200000.0,
        "payment_status": "Pending",
        "payment_disbursement_date": None,
        "expected_payment_date": "2026-04-30",
        "possession_status": "Notice Issued",
        "possession_date": None,
        "award_date": "2025-01-10",
        "objection_deadline": "2026-05-15",
        "objection_status": "Open",
        "rr_entitlements": "Commercial shop allotment in Transport Nagar + ₹3,00,000 resettlement grant + Livelihood skill training."
    },
    {
        "parcel_id": "PARCEL-UT-001",
        "project_id": "PRJ-UT-1002",
        "khasra_number": "204/1",
        "village": "Rohania",
        "district": "Varanasi",
        "state": "Uttar Pradesh",
        "landowner_name": "Kashi Nath Yadav",
        "mobile_number": "9922334455",
        "area_acres": 2.10,
        "land_type": "Agricultural (Unirrigated)",
        "market_value_inr": 7000000.0,
        "solatium_inr": 7000000.0,
        "additional_multiplier_inr": 1400000.0,
        "total_compensation_inr": 15400000.0,
        "payment_status": "Disbursed",
        "payment_disbursement_date": "2024-08-10",
        "expected_payment_date": "2024-08-10",
        "possession_status": "Physical Possession Taken",
        "possession_date": "2024-09-01",
        "award_date": "2024-02-15",
        "objection_deadline": "2024-04-15",
        "objection_status": "Closed",
        "rr_entitlements": "Lump sum resettlement assistance of ₹5,00,000 + Skill development voucher."
    },
    {
        "parcel_id": "PARCEL-WE-001",
        "project_id": "PRJ-WE-1007",
        "khasra_number": "512/3",
        "village": "Rajarhat",
        "district": "Kolkata",
        "state": "West Bengal",
        "landowner_name": "Debabrata Mukherjee",
        "mobile_number": "9733445566",
        "area_acres": 1.50,
        "land_type": "Agricultural",
        "market_value_inr": 5000000.0,
        "solatium_inr": 5000000.0,
        "additional_multiplier_inr": 1000000.0,
        "total_compensation_inr": 11000000.0,
        "payment_status": "Pending",
        "payment_disbursement_date": None,
        "expected_payment_date": "Overdue",
        "possession_status": "Pending",
        "possession_date": None,
        "award_date": "2019-01-15",
        "objection_deadline": "2019-03-15",
        "objection_status": "Closed",
        "rr_entitlements": "Schedule II R&R package verification pending."
    },
    {
        "parcel_id": "PARCEL-MA-001",
        "project_id": "PRJ-MA-1004",
        "khasra_number": "301/B",
        "village": "Bhiwandi Rural",
        "district": "Thane",
        "state": "Maharashtra",
        "landowner_name": "Balasaheb Patil",
        "mobile_number": "9820011223",
        "area_acres": 1.80,
        "land_type": "Agricultural",
        "market_value_inr": 8500000.0,
        "solatium_inr": 8500000.0,
        "additional_multiplier_inr": 1700000.0,
        "total_compensation_inr": 18700000.0,
        "payment_status": "Pending",
        "payment_disbursement_date": None,
        "expected_payment_date": "2026-06-30",
        "possession_status": "Pending",
        "possession_date": None,
        "award_date": None,
        "objection_deadline": "2026-04-10",
        "objection_status": "Open",
        "rr_entitlements": "Schedule II compensation + Annuity of ₹2,000/month for 20 years or lump sum ₹5 Lakhs."
    }
]

def init_and_seed_db():
    """
    Creates DB tables and seeds records from clean_data.csv and sample land parcels if empty.
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

        # Seed land parcels if table is empty
        parcel_count = db.query(LandParcelModel).count()
        if parcel_count == 0:
            for parcel_dict in SAMPLE_LAND_PARCELS:
                parcel = LandParcelModel(**parcel_dict)
                db.merge(parcel)
            db.commit()
            print(f"Database initialized and synchronized with {len(SAMPLE_LAND_PARCELS)} citizen land parcel records.")
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

def get_land_parcel(
    db: Session,
    project_id: Optional[str] = None,
    khasra_number: Optional[str] = None,
    village: Optional[str] = None,
    district: Optional[str] = None,
    mobile_number: Optional[str] = None
) -> Optional[LandParcelModel]:
    """
    Look up a land parcel by mobile, khasra + village/district, or project_id.
    """
    query = db.query(LandParcelModel)
    if mobile_number:
        clean_mob = mobile_number.strip().replace(" ", "").replace("-", "")
        # match last 10 digits
        if len(clean_mob) >= 10:
            clean_mob = clean_mob[-10:]
        parcel = query.filter(LandParcelModel.mobile_number.like(f"%{clean_mob}%")).first()
        if parcel:
            return parcel

    if khasra_number:
        q = query.filter(LandParcelModel.khasra_number.ilike(khasra_number.strip()))
        if village:
            q = q.filter(LandParcelModel.village.ilike(f"%{village.strip()}%"))
        if district:
            q = q.filter(LandParcelModel.district.ilike(f"%{district.strip()}%"))
        parcel = q.first()
        if parcel:
            return parcel

    if project_id:
        parcel = query.filter(LandParcelModel.project_id == project_id.strip()).first()
        if parcel:
            return parcel

    return None

def create_citizen_objection(db: Session, objection_dict: Dict[str, Any]) -> CitizenObjectionModel:
    objection = CitizenObjectionModel(**objection_dict)
    db.add(objection)
    db.commit()
    db.refresh(objection)
    return objection

def get_citizen_objection(db: Session, objection_id: str) -> Optional[CitizenObjectionModel]:
    return db.query(CitizenObjectionModel).filter(CitizenObjectionModel.objection_id == objection_id).first()


