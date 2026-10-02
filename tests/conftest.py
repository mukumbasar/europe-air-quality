# tests/conftest.py

import pandas as pd
import pytest

from config import (
    RAW_DATA_COLUMN_ORDER,
    TEST_EXTRACT_PARAMS,
    TEST_FORECAST_DAYS,
    TEST_MOCK_POLLUTANT_VALUES,
)
from etl import transform_air_quality_data
from forecasting import forecast_air_quality


@pytest.fixture(scope="session")
def raw_air_quality_df():
    """Generate mock raw air quality data using test constants."""
    records = []
    timestamps = pd.date_range(start="2020-01-01", periods=24 * 30, freq="h")

    cities = TEST_EXTRACT_PARAMS["cities"]
    countries = TEST_EXTRACT_PARAMS["countries"]
    lats = TEST_EXTRACT_PARAMS["lats"]
    lons = TEST_EXTRACT_PARAMS["lons"]

    for i in range(len(cities)):
        city = cities[i]
        country = countries[i]
        lat = lats[i]
        lon = lons[i]

        for ts in timestamps:
            row = {
                "timestamp": ts,
                "city": city,
                "country": country,
                "latitude": lat,
                "longitude": lon,
            }
            row.update(TEST_MOCK_POLLUTANT_VALUES)
            records.append(row)

    df = pd.DataFrame(records)
    return df[RAW_DATA_COLUMN_ORDER]


@pytest.fixture(scope="session")
def processed_air_quality_df(raw_air_quality_df):
    """Transform mock raw data into daily averages for testing."""
    return transform_air_quality_data(raw_air_quality_df)


@pytest.fixture(scope="session")
def forecasted_air_quality(processed_air_quality_df):
    """Generate short forecast from mock processed data for testing."""
    return forecast_air_quality(processed_air_quality_df, forecast_days=TEST_FORECAST_DAYS)