# etl/extract.py

from datetime import datetime, timedelta

import pandas as pd
import requests

from config import DEFAULT_POLLUTANTS, RAW_DATA_COLUMN_ORDER


def fetch_open_meteo_air_quality(
    cities: list[str],
    countries: list[str],
    lats: list[float],
    lons: list[float],
    pollutants: list[str] = None,
    years: int = 10,
) -> pd.DataFrame:
    """Fetch raw hourly air quality data from Open Meteo API.

    Args:
        cities (list[str]): List of city names.
        countries (list[str]): List of country names corresponding to cities.
        lats (list[float]): List of latitude coordinates.
        lons (list[float]): List of longitude coordinates.
        pollutants (list[str], optional): List of pollutants to fetch. Defaults to DEFAULT_POLLUTANTS.
        years (int, optional): Number of past years of data to fetch. Defaults to 10.

    Returns:
        pd.DataFrame: DataFrame containing raw hourly air quality data for all cities.
    """
    if pollutants is None:
        pollutants = DEFAULT_POLLUTANTS

    end_date_obj = datetime.now().date()
    start_date_obj = end_date_obj - timedelta(days=365 * years)

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": ",".join(str(lat) for lat in lats),
        "longitude": ",".join(str(lon) for lon in lons),
        "start_date": start_date_obj.strftime("%Y-%m-%d"),
        "end_date": end_date_obj.strftime("%Y-%m-%d"),
        "hourly": ",".join(pollutants),
        "timezone": "UTC",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    raw_data = response.json()

    raw_data_list = raw_data if isinstance(raw_data, list) else [raw_data]
    all_dfs = []

    for i in range(len(cities)):
        df = pd.DataFrame(raw_data_list[i]["hourly"])
        df["city"] = cities[i]
        df["country"] = countries[i]
        df["latitude"] = lats[i]
        df["longitude"] = lons[i]
        df.rename(columns={"time": "timestamp"}, inplace=True)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        all_dfs.append(df)

    final_df = pd.concat(all_dfs, ignore_index=True)

    final_df = final_df[RAW_DATA_COLUMN_ORDER]

    return final_df