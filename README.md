# SIH26017 — Land Acquisition Delay Prediction & Risk Management System

[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-F7931E.svg)](https://scikit-learn.org)
[![Explainability](https://img.shields.io/badge/XAI-TreeSHAP-blue.svg)](https://shap.readthedocs.io)

An end-to-end intelligent decision-support platform designed for the **Smart India Hackathon (SIH26017)**. The system forecasts infrastructure project land acquisition delays, maps calibrated risk scores (1–100), visualizes geospatial GIS markers across India, generates explainable AI (SHAP) factor breakdowns, and dispatches automated priority alerts.

---

## 🏛️ System Architecture

```
                                  ┌────────────────────────┐
                                  │   Raw Data Generator   │
                                  │   (projects.csv)       │
                                  └───────────┬────────────┘
                                              │ Clean & Engineer
                                              ▼
                                  ┌────────────────────────┐
                                  │  Clean Processed Data  │
                                  │  (clean_data.csv)      │
                                  └─────┬────────────┬─────┘
                                        │            │
            ┌───────────────────────────┘            └───────────────────────────┐
            ▼                                                                    ▼
┌───────────────────────────────┐                                ┌───────────────────────────────┐
│     TEAM 1: BACKEND / ML      │                                │       SQLITE DATABASE         │
│  - RandomForest Classifier    │                                │  - SQLAlchemy Models          │
│  - RandomForest Regressor     │                                │  - Auto-seeded project store  │
│  - TreeSHAP Explainer         │                                └───────────────┬───────────────┘
│  - Calibrated Risk (1-100)    │                                                │
│  - Alert & Email Engine       │                                                │
└───────────────┬───────────────┘                                                │
                │                                                                │
                └───────────────────────────────┬────────────────────────────────┘
                                                ▼
                                ┌───────────────────────────────┐
                                │       TEAM 2: REST API        │
                                │   FastAPI + Pydantic Contract │
                                │   Endpoints: A1 to A8 + CORS  │
                                └───────────────┬───────────────┘
                                                │ REST / JSON
                                                ▼
                                ┌───────────────────────────────┐
                                │      TEAM 3: FRONTEND UI      │
                                │  Streamlit Multi-Page App     │
                                │  - GIS Folium Map             │
                                │  - SHAP Factor Breakdown      │
                                │  - Risk Leaderboard           │
                                │  - Project Milestone Timeline │
                                │  - Real-time Project Ingest   │
                                └───────────────────────────────┘
```

---

## 🚀 Quick Start Instructions

### 1. Prerequisites & Environment
Ensure Python 3.10+ is installed. Dependencies can be verified or installed via:
```bash
pip install -r requirements.txt
```

### 2. Run the FastAPI Backend
Launch the backend REST API server on port 8000:
```bash
python run_backend.py
```
- **Interactive Swagger Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Documentation:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **Health Check:** [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

### 3. Run the Streamlit Frontend Dashboard
In a second terminal, launch the Streamlit frontend:
```bash
python run_frontend.py
```
- **Web UI:** [http://localhost:8501](http://localhost:8501)

---

## 📑 Team Deliverables & Work Breakdown

### TEAM 1 — Backend (Data + ML)
| # | Deliverable | Path | Details |
|---|---|---|---|
| **B1** | Synthetic Raw Dataset | `backend/data/raw/projects.csv` | 200+ realistic infrastructure projects across Indian states |
| **B2** | Cleaned Dataset | `backend/data/processed/clean_data.csv` | Missing value imputation, calculated `delay_days` |
| **B3** | Feature Engineering | `backend/app/ml/feature_engineering.py` | Stage indices, compensation deficit, litigation flags |
| **B4** | RF Delay Classifier | `backend/models/delay_classifier.pkl` | 90% accuracy, predicts `delay_flag` |
| **B5** | RF Delay Regressor | `backend/models/delay_regressor.pkl` | Predicts `expected_delay_days` |
| **B6** | Evaluation Metrics | `backend/models/evaluation_report.json` | Accuracy, Precision, Recall, F1, RMSE, MAE, R² |
| **B7** | Calibrated Risk Scoring | `backend/app/ml/risk_scoring.py` | 1–100 calibrated score with Low/Medium/High bands |
| **B8** | TreeSHAP Explainability | `backend/app/ml/shap_explainer.py` | Top positive & negative contributing delay drivers |
| **B9** | Alert Engine | `backend/app/ml/alert_engine.py` | Threshold detection (score > 70) & bottleneck diagnostics |
| **B10** | Email Alert Service | `backend/app/ml/email_service.py` | Live SMTP + HTML simulation dispatch |

### TEAM 2 — REST API Endpoints
All endpoints enforce strict Pydantic schemas defined in `backend/app/schemas/project_schema.py`:
| # | Endpoint | Method | Response Payload Description |
|---|---|---|---|
| **A1** | `/projects` | GET | List of all monitored projects (supports `state` & `stage` filters) |
| **A2** | `/projects/{project_id}` | GET | Complete project metadata & milestone progress |
| **A3** | `/predict/{project_id}` | GET | `{ delay_flag, delay_label, expected_delay_days, confidence_score }` |
| **A4** | `/risk-score/{project_id}` | GET | `{ risk_score, risk_category, color_code, top_factors (SHAP) }` |
| **A5** | `/dashboard-data` | GET | High-performance aggregated metrics, risk bands, and project portfolio |
| **A6** | `/alerts` | GET | List of active warnings and critical alerts (`threshold=70`) |
| **A7** | `/projects` | POST | Ingest/evaluate new project record and return ML delay predictions |
| **A8** | `/gis-data` | GET | Latitude, longitude, risk score, and category for map markers |
| **Bonus**| `/alerts/send-email/{id}`| POST | Triggers priority email alert dispatch with HTML preview |

### TEAM 3 — Frontend Dashboard
| # | View | Description |
|---|---|---|
| **F1** | **Dashboard (Home)** | Executive KPI cards, stage distributions, risk pie chart, interactive table |
| **F2** | **Project Details** | Visual milestone pipeline (Stages 1–6), compensation progress bar, legal status |
| **F3** | **Risk Ranking** | Sorted leaderboard of projects by risk score (High → Low) with score sliders |
| **F4** | **SHAP Explanations** | Interactive Plotly horizontal bar chart showing top delay drivers |
| **F5** | **GIS Map** | Folium map with color-coded pins (Red=High, Amber=Medium, Green=Low) |
| **F6** | **Alerts Panel** | Priority alert cards, bottleneck diagnostics, and one-click email trigger |
| **F7** | **Add Project** | Real-time simulator to input project parameters and obtain live AI predictions |

---

## 🧪 Automated Verification & Testing
The system includes an automated test suite verifying all 8 API endpoints:
```bash
python -u tests/test_api.py
```
Expected output:
```
[PASS] /health is OK
[PASS] A1: GET /projects returned 201 records
[PASS] A2: GET /projects/{id} returned valid details
[PASS] A3: GET /predict/{id} -> Delay Flag & Expected Days
[PASS] A4: GET /risk-score/{id} -> Calibrated Score & SHAP Factors
[PASS] A5: GET /dashboard-data -> Aggregated Portfolio & Metrics
[PASS] A6: GET /alerts -> Active alerts stream
[PASS] A7: POST /projects -> Successfully created & evaluated
[PASS] A8: GET /gis-data -> Map markers with lat/long
ALL 8 API CONTRACT TESTS PASSED PERFECTLY!
```

#   S I H - P R O J E C T  
 