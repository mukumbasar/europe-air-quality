# tests/test_extract.py

from config import RAW_DATA_COLUMN_ORDER, TEST_EXTRACT_PARAMS


def test_extract_not_empty(extracted_air_quality_df):
    """Test if the dataframe returned by live extract is not empty."""
    assert not extracted_air_quality_df.empty, "DataFrame is empty."


def test_extract_has_expected_columns(extracted_air_quality_df):
    """Test if the extracted dataframe has the expected columns."""
    for col in RAW_DATA_COLUMN_ORDER:
        assert (
            col in extracted_air_quality_df.columns
        ), f"Missing column detected: {col}"


def test_extract_has_five_head_rows(extracted_air_quality_df):
    """Test if the length of the dataframe head is 5."""
    assert (
        len(extracted_air_quality_df.head()) == 5
    ), "DataFrame head is empty!"


def test_extract_has_no_null_values(extracted_air_quality_df):
    """Test if the dataframe head does not contain any null values."""
    assert (
        not extracted_air_quality_df.head().isnull().values.any()
    ), "DataFrame head contains null values!"


def test_extract_preserves_city_country_values(extracted_air_quality_df):
    """Test if city and country values match the input."""
    for city in TEST_EXTRACT_PARAMS["cities"]:
        assert (
            city in extracted_air_quality_df["city"].values
        ), f"City missing: {city}"

    for country in TEST_EXTRACT_PARAMS["countries"]:
        assert (
            country in extracted_air_quality_df["country"].values
        ), f"Country missing: {country}"