# tests/test_extract.py

import os

import pytest
import pandas as pd

from config import RAW_DATA_COLUMN_ORDER, RAW_FILE_PATH, TEST_EXTRACT_PARAMS
from etl import fetch_open_meteo_air_quality


@pytest.fixture(scope="module")
def raw_air_quality_df():
    """Fixture to provide a sample raw air quality DataFrame for testing."""

    df = fetch_open_meteo_air_quality(
        cities=TEST_EXTRACT_PARAMS["cities"],
        countries=TEST_EXTRACT_PARAMS["countries"],
        lats=TEST_EXTRACT_PARAMS["lats"],
        lons=TEST_EXTRACT_PARAMS["lons"],
        years=1,
    )

    yield df

    if os.path.exists(RAW_FILE_PATH):
        os.remove(RAW_FILE_PATH)


def test_extract_not_empty(raw_air_quality_df):
    """Test if the dataframe is not empty."""
    assert not raw_air_quality_df.empty, "DataFrame is empty."


def test_extract_has_expected_columns(raw_air_quality_df):
    """Test if the dataframe has the expected columns."""

    for col in RAW_DATA_COLUMN_ORDER:
        assert col in raw_air_quality_df.columns, f"Missing column detected: {col}"


def test_extract_has_five_head_rows(raw_air_quality_df):
    """Test if the length of the dataframe head is 5."""
    assert len(raw_air_quality_df.head()) == 5, "DataFrame head is empty!"


def test_extract_has_no_null_values(raw_air_quality_df):
    """Test if the dataframe head does not contain any null values."""
    assert not raw_air_quality_df.head().isnull().values.any(), "DataFrame head contains null values!"


def test_extract_preserves_city_country_values(raw_air_quality_df):
    """Test if city and country values match the input."""

    for city in TEST_EXTRACT_PARAMS["cities"]:
        assert city in raw_air_quality_df["city"].values, f"City missing: {city}"

    for country in TEST_EXTRACT_PARAMS["countries"]:
        assert (
            country in raw_air_quality_df["country"].values
        ), f"Country missing: {country}"