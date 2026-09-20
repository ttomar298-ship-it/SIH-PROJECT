import sys
import os
import pytest
from fastapi.testclient import TestClient

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.app.main import app

def test_public_citizen_api_suite():
    with TestClient(app) as client:
        # 1. Anti-scraping check: Request without parameters must return HTTP 400
        res = client.get("/api/public/track")
        assert res.status_code == 400, f"Expected 400 on empty track request, got {res.status_code}: {res.text}"
        err_msg = res.json().get("detail", "")
        assert "Search query required" in err_msg or "Direct listing" in err_msg
        print("[PASS] 1. Anti-scraping guard rejects unparameterized requests with HTTP 400")

        # 2. Search by Khasra + Village
        res = client.get("/api/public/track", params={"khasra_number": "142/2", "village": "Danapur"})
        assert res.status_code == 200, f"Expected 200 on Khasra query, got {res.status_code}: {res.text}"
        data = res.json()

        # Verify whitelisted fields exist
        assert "project_id" in data
        assert "current_stage" in data
        assert "timeline_stages" in data
        assert len(data["timeline_stages"]) == 6, "Expected 6 RFCTLARR pipeline stages"
        assert "compensation" in data
        assert "parcel_info" in data
        assert "rr_details" in data

        # CRITICAL SECURITY ASSERTIONS: ZERO ML / OFFICER DATA LEAKAGE
        assert "risk_score" not in data, "Security violation: ML risk_score leaked in public endpoint!"
        assert "top_factors" not in data, "Security violation: SHAP top_factors leaked in public endpoint!"
        assert "action_recommendation" not in data, "Security violation: CALA action plan leaked in public endpoint!"
        assert "delay_probability" not in data, "Security violation: ML probability leaked in public endpoint!"
        assert "confidence_score" not in data, "Security violation: Model confidence leaked in public endpoint!"
        assert "budget_crores" not in data, "Internal budget figure exposed in citizen endpoint"

        # Privacy Name Masking Check
        parcel_info = data["parcel_info"]
        assert parcel_info is not None
        assert "Rameshwar Prasad Singh" not in parcel_info["landowner_masked_name"], "Landowner full name exposed without masking!"
        assert "***" in parcel_info["landowner_masked_name"], "Landowner name missing privacy asterisks!"
        print(f"[PASS] 2. Khasra search returned safe citizen data. Masked name: {parcel_info['landowner_masked_name']}")

        # 3. 100% Solatium Verification (Section 30(1))
        comp = data["compensation"]
        assert comp is not None
        assert comp["solatium_inr"] == comp["market_value_inr"], (
            f"Statutory mismatch: Solatium ₹{comp['solatium_inr']} does not equal Market Value ₹{comp['market_value_inr']}"
        )
        assert comp["total_compensation_inr"] >= comp["market_value_inr"] + comp["solatium_inr"]
        print(f"[PASS] 3. 100% Solatium verified: Market ₹{comp['market_value_inr']} + Solatium ₹{comp['solatium_inr']} = Total ₹{comp['total_compensation_inr']}")

        # 4. Search by Mobile Number
        res = client.get("/api/public/track", params={"mobile_number": "9876543210"})
        assert res.status_code == 200, f"Expected 200 on mobile query, got {res.status_code}: {res.text}"
        mob_data = res.json()
        assert mob_data["parcel_info"]["khasra_number"] == "142/2"
        print("[PASS] 4. Mobile number search successfully resolved parcel")

        # 5. Section 24 Lapsing Evaluation Test (Khasra 512/3 with award date > 5 years ago)
        res = client.get("/api/public/track", params={"khasra_number": "512/3", "village": "Rajarhat"})
        assert res.status_code == 200, f"Expected 200 on lapse query, got {res.status_code}: {res.text}"
        lapse_data = res.json()
        assert lapse_data["section_24_lapse_risk"] is True, "Section 24 lapse risk was not flagged for 5+ year old award!"
        assert "Section 24(2)" in lapse_data["section_24_details"], "Section 24 statutory reference missing from details!"
        print("[PASS] 5. Section 24(2) statutory lapse risk successfully flagged for 5+ year delayed parcel")

        # 6. Objection Filing (POST /api/public/objections)
        objection_payload = {
            "project_id": "PRJ-BI-1001",
            "parcel_id": "PARCEL-BI-002",
            "khasra_number": "89A",
            "village": "Phulwari",
            "district": "Patna",
            "citizen_name": "Sunita Kumari Devi",
            "mobile_number": "9811223344",
            "email": "sunita.claimant@example.com",
            "objection_category": "Compensation Dispute: Circle Rate / Solatium Calculation",
            "reason": "The notified circle rate of 2022 does not reflect the current commercial road-facing value. Requesting review under Section 15."
        }
        res = client.post("/api/public/objections", json=objection_payload)
        assert res.status_code == 201, f"Expected 201 Created on objection, got {res.status_code}: {res.text}"
        obj_res = res.json()
        assert obj_res["objection_id"].startswith("OBJ-2026-"), f"Invalid tracking ID format: {obj_res['objection_id']}"
        assert obj_res["status"] == "Submitted"
        assert obj_res["expected_resolution_days"] == 60
        assert "sms_status" in obj_res
        print(f"[PASS] 6. Objection successfully registered with Tracking ID: {obj_res['objection_id']}")

        # 7. Invalid objection validation
        invalid_payload = {
            "citizen_name": "A", # too short
            "mobile_number": "123", # too short
            "objection_category": "Compensation Dispute",
            "reason": "short" # too short
        }
        res = client.post("/api/public/objections", json=invalid_payload)
        assert res.status_code == 422, f"Expected 422 for invalid objection, got {res.status_code}"
        print("[PASS] 7. Pydantic validation rejected invalid objection submission with HTTP 422")

        print("\n========================================================")
        print("ALL 7 CITIZEN PUBLIC API CONTRACT & SECURITY TESTS PASSED!")
        print("========================================================")

if __name__ == "__main__":
    test_public_citizen_api_suite()

