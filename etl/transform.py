# etl/transform.py
import pandas as pd

DEFAULT_POLLUTANTS = [
    "pm2_5",
    "pm10",
    "ozone",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "carbon_monoxide"
]

def transform_raw_air_quality_data(raw_air_quality_df: pd.DataFrame, pollutants: list[str] = None) -> pd.DataFrame:
    """Transforms the hourly raw air quality data into a monthly aggregated format for the specified pollutants."""

    if pollutants is None:
        pollutants = DEFAULT_POLLUTANTS

    # Copy raw_air_quality_df into df to prevent possible side effects
    df = raw_air_quality_df.copy()

    