# tests/test_transform.py

import os

import pytest

from config import TEST_EXTRACT_PARAMS, PROCESSED_DATA_COLUMN_ORDER
from etl import fetch_open_meteo_air_quality, transform_air_quality_data


@pytest.fixture(scope="module")
def processed_air_quality_df():
    """Fixture to provide a sample processed air quality DataFrame for testing."""

    raw_df = fetch_open_meteo_air_quality(
        cities=TEST_EXTRACT_PARAMS["cities"],
        countries=TEST_EXTRACT_PARAMS["countries"],
        lats=TEST_EXTRACT_PARAMS["lats"],
        lons=TEST_EXTRACT_PARAMS["lons"],
        years=1,
    )

    processed_df = transform_air_quality_data(raw_df)

    return processed_df


def test_transform_not_empty(processed_air_quality_df):
    """Test if the dataframe is not empty."""
    assert not processed_air_quality_df.empty, "DataFrame is empty."


def test_transform_has_expected_columns(processed_air_quality_df):
    """Test if the dataframe has the expected columns."""
    for col in PROCESSED_DATA_COLUMN_ORDER:
        assert col in processed_air_quality_df.columns, f"Missing column detected: {col}"


def test_transform_has_five_head_rows(processed_air_quality_df):
    """Test if the length of the dataframe head is 5."""
    assert len(processed_air_quality_df.head()) == 5, "DataFrame head is empty!"


def test_transform_has_no_null_values(processed_air_quality_df):
    """Test if the dataframe head does not contain any null values."""
    assert (
        not processed_air_quality_df.head().isnull().values.any()
    ), "DataFrame head contains null values!"


def test_transform_preserves_city_country_values(processed_air_quality_df):
    """Test if city and country values match the input."""
    for city in TEST_EXTRACT_PARAMS["cities"]:
        assert city in processed_air_quality_df["city"].values, f"City missing: {city}"

    for country in TEST_EXTRACT_PARAMS["countries"]:
        assert (
            country in processed_air_quality_df["country"].values
        ), f"Country missing: {country}"