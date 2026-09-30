# tests/conftest.py

import pytest
from config import TEST_EXTRACT_PARAMS
from etl import fetch_open_meteo_air_quality, transform_air_quality_data
from forecasting import forecast_air_quality


@pytest.fixture(scope="session")
def raw_air_quality_df():
    """Fetch raw air quality data once for the entire test session."""
    return fetch_open_meteo_air_quality(
        cities=TEST_EXTRACT_PARAMS["cities"],
        countries=TEST_EXTRACT_PARAMS["countries"],
        lats=TEST_EXTRACT_PARAMS["lats"],
        lons=TEST_EXTRACT_PARAMS["lons"],
        years=5,
    )


@pytest.fixture(scope="session")
def processed_air_quality_df(raw_air_quality_df):
    """Transform raw data into monthly averages for testing."""
    return transform_air_quality_data(raw_air_quality_df)


@pytest.fixture(scope="session")
def forecasted_air_quality(processed_air_quality_df):
    """Generate 12-month forecasts from processed data for testing."""
    return forecast_air_quality(processed_air_quality_df, 12)