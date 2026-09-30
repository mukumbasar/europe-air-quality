# tests/test_forecast.py

from config import FORECAST_DATA_COLUMN_ORDER, TEST_EXTRACT_PARAMS


def test_forecast_not_empty(forecasted_air_quality):
    """Test if the dataframe is not empty."""
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
    assert (
        not forecasted_air_quality.head().isnull().values.any()
    ), "DataFrame head has null values."


def test_forecast_preserves_city_country_values(forecasted_air_quality):
    """Test if city and country values match the input."""
    for city in TEST_EXTRACT_PARAMS["cities"]:
        assert city in forecasted_air_quality["city"].values, f"City missing: {city}"

    for country in TEST_EXTRACT_PARAMS["countries"]:
        assert (
            country in forecasted_air_quality["country"].values
        ), f"Country missing: {country}"