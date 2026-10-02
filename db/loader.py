# db/loader.py

import logging
import pandas as pd
from sqlalchemy import Engine

logger = logging.getLogger(__name__)


def save_raw_data(
    df: pd.DataFrame, engine: Engine, table_name: str = "raw_air_quality"
) -> None:
    """Save raw hourly air quality data to the database.

    Args:
        df (pd.DataFrame): DataFrame containing raw hourly air quality records.
        engine (Engine): SQLAlchemy database engine connection.
        table_name (str, optional): Target database table name. Defaults to "raw_air_quality".
    """
    df.to_sql(table_name, con=engine, if_exists="append", index=False)
    logger.info(f"Successfully saved {len(df)} rows to '{table_name}'.")


def save_processed_data(
    df: pd.DataFrame, engine: Engine, table_name: str = "processed_air_quality"
) -> None:
    """Save processed daily average air quality data to the database.

    Args:
        df (pd.DataFrame): DataFrame containing processed daily air quality records.
        engine (Engine): SQLAlchemy database engine connection.
        table_name (str, optional): Target database table name. Defaults to "processed_air_quality".
    """
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)
    logger.info(f"Successfully saved {len(df)} rows to '{table_name}'.")


def save_forecast_data(
    df: pd.DataFrame, engine: Engine, table_name: str = "forecasted_air_quality"
) -> None:
    """Save forecasted air quality predictions to the database.

    Args:
        df (pd.DataFrame): DataFrame containing forecasted air quality predictions.
        engine (Engine): SQLAlchemy database engine connection.
        table_name (str, optional): Target database table name. Defaults to "forecasted_air_quality".
    """
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)
    logger.info(f"Successfully saved {len(df)} rows to '{table_name}'.")