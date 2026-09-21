
import pytest


from etl import fetch_open_meteo_air_quality, transform_air_quality_data
from forecasting import forecast_air_quality

from config import TEST_EXTRACT_PARAMS, FORECAST_DATA_COLUMN_ORDER

@pytest.fixture(scope="module")
def forecasted_air_quality():
    """Fixture to provide a sample processed air quality DataFrame for testing."""

    raw_df = fetch_open_meteo_air_quality(
        cities=TEST_EXTRACT_PARAMS["cities"],
        countries=TEST_EXTRACT_PARAMS["countries"],
        lats=TEST_EXTRACT_PARAMS["lats"],
        lons=TEST_EXTRACT_PARAMS["lons"],
        years=5,
    )

    processed_df = transform_air_quality_data(raw_df)

    forecasted_df = forecast_air_quality(processed_df, 12) 

    return forecasted_df


def test_forecast_not_empty(forecasted_air_quality):
    """Test if the dataframe is. not empty."""
    assert not forecasted_air_quality.empty, "DataFrame is empty."


def test_forecast_has_expected_columns(forecasted_air_quality):
    """Test if the DataFrame has the expected columns."""
    for col in FORECAST_DATA_COLUMN_ORDER:
        assert col in forecasted_air_quality.columns, f"Missing column detected: {col}"

def test_forecast_has_five_head_rows(forecasted_air_quality):
    """Test if the head of DataFrame has the length of 5."""
    assert len(forecasted_air_quality.head()) == 5, "DataFrame head length is not 5."

def test_forecast_has_no_null_values(forecasted_air_quality):
    """Test if the DataFrame head has no null values."""
    assert not forecasted_air_quality.head().isnull().values.any(), "DataFrame head has null values."

def test_forecast_preserves_city_country_values(forecasted_air_quality):
    """Test if city and country values match the input."""
    for city in TEST_EXTRACT_PARAMS["cities"]:
        assert city in forecasted_air_quality["city"].values, f"City missing: {city}"

    for country in TEST_EXTRACT_PARAMS["countries"]:
        assert country in forecasted_air_quality["country"].values, f"Country missing: {country}"