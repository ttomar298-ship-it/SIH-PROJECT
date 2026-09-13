import os
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seeds for reproducibility
random.seed(42)
np.random.seed(42)

# Indian States, Districts, and Representative Coordinates (Lat, Long)
LOCATIONS = [
    {"state": "Maharashtra", "district": "Pune", "lat": 18.5204, "lon": 73.8567},
    {"state": "Maharashtra", "district": "Nagpur", "lat": 21.1458, "lon": 79.0882},
    {"state": "Maharashtra", "district": "Thane", "lat": 19.2183, "lon": 72.9781},
    {"state": "Gujarat", "district": "Ahmedabad", "lat": 23.0225, "lon": 72.5714},
    {"state": "Gujarat", "district": "Surat", "lat": 21.1702, "lon": 72.8311},
    {"state": "Gujarat", "district": "Vadodara", "lat": 22.3072, "lon": 73.1812},
    {"state": "Uttar Pradesh", "district": "Varanasi", "lat": 25.3176, "lon": 82.9739},
    {"state": "Uttar Pradesh", "district": "Lucknow", "lat": 26.8467, "lon": 80.9462},
    {"state": "Uttar Pradesh", "district": "Kanpur", "lat": 26.4499, "lon": 80.3319},
    {"state": "Tamil Nadu", "district": "Chennai", "lat": 13.0827, "lon": 80.2707},
    {"state": "Tamil Nadu", "district": "Coimbatore", "lat": 11.0168, "lon": 76.9558},
    {"state": "Karnataka", "district": "Bengaluru Urban", "lat": 12.9716, "lon": 77.5946},
    {"state": "Karnataka", "district": "Mysuru", "lat": 12.2958, "lon": 76.6394},
    {"state": "Odisha", "district": "Bhubaneswar", "lat": 20.2961, "lon": 85.8245},
    {"state": "Odisha", "district": "Sambalpur", "lat": 21.4669, "lon": 83.9812},
    {"state": "Rajasthan", "district": "Jaipur", "lat": 26.9124, "lon": 75.7873},
    {"state": "Rajasthan", "district": "Jodhpur", "lat": 26.2389, "lon": 73.0243},
    {"state": "Andhra Pradesh", "district": "Visakhapatnam", "lat": 17.6868, "lon": 83.2185},
    {"state": "West Bengal", "district": "Kolkata", "lat": 22.5726, "lon": 88.3639},
    {"state": "Madhya Pradesh", "district": "Bhopal", "lat": 23.2599, "lon": 77.4126},
    {"state": "Bihar", "district": "Patna", "lat": 25.5941, "lon": 85.1376},
]

PROJECT_TYPES = [
    "National Highway Expansion",
    "High-Speed Rail Corridor",
    "Expressway Link Road",
    "Dedicated Freight Corridor",
    "Metro Rail Phase-II",
    "Industrial Corridor Node",
    "Multi-Modal Logistics Park",
    "Greenfield Airport Access Highway",
    "River Valley Hydro Irrigation Link",
    "Smart City Bypass"
]

STAGES = [
    "Section 4 - Preliminary Notification",
    "Social Impact Assessment (SIA)",
    "Section 11 Notification",
    "Section 19 Declaration (R&R Scheme)",
    "Award of Compensation (Section 23/30)",
    "Possession & Physical Transfer"
]

RR_STATUSES = ["Pending", "In Progress", "Completed"]

