# dashboard/helpers.py

import pandas as pd
from config import COLOR_MAP

def get_status_color(status: str) -> str:
    """
    Get color code with status string. ("Low Risk", "Moderate Risk", "High Risk")
    """
    return COLOR_MAP.get(status, "#FFFFFF")

def format_pollutant_name(name: str) -> str:
    """
    Convert raw pollutant names from the db into clean display names
    """
    mapping = {
        "pm2_5": "PM2.5",
        "pm10": "PM10",
        "ozone": "Ozone",
        "nitrogen_dioxide": "Nitrogen Dioxide",
        "sulphur_dioxide": "Sulphur Dioxide",
        "carbon_monoxide": "Carbon Monoxide",
    }
    key = name.lower().strip()
    if key in mapping:
        return mapping[key]
    return name.replace("_", " ").title()

def categorize_air_quality(val: float, middle_limit: float, high_limit: float) -> str:
    """
    Determine the risk level based on the pollutant value and given thresholds.
    """
    if val < middle_limit:
        return "Low Risk"
    elif val < high_limit:
        return "Moderate Risk"
    else:
        return "High Risk"

def get_pollutant_limits(thresholds_df: pd.DataFrame, pollutant_name: str) -> tuple[float, float]:
    """
    Extract the middle and high risk threshold limits for a specific pollutant.
    """
    if thresholds_df.empty:
        return 0.0, 0.0
    row = thresholds_df[thresholds_df["pollutant_name"] == pollutant_name]
    if row.empty:
        return 0.0, 0.0
    return float(row.iloc[0]["middle_limit"]), float(row.iloc[0]["high_limit"])