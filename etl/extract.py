# etl/extract.py

from datetime import datetime, timedelta
import os
import pandas as pd
import requests


def fetch_open_meteo_air_quality(city: str, country: str, lat: float, lon: float, years: int = 10) -> pd.DataFrame:
    """Fetches raw air quality data from the Open Meteo API for a given city and country for a specified number of years going back."""

    end_date_obj = datetime.now().date()
    start_date_obj = end_date_obj - timedelta(days=365 * years)

    end_date = end_date_obj.strftime("%Y-%m-%d")
    start_date = start_date_obj.strftime("%Y-%m-%d")

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "pm2_5,pm10,ozone,nitrogen_dioxide,sulphur_dioxide,carbon_monoxide",
        "timezone": "UTC",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(data["hourly"])

    df.rename(columns={"time": "timestamp"}, inplace=True)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["city"] = city
    df["country"] = country
    df["latitude"] = lat
    df["longitude"] = lon

    column_order = [
        "city",
        "country",
        "latitude",
        "longitude",
        "timestamp",
        "pm2_5",
        "pm10",
        "ozone",
        "nitrogen_dioxide",
        "sulphur_dioxide",
        "carbon_monoxide",
    ]

    # Save the DataFrame as a Parquet file in the "data" directory
    os.makedirs("data", exist_ok=True)
    file_path = f"data/raw_{city.lower()}_air_quality.parquet"
    df.to_parquet(file_path, index=False)
    
    return df[column_order]