def generate_synthetic_data(num_records=180):
    records = []
    base_date = datetime(2023, 1, 1)

    for i in range(1, num_records + 1):
        loc = random.choice(LOCATIONS)
        proj_type = random.choice(PROJECT_TYPES)
        proj_id = f"PRJ-{loc['state'][:2].upper()}-{1000 + i}"
        proj_name = f"{loc['district']} {proj_type}"
        stage = random.choice(STAGES)
        
        # Start date between Jan 2023 and Dec 2024
        start_offset = random.randint(0, 600)
        start_date = base_date + timedelta(days=start_offset)
        
        # Planned duration between 180 and 720 days
        planned_duration = random.randint(180, 720)
        target_date = start_date + timedelta(days=planned_duration)
        
        # Budget in Crores INR
        budget_crores = round(random.uniform(150.0, 3500.0), 2)
        
        # Affected families
        affected_families = random.randint(25, 3200)
        
        # Legal case likelihood higher for projects with large affected families
        legal_case_prob = 0.65 if affected_families > 1200 else (0.45 if stage in ["Section 19 Declaration (R&R Scheme)", "Award of Compensation (Section 23/30)"] else 0.20)
        legal_case = 1 if random.random() < legal_case_prob else 0
        
        # Compensation percentage disbursed
        if stage == "Section 4 - Preliminary Notification":
            compensation_pct = round(random.uniform(0.0, 15.0), 1)
            rr_status = "Pending"
        elif stage == "Social Impact Assessment (SIA)":
            compensation_pct = round(random.uniform(5.0, 25.0), 1)
            rr_status = random.choice(["Pending", "In Progress"])
        elif stage == "Section 11 Notification":
            compensation_pct = round(random.uniform(15.0, 45.0), 1)
            rr_status = random.choice(["Pending", "In Progress"])
        elif stage == "Section 19 Declaration (R&R Scheme)":
            compensation_pct = round(random.uniform(30.0, 75.0), 1)
            rr_status = random.choice(["In Progress", "Completed"] if legal_case == 0 else ["Pending", "In Progress"])
        elif stage == "Award of Compensation (Section 23/30)":
            compensation_pct = round(random.uniform(50.0, 95.0), 1)
            rr_status = random.choice(["In Progress", "Completed"])
        else: # Possession & Physical Transfer
            compensation_pct = round(random.uniform(75.0, 100.0), 1)
            rr_status = "Completed" if random.random() > 0.15 else "In Progress"

        # Coordinates with slight jitter (+/- 0.08 deg)
        lat = loc["lat"] + random.uniform(-0.08, 0.08)
        lon = loc["lon"] + random.uniform(-0.08, 0.08)

        # Ground truth delay calculation factors:
        # Delay drivers: Legal case (+90 to 240 days), low compensation given the stage, R&R pending, high affected families
        delay_calc = 0
        if legal_case == 1:
            delay_calc += random.randint(80, 260)
        if compensation_pct < 40.0 and stage in ["Section 19 Declaration (R&R Scheme)", "Award of Compensation (Section 23/30)"]:
            delay_calc += random.randint(60, 180)
        if rr_status == "Pending" and stage not in ["Section 4 - Preliminary Notification"]:
            delay_calc += random.randint(45, 140)
        if affected_families > 1500:
            delay_calc += random.randint(30, 120)
        
        # Noise factor
        delay_calc += random.randint(-40, 50)
        actual_delay_days = max(0, delay_calc)
        
        # delay_flag: 1 if delayed > 30 days
        delay_flag = 1 if actual_delay_days > 30 else 0
        
        # Actual or projected completion date
        actual_or_projected_completion_date = target_date + timedelta(days=actual_delay_days)

        records.append({
            "project_id": proj_id,
            "project_name": proj_name,
            "state": loc["state"],
            "district": loc["district"],
            "stage": stage,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "target_completion_date": target_date.strftime("%Y-%m-%d"),
            "actual_or_projected_date": actual_or_projected_completion_date.strftime("%Y-%m-%d"),
            "planned_duration_days": planned_duration,
            "compensation_pct": compensation_pct,
            "legal_case": legal_case,
            "rr_status": rr_status,
            "affected_families": affected_families,
            "budget_crores": budget_crores,
            "latitude": round(lat, 5),
            "longitude": round(lon, 5),
            "delay_days": actual_delay_days,
            "delay_flag": delay_flag
        })

    df = pd.DataFrame(records)
    return df

def main():
    raw_dir = os.path.join("backend", "data", "raw")
    processed_dir = os.path.join("backend", "data", "processed")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)

    print("Generating synthetic infrastructure land acquisition dataset...")
    df = generate_synthetic_data(200)

    # Save raw CSV
    raw_file = os.path.join(raw_dir, "projects.csv")
    df.to_csv(raw_file, index=False)
    print(f"Raw dataset saved to: {raw_file} ({len(df)} rows)")

    # Data cleaning & handling
    clean_df = df.copy()
    clean_df["compensation_pct"] = clean_df["compensation_pct"].clip(0.0, 100.0)
    clean_df["legal_case"] = clean_df["legal_case"].fillna(0).astype(int)
    clean_df["affected_families"] = clean_df["affected_families"].fillna(clean_df["affected_families"].median()).astype(int)
    clean_df["delay_days"] = clean_df["delay_days"].fillna(0).astype(int)
    clean_df["delay_flag"] = clean_df["delay_flag"].fillna(0).astype(int)

    # Save processed CSV
    processed_file = os.path.join(processed_dir, "clean_data.csv")
    clean_df.to_csv(processed_file, index=False)
    print(f"Processed dataset saved to: {processed_file}")

if __name__ == "__main__":
    main()

