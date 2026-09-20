import random
import re
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.db.models import LandParcelModel, ProjectModel
from backend.app.db.crud import (
    get_land_parcel,
    get_project_by_id,
    create_citizen_objection
)
from backend.app.schemas.public_schema import (
    PublicProjectStatus,
    CitizenParcelSummary,
    CompensationBreakdown,
    RRDetails,
    StageProgress,
    ObjectionCreate,
    ObjectionResponse
)
from backend.app.ml.email_service import get_email_service

router = APIRouter()

# Rate limiting / Scraping guard: Simple in-memory tracker (requests per IP per minute)
_RATE_LIMIT_CACHE: Dict[str, List[float]] = {}
RATE_LIMIT_MAX_REQUESTS = 60
RATE_LIMIT_WINDOW_SECONDS = 60.0

def enforce_rate_limit(request: Request):
    """
    Prevents mass scraping of citizen land records by limiting request frequency.
    """
    client_ip = request.client.host if request.client else "unknown_ip"
    now = datetime.now().timestamp()
    timestamps = _RATE_LIMIT_CACHE.get(client_ip, [])
    # Evict older than window
    timestamps = [ts for ts in timestamps if now - ts < RATE_LIMIT_WINDOW_SECONDS]
    if len(timestamps) >= RATE_LIMIT_MAX_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Citizen tracker allows up to 60 queries per minute to safeguard data privacy."
        )
    timestamps.append(now)
    _RATE_LIMIT_CACHE[client_ip] = timestamps

def mask_name(full_name: str) -> str:
    """
    Masks citizen names to protect personal identity (e.g., 'Rameshwar Prasad Singh' -> 'R*** P*** S***').
    """
    if not full_name:
        return "Landowner (Verified)"
    parts = full_name.strip().split()
    masked = []
    for p in parts:
        if len(p) > 1:
            masked.append(f"{p[0]}***")
        else:
            masked.append(p)
    return " ".join(masked)

RFCTLARR_STAGES = [
    {
        "key": "SIA",
        "name_en": "Social Impact Assessment (SIA)",
        "name_hi": "सामाजिक प्रभाव आकलन (एसआईए)",
        "section": "Section 4",
        "desc_en": "Independent study evaluating public utility, livelihood impact, and affected families with Gram Sabha participation.",
        "desc_hi": "ग्राम सभा की भागीदारी के साथ जनहित उपयोगिता, आजीविका प्रभाव व प्रभावित परिवारों का स्वतंत्र मूल्यांकन अध्ययन।"
    },
    {
        "key": "SECTION_11",
        "name_en": "Preliminary Notification",
        "name_hi": "प्रारंभिक अधिसूचना",
        "section": "Section 11",
        "desc_en": "Official Gazette notice declaring government intention to acquire specified land parcels. Land sale/transfer restricted.",
        "desc_hi": "भूमि अधिग्रहण की सरकारी मंशा प्रकट करने वाला राजपत्र प्रकाशन। क्षेत्र में भूमि के विक्रय/हस्तांतरण पर रोक।"
    },
    {
        "key": "SECTION_15",
        "name_en": "Hearing of Objections",
        "name_hi": "आपत्तियों की सुनवाई",
        "section": "Section 15",
        "desc_en": "60-day statutory window for landowners to lodge objections on public purpose, area survey, or land suitability before CALA.",
        "desc_hi": "भूस्वामियों को जन-उद्देश्य, क्षेत्रफल पैमाइश अथवा भूमि उपयोगिता पर सीएएलए के समक्ष आपत्ति दर्ज करने हेतु 60 दिनों का अवसर।"
    },
    {
        "key": "SECTION_19",
        "name_en": "Declaration of Acquisition & R&R",
        "name_hi": "अधिग्रहण की घोषणा व पुनर्वास योजना",
        "section": "Section 19",
        "desc_en": "Final declaration published alongside the approved Rehabilitation & Resettlement (R&R) scheme summary.",
        "desc_hi": "स्वीकृत पुनर्वास एवं पुनर्व्यवस्था (आर एंड आर) योजना के सारांश के साथ अंतिम अधिग्रहण घोषणा का प्रकाशन।"
    },
    {
        "key": "SECTION_23_30",
        "name_en": "Award Determination & 100% Solatium",
        "name_hi": "मुआवजा निर्धारण व 100% तोषणा",
        "section": "Section 23 & 30",
        "desc_en": "Formal compensation award fixed: Market Value × Multiplier + mandatory 100% Solatium under Section 30(1).",
        "desc_hi": "औपचारिक मुआवजा निर्धारण: बाजार मूल्य × ग्रामीण/शहरी गुणक + धारा 30(1) के तहत अनिवार्य 100% तोषणा (Solatium)।"
    },
    {
        "key": "SECTION_38",
        "name_en": "Physical Possession & Full Payment",
        "name_hi": "भौतिक कब्जा व पूर्ण भुगतान",
        "section": "Section 38",
        "desc_en": "Statutory rule: Full monetary compensation and R&R entitlements must be credited to bank accounts before physical possession is taken.",
        "desc_hi": "वैधानिक नियम: भूमि का भौतिक कब्जा लेने से पूर्व भूस्वामी के खाते में संपूर्ण मुआवजा व आर एंड आर अंतरण अनिवार्य।"
    }
]

