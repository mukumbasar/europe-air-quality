import pytest
import os
from etl.extract import fetch_open_meteo_air_quality

FILE_PATH = "data/raw_berlin_air_quality.parquet"

@pytest.fixture(scope="module")
def air_quality_df():
    """Fetch air quality data from Open Meteo API before tests run, 
        then clean up the generated file after tests are finalized."""
    df = fetch_open_meteo_air_quality(
        city="Berlin", 
        country="Germany", 
        lat=52.5200, 
        lon=13.4050, 
        years=1
    )

    # Provide the dataframe to the tests and wait for them to finish
    yield df

    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)

def test_phase_1_not_empty(air_quality_df):
    """Test if the dataframe is not empty."""
    assert not air_quality_df.empty, "DataFrame is empty."
    
def test_phase_2_expected_columns(air_quality_df):
    """Test if the dataframe has the expected columns."""
    expected_columns = [
        "city", "country", "latitude", "longitude", "timestamp",
        "pm2_5", "pm10", "ozone", "nitrogen_dioxide", "sulphur_dioxide", "carbon_monoxide"
    ]
    for col in expected_columns:
        assert col in air_quality_df.columns, f"Missing column detected: {col}"

def test_phase_3_head_length(air_quality_df):
    """Test if the length of the dataframe head is 5."""
    assert len(air_quality_df.head()) == 5, "DataFrame head is empty!"

def test_phase_4_no_null_values(air_quality_df):
    """Test if the dataframe head does not contain any null values."""
    assert not air_quality_df.head().isnull().values.any(), "DataFrame head contains null values!"

def test_phase_5_city_country_values(air_quality_df):
    """Test if the country value in the dataframe head is "Germany"."""
    assert (air_quality_df.head()["country"] == "Germany").all(), "Country value mismatch in DataFrame head!"

def test_phase_6_parquet_file_exists(air_quality_df):
    """Test if the parquet file exists after fetching the data."""
    assert os.path.exists(FILE_PATH), f"Parquet file does not exist at {FILE_PATH}."