from datetime import datetime

import pandas as pd

from config import PROCESSED_DATA_COLUMN_ORDER


def transform_air_quality_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transform hourly air quality data into monthly averages.

    Args:
        df (pd.DataFrame): DataFrame containing hourly air quality data.

    Returns:
        pd.DataFrame: DataFrame containing monthly air quality averages,
        available hourly records, and processing time.
    """

    df["date"] = df["timestamp"].dt.to_period("M").dt.start_time

    grouped = df.groupby(["city", "country", "date"])

    processed_df = grouped.agg({
        "pm2_5": "mean",
        "pm10": "mean",
        "ozone": "mean",
        "nitrogen_dioxide": "mean",
        "sulphur_dioxide": "mean",
        "carbon_monoxide": "mean",
        "timestamp": "count",
    })

    processed_df = processed_df.reset_index()

    processed_df = processed_df.rename(
        columns={"timestamp": "hours_available"}
    )

    processed_df["processed_at"] = datetime.now()

    processed_df = processed_df[PROCESSED_DATA_COLUMN_ORDER]

    return processed_df