def map_stage_to_index(stage_text: str) -> int:
    """
    Maps an internal project stage string to the 0-5 index of canonical RFCTLARR stages.
    """
    s = (stage_text or "").lower()
    if "sia" in s or "social" in s:
        return 0
    elif "11" in s or "preliminary" in s or "section 4" in s:
        return 1
    elif "15" in s or "objection" in s or "hearing" in s:
        return 2
    elif "19" in s or "declaration" in s:
        return 3
    elif "award" in s or "23" in s or "30" in s or "solatium" in s:
        return 4
    elif "38" in s or "possession" in s or "disbursement" in s:
        return 5
    return 2 # default to intermediate hearing stage if uncertain

def calculate_section_24_lapse(parcel: Optional[LandParcelModel]) -> tuple[bool, Optional[str], Optional[str]]:
    """
    Computes Section 24(2) lapse risk:
    Where an award was made 5 years or more prior, and physical possession
    has not been taken OR compensation has not been paid, the acquisition
    proceedings are deemed to have lapsed under Section 24(2) of RFCTLARR Act, 2013.
    """
    if not parcel or not parcel.award_date:
        return False, None, None

    try:
        award_dt = datetime.strptime(parcel.award_date.strip(), "%Y-%m-%d").date()
        today = date.today()
        years_diff = (today - award_dt).days / 365.25
        
        possession_pending = (parcel.possession_status != "Physical Possession Taken")
        payment_pending = (parcel.payment_status != "Disbursed")

        if years_diff >= 5.0 and (possession_pending or payment_pending):
            details_en = (
                f"Statutory Notice under Section 24(2) of the RFCTLARR Act, 2013: "
                f"The compensation award was declared on {parcel.award_date} ({years_diff:.1f} years ago). "
                f"Because {'physical possession has not been taken' if possession_pending else 'compensation has not been disbursed'}, "
                f"the acquisition proceedings may be legally deemed to have lapsed. "
                f"Landowners retain the right to petition the High Court or CALA for fresh determination."
            )
            details_hi = (
                f"RFCTLARR अधिनियम, 2013 की धारा 24(2) के तहत वैधानिक सूचना: "
                f"मुआवजा निर्धारण (अवार्ड) {parcel.award_date} को ({years_diff:.1f} वर्ष पूर्व) घोषित हुआ था। "
                f"चूंकि {'भौतिक कब्जा नहीं लिया गया है' if possession_pending else 'मुआवजा भुगतान अभी तक लंबित है'}, "
                f"अधिग्रहण प्रक्रिया कानूनन व्यपगत (Lapsed) मानी जा सकती है। "
                f"भूस्वामी उच्च न्यायालय या सीएएलए के समक्ष नवीन निर्धारण हेतु आवेदन करने का वैधानिक अधिकार रखते हैं।"
            )
            return True, details_en, details_hi
    except Exception:
        pass

    return False, None, None


