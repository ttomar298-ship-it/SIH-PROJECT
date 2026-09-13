from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ProjectBase(BaseModel):
    project_id: str = Field(..., description="Unique Project Identifier, e.g. PRJ-MH-1001")
    project_name: str = Field(..., description="Name of the infrastructure or land acquisition project")
    state: str = Field(..., description="State in India")
    district: str = Field(..., description="District name")
    stage: str = Field(..., description="Current land acquisition milestone stage")
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    target_completion_date: str = Field(..., description="Planned completion date (YYYY-MM-DD)")
    actual_or_projected_date: Optional[str] = Field(None, description="Actual or projected completion date (YYYY-MM-DD)")
    planned_duration_days: int = Field(..., description="Planned timeline duration in days")
    compensation_pct: float = Field(..., ge=0.0, le=100.0, description="Disbursed compensation % (0-100)")
    legal_case: int = Field(0, ge=0, le=1, description="Active court case / litigation flag (0 or 1)")
    rr_status: str = Field("Pending", description="Resettlement & Rehabilitation status (Pending, In Progress, Completed)")
    affected_families: int = Field(..., ge=0, description="Number of affected families")
    budget_crores: float = Field(..., ge=0.0, description="Project budget in INR Crores")
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    clr_completed_pct: Optional[float] = Field(97.5, description="State Land Records Computerization % (DILRMP)")
    sector: Optional[str] = Field("Infrastructure", description="Ministry or Sector")
    cost_overrun_pct: Optional[float] = Field(0.0, description="Cost overrun percentage")

class ProjectCreate(BaseModel):
    project_id: Optional[str] = None
    project_name: str
    state: str
    district: str
    stage: str
    start_date: str
    target_completion_date: str
    actual_or_projected_date: Optional[str] = None
    planned_duration_days: Optional[int] = 365
    compensation_pct: float = 0.0
    legal_case: int = 0
    rr_status: str = "Pending"
    affected_families: int = 50
    budget_crores: float = 250.0
    latitude: float = 20.5937
    longitude: float = 78.9629
    clr_completed_pct: Optional[float] = 97.5
    sector: Optional[str] = "Infrastructure"
    cost_overrun_pct: Optional[float] = 0.0

class ProjectResponse(ProjectBase):
    delay_days: Optional[int] = 0
    delay_flag: Optional[int] = 0

    class Config:
        from_attributes = True

class PredictionResponse(BaseModel):
    project_id: str
    delay_flag: int
    delay_label: str
    expected_delay_days: float
    delay_probability: float
    confidence_score: float

class ShapFactor(BaseModel):
    feature: str
    label: str
    shap_value: float
    impact: str
    description: str
    raw_value: float

class RiskScoreResponse(BaseModel):
    project_id: str
    risk_score: int
    risk_category: str
    color_code: str
    badge: str
    action_recommendation: str
    top_factors: List[ShapFactor]
    components: Optional[Dict[str, float]] = None

class DashboardSummaryResponse(BaseModel):
    total_projects: int
    delayed_projects_count: int
    delayed_projects_pct: float
    avg_risk_score: float
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    projects: List[Dict[str, Any]]

class AlertResponse(BaseModel):
    project_id: str
    project_name: str
    state: str
    district: str
    risk_score: int
    severity: str
    alert_count: int
    alert_messages: List[str]
    evaluated_at: str

class GISMarkerResponse(BaseModel):
    project_id: str
    project_name: str
    state: str
    district: str
    stage: str
    latitude: float
    longitude: float
    risk_score: int
    risk_category: str
    color_code: str
    delay_days: int
    legal_case: int
    compensation_pct: float
    sector: Optional[str] = "Infrastructure"
    budget_cr: Optional[float] = 0.0
    affected_families: Optional[int] = 0
    rr_status: Optional[str] = "In Progress"

