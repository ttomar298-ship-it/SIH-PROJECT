import os
import requests
from typing import Dict, Any, List, Optional

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

class APIClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip("/")

    def check_health(self) -> bool:
        try:
            res = requests.get(f"{self.base_url}/health", timeout=3)
            return res.status_code == 200
        except Exception:
            return False

    def get_dashboard_data(self) -> Dict[str, Any]:
        url = f"{self.base_url}/dashboard-data"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()

    def get_projects(self, state: Optional[str] = None, stage: Optional[str] = None) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/projects"
        params = {}
        if state and state != "All":
            params["state"] = state
        if stage and stage != "All":
            params["stage"] = stage
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        return res.json()

    def get_project(self, project_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/projects/{project_id}"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()

    def get_prediction(self, project_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/predict/{project_id}"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()

    def get_risk_score(self, project_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/risk-score/{project_id}"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()

    def get_alerts(self, threshold: int = 70) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/alerts"
        res = requests.get(url, params={"threshold": threshold}, timeout=10)
        res.raise_for_status()
        return res.json()

    def get_gis_data(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/gis-data"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()

    def create_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/projects"
        res = requests.post(url, json=project_data, timeout=10)
        res.raise_for_status()
        return res.json()

    def send_alert_email(self, project_id: str, recipient: Optional[str] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/alerts/send-email/{project_id}"
        params = {"recipient": recipient} if recipient else {}
        res = requests.post(url, params=params, timeout=10)
        res.raise_for_status()
        return res.json()

    def get_dilrmp_data(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/dilrmp-data"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()

    def get_model_metrics(self) -> Dict[str, Any]:
        try:
            url = f"{self.base_url}/model-metrics"
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                return res.json()
        except Exception:
            pass

        # Fallback to local evaluation_report.json file if API is unreachable
        local_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend", "models", "evaluation_report.json"))
        if os.path.exists(local_path):
            try:
                import json
                with open(local_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def track_citizen_status(
        self,
        project_id: Optional[str] = None,
        khasra_number: Optional[str] = None,
        village: Optional[str] = None,
        district: Optional[str] = None,
        mobile_number: Optional[str] = None
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/api/public/track"
        params = {}
        if project_id:
            params["project_id"] = project_id.strip()
        if khasra_number:
            params["khasra_number"] = khasra_number.strip()
        if village:
            params["village"] = village.strip()
        if district:
            params["district"] = district.strip()
        if mobile_number:
            params["mobile_number"] = mobile_number.strip()
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        return res.json()

    def submit_citizen_objection(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/api/public/objections"
        res = requests.post(url, json=payload, timeout=10)
        res.raise_for_status()
        return res.json()

# Global client singleton
client = APIClient()


