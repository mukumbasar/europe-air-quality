# tests/conftest.py

import pandas as pd
import pytest
from sqlalchemy import create_engine, Engine

from config import (
    RAW_DATA_COLUMN_ORDER,
    TEST_EXTRACT_PARAMS,
    TEST_FORECAST_DAYS,
    TEST_MOCK_POLLUTANT_VALUES,
)
from etl import fetch_open_meteo_air_quality, transform_air_quality_data
from forecasting import forecast_air_quality


@pytest.fixture(scope="session")
def extracted_air_quality_df() -> pd.DataFrame:
    """Fetch raw air quality data from Open-Meteo API for extract integration testing.

    Returns:
        pd.DataFrame: DataFrame produced by live call to fetch_open_meteo_air_quality.
    """
    return fetch_open_meteo_air_quality(
        cities=TEST_EXTRACT_PARAMS["cities"],
        countries=TEST_EXTRACT_PARAMS["countries"],
        lats=TEST_EXTRACT_PARAMS["lats"],
        lons=TEST_EXTRACT_PARAMS["lons"],
        years=1,
    )


@pytest.fixture(scope="session")
def raw_air_quality_df() -> pd.DataFrame:
    """Generate mock raw air quality data using test constants.

    Returns:
        pd.DataFrame: Synthetic raw hourly air quality DataFrame.
    """
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
def processed_air_quality_df(raw_air_quality_df: pd.DataFrame) -> pd.DataFrame:
    """Transform mock raw data into daily averages for testing.

    Args:
        raw_air_quality_df (pd.DataFrame): Input raw air quality data fixture.

    Returns:
        pd.DataFrame: Transformed daily average DataFrame.
    """
    return transform_air_quality_data(raw_air_quality_df)


@pytest.fixture(scope="session")
def forecasted_air_quality(processed_air_quality_df: pd.DataFrame) -> pd.DataFrame:
    """Generate short forecast from mock processed data for testing.

    Args:
        processed_air_quality_df (pd.DataFrame): Processed daily data fixture.

    Returns:
        pd.DataFrame: Forecasted air quality predictions DataFrame.
    """
    return forecast_air_quality(
        processed_air_quality_df, forecast_days=TEST_FORECAST_DAYS
    )


@pytest.fixture
def db_engine() -> Engine:
    """Create an in-memory SQLite database engine for testing load operations.

    Returns:
        Engine: SQLAlchemy Engine connected to an in-memory SQLite instance.
    """
    engine = create_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()
