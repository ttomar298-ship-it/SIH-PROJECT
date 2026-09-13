import os
import datetime
import pandas as pd

# Flag to distinguish between static benchmark mode and external live API integrations
USE_LIVE_API = os.getenv("USE_LIVE_API", "false").lower() in ("true", "1", "yes")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DATA_PATH = os.path.join(BASE_DIR, "backend", "data", "processed", "clean_data.csv")

def get_dataset_metadata() -> dict:
    """
    Dynamically pulls dataset metadata including last modified timestamp and
    date horizon, avoiding hardcoded date claims.
    """
    last_updated_str = "December 2024"
    record_count = 262
    
    if os.path.exists(DATA_PATH):
        try:
            mtime = os.path.getmtime(DATA_PATH)
            # Format timestamp from actual dataset file
            file_dt = datetime.datetime.fromtimestamp(mtime)
            last_updated_str = file_dt.strftime("%d %b %Y")
            
            # Read sample to verify count and max date
            df = pd.read_csv(DATA_PATH)
            record_count = len(df)
            if "start_date" in df.columns:
                max_start_val = df["start_date"].dropna().max()
                if pd.notna(max_start_val) and str(max_start_val).strip():
                    last_updated_str = f"{last_updated_str} (Historical baseline through {str(max_start_val)[:4]})"
        except Exception:
            pass

    return {
        "use_live_api": USE_LIVE_API,
        "is_static": not USE_LIVE_API,
        "mode_label": "Live API Connected" if USE_LIVE_API else "Curated Benchmark (Static)",
        "badge_color": "#10B981" if USE_LIVE_API else "#64748B",
        "badge_icon": "🟢" if USE_LIVE_API else "📦",
        "last_updated": last_updated_str,
        "record_count": record_count,
        "source_attribution": "MoSPI Infrastructure Monitoring & DILRMP Land Modernization Records"
    }

