# tests/test_load.py

import pandas as pd
from sqlalchemy import inspect

from config import (
    FORECAST_DATA_COLUMN_ORDER,
    PROCESSED_DATA_COLUMN_ORDER,
    RAW_DATA_COLUMN_ORDER,
)
from etl.load import save_forecast_data, save_processed_data, save_raw_data


# ==========================================
# TESTS FOR save_raw_data
# ==========================================


def test_save_raw_data_creates_table_and_not_empty(raw_air_quality_df, db_engine):
    """Test if save_raw_data writes a non-empty table to the database."""
    table_name = "test_raw_air_quality"
    save_raw_data(raw_air_quality_df, db_engine, table_name=table_name)

    inspector = inspect(db_engine)
    assert inspector.has_table(table_name), f"Table '{table_name}' was not created."

    saved_df = pd.read_sql_table(table_name, con=db_engine)
    assert not saved_df.empty, "Saved raw table is empty."


def test_save_raw_data_preserves_row_count(raw_air_quality_df, db_engine):
    """Test if save_raw_data preserves total row count."""
    table_name = "test_raw_row_count"
    save_raw_data(raw_air_quality_df, db_engine, table_name=table_name)

    saved_df = pd.read_sql_table(table_name, con=db_engine)
    assert len(saved_df) == len(raw_air_quality_df), "Saved row count does not match input."


def test_save_raw_data_has_expected_columns(raw_air_quality_df, db_engine):
    """Test if saved raw table contains all expected columns."""
    table_name = "test_raw_columns"
    save_raw_data(raw_air_quality_df, db_engine, table_name=table_name)

    saved_df = pd.read_sql_table(table_name, con=db_engine)
    for col in RAW_DATA_COLUMN_ORDER:
        assert col in saved_df.columns, f"Missing column detected: {col}"


# ==========================================
# TESTS FOR save_processed_data
# ==========================================


def test_save_processed_data_creates_table_and_not_empty(processed_air_quality_df, db_engine):
    """Test if save_processed_data writes a non-empty table to the database."""
    table_name = "test_processed_air_quality"
    save_processed_data(processed_air_quality_df, db_engine, table_name=table_name)

    inspector = inspect(db_engine)
    assert inspector.has_table(table_name), f"Table '{table_name}' was not created."

    saved_df = pd.read_sql_table(table_name, con=db_engine)
    assert not saved_df.empty, "Saved processed table is empty."


def test_save_processed_data_preserves_row_count(processed_air_quality_df, db_engine):
    """Test if save_processed_data preserves total row count."""
    table_name = "test_processed_row_count"
    save_processed_data(processed_air_quality_df, db_engine, table_name=table_name)

    saved_df = pd.read_sql_table(table_name, con=db_engine)
    assert len(saved_df) == len(processed_air_quality_df), "Saved row count does not match input."


def test_save_processed_data_has_expected_columns(processed_air_quality_df, db_engine):
    """Test if saved processed table contains all expected columns."""
    table_name = "test_processed_columns"
    save_processed_data(processed_air_quality_df, db_engine, table_name=table_name)

    saved_df = pd.read_sql_table(table_name, con=db_engine)
    for col in PROCESSED_DATA_COLUMN_ORDER:
        assert col in saved_df.columns, f"Missing column detected: {col}"


# ==========================================
# TESTS FOR save_forecast_data
# ==========================================


def test_save_forecast_data_creates_table_and_not_empty(forecasted_air_quality, db_engine):
    """Test if save_forecast_data writes a non-empty table to the database."""
    table_name = "test_forecast_air_quality"
    save_forecast_data(forecasted_air_quality, db_engine, table_name=table_name)

    inspector = inspect(db_engine)
    assert inspector.has_table(table_name), f"Table '{table_name}' was not created."

    saved_df = pd.read_sql_table(table_name, con=db_engine)
    assert not saved_df.empty, "Saved forecast table is empty."


def test_save_forecast_data_preserves_row_count(forecasted_air_quality, db_engine):
    """Test if save_forecast_data preserves total row count."""
    table_name = "test_forecast_row_count"
    save_forecast_data(forecasted_air_quality, db_engine, table_name=table_name)

    saved_df = pd.read_sql_table(table_name, con=db_engine)
    assert len(saved_df) == len(forecasted_air_quality), "Saved row count does not match input."


def test_save_forecast_data_has_expected_columns(forecasted_air_quality, db_engine):
    """Test if saved forecast table contains all expected columns."""
    table_name = "test_forecast_columns"
    save_forecast_data(forecasted_air_quality, db_engine, table_name=table_name)

    saved_df = pd.read_sql_table(table_name, con=db_engine)
    for col in FORECAST_DATA_COLUMN_ORDER:
        assert col in saved_df.columns, f"Missing column detected: {col}"
