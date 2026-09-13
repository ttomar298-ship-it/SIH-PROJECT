import os
import re
import pandas as pd
import numpy as np
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW_DIR = os.path.join(BASE_DIR, "backend", "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "backend", "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

def parse_date_flexible(d_str):
    if not d_str or str(d_str).strip() in ["NA", "nan", ""]:
        return None
    d_str = str(d_str).strip()
    for fmt in ["%Y-%m-%d", "%B-%Y", "%b-%y", "%B-%y", "%b-%Y", "%Y/%m/%d"]:
        try:
            return datetime.strptime(d_str, fmt)
        except ValueError:
            pass
    return None

def build_enriched_dataset():
    # 1. Load DILRMP data
    dilrmp_path = os.path.join(RAW_DIR, "dilrmp_land_records.csv")
    df_dilrmp = pd.read_csv(dilrmp_path)
    # Clean state names
    state_clr_map = {}
    for _, row in df_dilrmp.iterrows():
        st_name = str(row["State/UT"]).strip().title()
        pct = float(row["Villages of CLR Completed (%)"])
        state_clr_map[st_name] = pct
        # Also handle common variants
        if "Andaman" in st_name or "Andman" in st_name:
            state_clr_map["Andaman and Nicobar Islands"] = pct
        elif "Delhi" in st_name:
            state_clr_map["Delhi"] = pct
        elif "Jammu" in st_name:
            state_clr_map["Jammu and Kashmir"] = pct

    default_clr = 97.5

    # 2. Load existing clean data
    clean_path = os.path.join(PROCESSED_DIR, "clean_data.csv")
    if os.path.exists(clean_path):
        df_existing = pd.read_csv(clean_path)
    else:
        df_existing = pd.read_csv(os.path.join(RAW_DIR, "projects.csv"))

    # Add CLR % to existing projects based on state
    df_existing["clr_completed_pct"] = df_existing["state"].apply(
        lambda s: state_clr_map.get(str(s).strip().title(), default_clr)
    )
    if "sector" not in df_existing.columns:
        df_existing["sector"] = "Road Transport and Highways"
    if "cost_overrun_pct" not in df_existing.columns:
        df_existing["cost_overrun_pct"] = 0.0

    # 3. Load and transform MoSPI Real Projects
    mospi_path = os.path.join(RAW_DIR, "mospi_real_projects.csv")
    df_mospi = pd.read_csv(mospi_path)
    
    mospi_records = []
    ap_clr = state_clr_map.get("Andhra Pradesh", 98.75)

    for idx, row in df_mospi.iterrows():
        p_id = f"PRJ-MOSPI-{2001 + idx}"
        name = str(row["name"])
        sector = str(row["sector"])
        district = str(row["district"])
        lat = float(row["lat"])
        lon = float(row["lon"])
        orig_cost = float(row["orig_cost"])
        rev_cost = float(row["rev_cost"])
        cost_overrun_pct = round(max(0.0, ((rev_cost - orig_cost) / orig_cost) * 100.0), 1)

        start_dt = parse_date_flexible(row["start"]) or datetime(2017, 1, 1)
        target_dt = parse_date_flexible(row["target"]) or datetime(2021, 1, 1)
        actual_dt = parse_date_flexible(row["actual"]) or (target_dt if target_dt > start_dt else datetime(2022, 1, 1))

        planned_days = max(90, (target_dt - start_dt).days)
        delay_days = max(0, (actual_dt - target_dt).days)
        delay_flag = 1 if delay_days > 30 else 0

        # Stage inference
        if delay_days > 365 or cost_overrun_pct > 50:
            stage = "Section 19 Declaration (R&R Scheme)"
            comp_pct = round(min(85.0, max(25.0, 100.0 - (delay_days / 15.0))), 1)
            legal_case = 1
            rr_status = "Pending" if cost_overrun_pct > 100 else "In Progress"
        elif delay_days > 60:
            stage = "Award of Compensation (Section 23/30)"
            comp_pct = round(min(90.0, max(50.0, 100.0 - (delay_days / 20.0))), 1)
            legal_case = 1 if idx % 2 == 0 else 0
            rr_status = "In Progress"
        else:
            stage = "Possession & Physical Transfer"
            comp_pct = 95.0
            legal_case = 0
            rr_status = "Completed"

        affected_families = int(min(6000, max(80, int(orig_cost * 1.5))))

        mospi_records.append({
            "project_id": p_id,
            "project_name": name,
            "state": "Andhra Pradesh",
            "district": district,
            "stage": stage,
            "start_date": start_dt.strftime("%Y-%m-%d"),
            "target_completion_date": target_dt.strftime("%Y-%m-%d"),
            "actual_or_projected_date": actual_dt.strftime("%Y-%m-%d"),
            "planned_duration_days": planned_days,
            "compensation_pct": comp_pct,
            "legal_case": legal_case,
            "rr_status": rr_status,
            "affected_families": affected_families,
            "budget_crores": rev_cost,
            "latitude": round(lat, 5),
            "longitude": round(lon, 5),
            "delay_days": delay_days,
            "delay_flag": delay_flag,
            "clr_completed_pct": ap_clr,
            "sector": sector,
            "cost_overrun_pct": cost_overrun_pct
        })

    df_mospi_clean = pd.DataFrame(mospi_records)

    # Filter existing to keep standard columns
    cols_to_keep = [
        "project_id", "project_name", "state", "district", "stage",
        "start_date", "target_completion_date", "actual_or_projected_date",
        "planned_duration_days", "compensation_pct", "legal_case",
        "rr_status", "affected_families", "budget_crores", "latitude",
        "longitude", "delay_days", "delay_flag", "clr_completed_pct",
        "sector", "cost_overrun_pct"
    ]

    # Combine datasets
    df_combined = pd.concat([df_existing[cols_to_keep], df_mospi_clean[cols_to_keep]], ignore_index=True)
    df_combined.drop_duplicates(subset=["project_id"], keep="last", inplace=True)

    # Save to clean_data.csv
    df_combined.to_csv(clean_path, index=False)
    print(f"Successfully created enriched clean_data.csv with {len(df_combined)} total projects!")
    print(f"  - Synthetic projects: {len(df_existing)}")
    print(f"  - Real MoSPI Infrastructure projects added: {len(df_mospi_clean)}")
    print(f"  - Integrated DILRMP state CLR % coverage: {len(state_clr_map)} States/UTs")

if __name__ == "__main__":
    build_enriched_dataset()

