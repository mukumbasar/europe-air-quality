import pytest
from etl.extract import fetch_open_meteo_air_quality

@pytest.fixture(scope="module", name="air_quality_df")
def run_fetch_open_meteo_air_quality():
    """Fetches data once and reuses it across all phase tests."""
    return fetch_open_meteo_air_quality(
        city="Berlin", 
        country="Germany", 
        lat=52.5200, 
        lon=13.4050, 
        years=1
    )

def test_phase_1_not_empty(air_quality_df):
    assert not air_quality_df.empty, "DataFrame is empty."

def test_phase_2_expected_columns(air_quality_df):
    expected_columns = [
        "city", "country", "latitude", "longitude", "timestamp",
        "pm2_5", "pm10", "ozone", "nitrogen_dioxide", "sulphur_dioxide", "carbon_monoxide"
    ]
    for col in expected_columns:
        assert col in air_quality_df.columns, f"Missing column detected: {col}"

def test_phase_3_head_length(air_quality_df):
    assert len(air_quality_df.head()) == 5, "DataFrame head is empty!"

def test_phase_4_no_null_values(air_quality_df):
    assert not air_quality_df.head().isnull().values.any(), "DataFrame head contains null values!"

def test_phase_5_city_country_values(air_quality_df):
    assert (air_quality_df.head()["city"] == "Berlin").all(), "City value mismatch in DataFrame head!"
    assert (air_quality_df.head()["country"] == "Germany").all(), "Country value mismatch in DataFrame head!"