@router.get(
    "/track",
    response_model=PublicProjectStatus,
    summary="Track Land Acquisition Status for Citizens (Whitelisted Public Schema)",
    description="Public citizen-safe query endpoint. Requires specific parcel or project parameters. ML risk scores, SHAP values, and officer notes are strictly omitted."
)
def track_citizen_status(
    request: Request,
    project_id: Optional[str] = Query(None, description="Unique Project ID e.g. PRJ-BI-1001"),
    khasra_number: Optional[str] = Query(None, description="Survey / Khasra number e.g. 142/2"),
    village: Optional[str] = Query(None, description="Village name e.g. Danapur"),
    district: Optional[str] = Query(None, description="District name e.g. Patna"),
    mobile_number: Optional[str] = Query(None, description="Landowner 10-digit mobile number"),
    db: Session = Depends(get_db)
):
    enforce_rate_limit(request)

    # 1. Scraping Guard: Require at least one specific lookup criterion
    has_project = bool(project_id and project_id.strip())
    has_khasra = bool(khasra_number and khasra_number.strip())
    has_mobile = bool(mobile_number and mobile_number.strip())

    if not (has_project or has_khasra or has_mobile):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Search query required. Please specify a Khasra/Survey Number with Village/District, "
                "or a Registered Mobile Number, or a Project ID. Direct listing of projects is disabled "
                "to protect citizen privacy."
            )
        )

    # 2. Query land parcel if Khasra, Mobile, or Project is provided
    parcel = get_land_parcel(
        db=db,
        project_id=project_id,
        khasra_number=khasra_number,
        village=village,
        district=district,
        mobile_number=mobile_number
    )

    # 3. Retrieve linked ProjectModel
    resolved_proj_id = parcel.project_id if parcel else (project_id.strip() if project_id else None)
    project = get_project_by_id(db, resolved_proj_id) if resolved_proj_id else None

    if not parcel and not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No land acquisition record found matching your query. Please check the Khasra number, Village, or Project ID."
        )

    # Project meta attributes
    proj_name = project.project_name if project else "National Infrastructure Project"
    proj_state = project.state if project else (parcel.state if parcel else "India")
    proj_district = project.district if project else (parcel.district if parcel else "District")
    proj_stage = project.stage if project else "Award of Compensation (Section 23/30)"

    curr_stage_idx = map_stage_to_index(proj_stage)
    curr_rfctlarr = RFCTLARR_STAGES[curr_stage_idx]

    # Build timeline stages
    timeline_stages: List[StageProgress] = []
    for idx, s in enumerate(RFCTLARR_STAGES):
        timeline_stages.append(
            StageProgress(
                stage_key=s["key"],
                stage_name_en=s["name_en"],
                stage_name_hi=s["name_hi"],
                rfctlarr_section=s["section"],
                plain_english_description=s["desc_en"],
                plain_hindi_description=s["desc_hi"],
                is_completed=(idx < curr_stage_idx),
                is_current=(idx == curr_stage_idx)
            )
        )

    # Section 24 Lapsing Evaluation
    sec24_risk, sec24_en, sec24_hi = calculate_section_24_lapse(parcel)

    # Objection window logic
    objection_open = False
    objection_deadline = None
    if parcel and parcel.objection_status == "Open":
        objection_open = True
        objection_deadline = parcel.objection_deadline or "Open for Hearing"
    elif curr_stage_idx in [1, 2]: # Section 11 or Section 15
        objection_open = True
        objection_deadline = parcel.objection_deadline if parcel else "Within 60 days of Preliminary Notification"

    if objection_open:
        obj_instr_en = (
            "The statutory 60-day objection window under Section 15 of RFCTLARR Act, 2013 is currently OPEN. "
            "You may submit an objection regarding land measurement, suitability, or public purpose through this portal."
        )
        obj_instr_hi = (
            "RFCTLARR अधिनियम, 2013 की धारा 15 के तहत 60 दिवसीय वैधानिक आपत्ति दर्ज करने की विंडो वर्तमान में खुली है। "
            "आप इस पोर्टल के माध्यम से भूमि माप, उपयुक्तता या जन-उद्देश्य के संबंध में अपनी आपत्ति दर्ज कर सकते हैं।"
        )
    else:
        obj_instr_en = (
            f"The Section 15 objection window is currently CLOSED for this parcel (Status: {parcel.objection_status if parcel else 'Concluded'}). "
            "Grievances regarding compensation disbursement or R&R entitlements may still be submitted to CALA."
        )
        obj_instr_hi = (
            f"इस भूखंड के लिए धारा 15 आपत्ति विंडो समाप्त हो चुकी है (स्थिति: {parcel.objection_status if parcel else 'समाप्त'})। "
            "मुआवजा वितरण अथवा पुनर्वास लाभों के संबंध में शिकायतें अभी भी सीएएलए को प्रेषित की जा सकती हैं।"
        )

    # Parcel & Compensation models
    parcel_summary: Optional[CitizenParcelSummary] = None
    comp_breakdown: Optional[CompensationBreakdown] = None
    rr_details: Optional[RRDetails] = None

    if parcel:
        parcel_summary = CitizenParcelSummary(
            parcel_id=parcel.parcel_id,
            khasra_number=parcel.khasra_number,
            village=parcel.village,
            district=parcel.district,
            state=parcel.state,
            landowner_masked_name=mask_name(parcel.landowner_name),
            area_acres=parcel.area_acres,
            land_type=parcel.land_type,
            possession_status=parcel.possession_status,
            possession_date=parcel.possession_date,
            objection_status=parcel.objection_status
        )

        comp_breakdown = CompensationBreakdown(
            market_value_inr=parcel.market_value_inr,
            solatium_inr=parcel.solatium_inr,
            additional_multiplier_inr=parcel.additional_multiplier_inr,
            total_compensation_inr=parcel.total_compensation_inr,
            payment_status=parcel.payment_status,
            disbursement_date=parcel.payment_disbursement_date,
            expected_payment_date=parcel.expected_payment_date
        )

        rr_details = RRDetails(
            status=project.rr_status if project else "In Progress",
            entitlements=parcel.rr_entitlements
        )

    return PublicProjectStatus(
        project_id=resolved_proj_id or "N/A",
        project_name=proj_name,
        state=proj_state,
        district=proj_district,
        current_stage=curr_rfctlarr["name_en"],
        current_stage_hi=curr_rfctlarr["name_hi"],
        rfctlarr_stage_description=curr_rfctlarr["desc_en"],
        rfctlarr_stage_description_hi=curr_rfctlarr["desc_hi"],
        timeline_stages=timeline_stages,
        objection_window_open=objection_open,
        objection_deadline=objection_deadline,
        objection_instructions=obj_instr_en,
        objection_instructions_hi=obj_instr_hi,
        parcel_info=parcel_summary,
        compensation=comp_breakdown,
        rr_details=rr_details,
        section_24_lapse_risk=sec24_risk,
        section_24_details=sec24_en,
        section_24_details_hi=sec24_hi,
        last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


@router.post(
    "/objections",
    response_model=ObjectionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="File a Citizen Objection or Grievance (RFCTLARR Section 15)",
    description="Allows affected landowners to lodge formal objections. Generates an official tracking ID and dispatches acknowledgement email and SMS stub."
)
def submit_citizen_objection(
    payload: ObjectionCreate,
    db: Session = Depends(get_db)
):
    # Generate official tracking ID
    year = datetime.now().year
    rand_suffix = random.randint(1000, 9999)
    objection_id = f"OBJ-{year}-{rand_suffix}"
    filed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    objection_data = {
        "objection_id": objection_id,
        "project_id": payload.project_id,
        "parcel_id": payload.parcel_id,
        "khasra_number": payload.khasra_number,
        "village": payload.village,
        "district": payload.district,
        "citizen_name": payload.citizen_name.strip(),
        "mobile_number": payload.mobile_number.strip(),
        "email": payload.email.strip() if payload.email else None,
        "objection_category": payload.objection_category,
        "reason": payload.reason.strip(),
        "document_filename": None,
        "status": "Submitted",
        "filed_at": filed_at
    }

    # Save to database
    create_citizen_objection(db, objection_data)

    # Dispatch email & SMS receipts
    email_service = get_email_service()
    email_res = email_service.send_citizen_objection_receipt(objection_data)
    
    sms_text = (
        f"Dear {payload.citizen_name}, your grievance {objection_id} regarding Khasra {payload.khasra_number or 'N/A'} "
        f"has been officially registered with CALA. Expected review within 60 days under RFCTLARR Sec 15."
    )
    sms_res = email_service.send_sms_notification(payload.mobile_number, sms_text)

    return ObjectionResponse(
        objection_id=objection_id,
        status="Submitted",
        citizen_name=payload.citizen_name,
        mobile_number=payload.mobile_number,
        objection_category=payload.objection_category,
        filed_at=filed_at,
        expected_resolution_days=60,
        message=(
            f"Objection successfully lodged under Section 15 of RFCTLARR Act, 2013. "
            f"Your tracking reference is {objection_id}. The Competent Authority (CALA) is mandated "
            f"to schedule a hearing and resolve this submission within 60 days."
        ),
        sms_status=sms_res.get("status", "sent"),
        email_status=email_res.get("status", "skipped")
    )

