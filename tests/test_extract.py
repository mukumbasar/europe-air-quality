# tests/test_extract.py

import os
import pytest
from etl.extract import fetch_open_meteo_air_quality

FILE_PATH = "data/raw_multi_city_air_quality.parquet"


@pytest.fixture(scope="module")
def air_quality_df():
    """Fetch air quality data from Open Meteo API before tests run, then clean up the generated file after tests are finalized."""

    # Fetch the temporary air quality data and provide it to the tests
    df = fetch_open_meteo_air_quality(
        cities=["Berlin", "Paris", "London"],
        countries=["Germany", "France", "United Kingdom"],
        lats=[52.5200, 48.8566, 51.5074],
        lons=[13.4050, 2.3522, -0.1278],
        years=1,
    )

    # Provide the dataframe to the tests and wait for them to finish
    yield df

    # Clean up the generated parquet file after tests are finalized
    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)


def test_phase_1_not_empty(air_quality_df):
    """Test if the dataframe is not empty."""
    assert not air_quality_df.empty, "DataFrame is empty."


def test_phase_2_expected_columns(air_quality_df):
    """Test if the dataframe has the expected columns."""
    expected_columns = [
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
    for col in expected_columns:
        assert col in air_quality_df.columns, f"Missing column detected: {col}"


def test_phase_3_head_length(air_quality_df):
    """Test if the length of the dataframe head is 5."""
    assert len(air_quality_df.head()) == 5, "DataFrame head is empty!"


def test_phase_4_no_null_values(air_quality_df):
    """Test if the dataframe head does not contain any null values."""
    assert (
        not air_quality_df.head().isnull().values.any()
    ), "DataFrame head contains null values!"


def test_phase_5_city_country_values(air_quality_df):
    """Test if the city and country values in the dataframe match the input."""
    expected_cities = ["Berlin", "Paris", "London"]
    expected_countries = ["Germany", "France", "United Kingdom"]

    for city in expected_cities:
        assert city in air_quality_df["city"].values, f"City missing: {city}"

    for country in expected_countries:
        assert country in air_quality_df["country"].values, f"Country missing: {country}"


def test_phase_6_parquet_file_exists(air_quality_df):
    """Test if the parquet file exists after fetching the data."""
    assert os.path.exists(
        FILE_PATH
    ), f"Parquet file does not exist at {FILE_PATH}."