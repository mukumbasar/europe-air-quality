# etl/extract.py

from datetime import datetime, timedelta
import os
import pandas as pd
import requests

DEFAULT_POLLUTANTS = [
    "pm2_5",
    "pm10",
    "ozone",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "carbon_monoxide",
]

def fetch_open_meteo_air_quality(
    cities: list[str], 
    countries: list[str], 
    lats: list[float], 
    lons: list[float], 
    pollutants: list[str] = None,
    years: int = 10
) -> pd.DataFrame:
    """Fetch raw hourly air quality data from the Open Meteo API for multiple locations.

    Args:
        cities (list[str]): Names of the target cities.
        countries (list[str]): Names of the target countries corresponding to each city.
        lats (list[float]): Latitude coordinates of the locations.
        lons (list[float]): Longitude coordinates of the locations.
        pollutants (list[str], optional): List of pollutant variables to fetch. Defaults to None.
        years (int, optional): Number of historical years to fetch. Defaults to 10.

    Returns:
        pd.DataFrame: A DataFrame containing hourly air quality observations
        structured with the following schema:
            - city (str): City name
            - country (str): Country name
            - latitude (float): Latitude coordinate
            - longitude (float): Longitude coordinate
            - timestamp (datetime64[ns]): Hourly observation timestamp (UTC)
            - pm2_5 (float): Fine particulate matter concentration
            - pm10 (float): Coarse particulate matter concentration
            - ozone (float): Ground-level Ozone concentration
            - nitrogen_dioxide (float): NO2 concentration
            - sulphur_dioxide (float): SO2 concentration
            - carbon_monoxide (float): CO concentration
    """
    
    # Use default pollutants list if none is provided
    if pollutants is None:
        pollutants = DEFAULT_POLLUTANTS

    # Calculate the start and end dates in the format required by the API (YYYY-MM-DD)
    end_date_obj = datetime.now().date()
    start_date_obj = end_date_obj - timedelta(days=365 * years)
    end_date = end_date_obj.strftime("%Y-%m-%d")
    start_date = start_date_obj.strftime("%Y-%m-%d")

    # Define the API endpoint and parameters (joins coordinate and pollutant lists into comma-separated text)
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": ",".join(str(lat) for lat in lats),
        "longitude": ",".join(str(lon) for lon in lons),
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ",".join(pollutants),
        "timezone": "UTC",
    }

    # Make the API request and handle potential errors
    response = requests.get(url, params=params)
    response.raise_for_status()
    raw_data = response.json()

    # Ensure response is a list so the loop works whether 1 or multiple cities are passed
    raw_data_list = raw_data if isinstance(raw_data, list) else [raw_data]

    # Initialize an empty list to later hold DataFrames for each city
    all_dfs = []

    # Iterate on a city basis to create a DataFrame for each city and append it to the list of all DataFrames
    for i in range(len(cities)):
        # Convert the hourly data for this city to a pandas DataFrame
        df = pd.DataFrame(raw_data_list[i]["hourly"])

        # Add additional columns for city, country, latitude, and longitude
        df["city"] = cities[i]
        df["country"] = countries[i]
        df["latitude"] = lats[i]
        df["longitude"] = lons[i]

        # Rename the "time" column to "timestamp" and change the data type to datetime
        df.rename(columns={"time": "timestamp"}, inplace=True)
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        # Append the DataFrame for this city to the list of all DataFrames
        all_dfs.append(df)

    # Combine all city DataFrames together into one master DataFrame
    final_df = pd.concat(all_dfs, ignore_index=True)

    # Define the desired column order for the final DataFrame 
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

    final_df = final_df[column_order]

    # Save the dataframe as a parquet file in the "data" directory
    os.makedirs("data", exist_ok=True)
    file_path = "data/raw_multi_city_air_quality.parquet"
    final_df.to_parquet(file_path, index=False)

    # Return the dataframe with the specified column order
    return final_df