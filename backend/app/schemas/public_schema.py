from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class CompensationBreakdown(BaseModel):
    market_value_inr: float = Field(..., description="Determined market value of the land parcel in INR")
    solatium_inr: float = Field(..., description="Mandatory 100% Solatium under Section 30(1) of RFCTLARR Act, 2013")
    additional_multiplier_inr: float = Field(0.0, description="Rural/Urban factor and standing crop/tree assets in INR")
    total_compensation_inr: float = Field(..., description="Total aggregate compensation in INR")
    payment_status: str = Field(..., description="Payment status: Disbursed, Pending, or In Escrow")
    disbursement_date: Optional[str] = Field(None, description="Date of fund disbursement if completed")
    expected_payment_date: Optional[str] = Field(None, description="Expected date of payment transfer")
    calculation_formula_note: str = Field(
        "Total = (Market Value × Location Multiplier) + 100% Solatium + Assets/Trees (RFCTLARR First Schedule)",
        description="Statutory reference for compensation calculation"
    )

class RRDetails(BaseModel):
    status: str = Field(..., description="Rehabilitation & Resettlement status")
    entitlements: str = Field(..., description="Entitlements under Schedule II of RFCTLARR Act, 2013")
    mandatory_provisions: str = Field(
        "Mandatory housing unit, subsistence grant for 12 months, and cattle shed/transport allowance.",
        description="Statutory guarantees"
    )

class StageProgress(BaseModel):
    stage_key: str
    stage_name_en: str
    stage_name_hi: str
    rfctlarr_section: str
    plain_english_description: str
    plain_hindi_description: str
    is_completed: bool
    is_current: bool

class CitizenParcelSummary(BaseModel):
    parcel_id: str
    khasra_number: str
    village: str
    district: str
    state: str
    landowner_masked_name: str
    area_acres: float
    land_type: str
    possession_status: str
    possession_date: Optional[str] = None
    objection_status: str

class PublicProjectStatus(BaseModel):
    project_id: str
    project_name: str
    state: str
    district: str
    current_stage: str
    current_stage_hi: str
    rfctlarr_stage_description: str
    rfctlarr_stage_description_hi: str
    timeline_stages: List[StageProgress]
    objection_window_open: bool
    objection_deadline: Optional[str] = None
    objection_instructions: str
    objection_instructions_hi: str
    parcel_info: Optional[CitizenParcelSummary] = None
    compensation: Optional[CompensationBreakdown] = None
    rr_details: Optional[RRDetails] = None
    section_24_lapse_risk: bool = False
    section_24_details: Optional[str] = None
    section_24_details_hi: Optional[str] = None
    last_updated: str
    disclaimer: str = (
        "Official Citizen Information Portal governed by the Right to Fair Compensation and "
        "Transparency in Land Acquisition, Rehabilitation and Resettlement Act, 2013 (RFCTLARR). "
        "This portal displays only verified statutory land records and compensation statuses."
    )

    model_config = ConfigDict(from_attributes=True)

class ObjectionCreate(BaseModel):
    project_id: Optional[str] = None
    parcel_id: Optional[str] = None
    khasra_number: Optional[str] = None
    village: Optional[str] = None
    district: Optional[str] = None
    citizen_name: str = Field(..., min_length=2, max_length=100)
    mobile_number: str = Field(..., min_length=10, max_length=15)
    email: Optional[str] = None
    objection_category: str = Field(..., description="Section 15 Hearing, Compensation Dispute, R&R Grievance, Possession Dispute, or Measurement/Boundary Error")
    reason: str = Field(..., min_length=10, max_length=2000)

class ObjectionResponse(BaseModel):
    objection_id: str
    status: str
    citizen_name: str
    mobile_number: str
    objection_category: str
    filed_at: str
    expected_resolution_days: int = 60
    message: str
    sms_status: str
    email_status: str

