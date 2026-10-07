# db/queries.py

import pandas as pd
import streamlit as st 
from sqlalchemy import Engine, text

# ==========================================
# ETL & FORECASTING PIPELINE QUERIES
# ==========================================

# TODO: Consider moving these queries to seperate modular files.


def get_active_pollutants(engine: Engine) -> list[str]:
    """Fetch active pollutant names from the database.

    Args:
        engine (Engine): SQLAlchemy database engine connection.

    Returns:
        list[str]: List of active pollutant names.
    """
    query = "SELECT pollutant_name FROM pollutant_details WHERE is_active = TRUE;"
    df = pd.read_sql(query, engine)
    return df["pollutant_name"].tolist()


def get_cities(engine: Engine) -> pd.DataFrame:
    """Fetch cities and their spatial coordinates from the database.

    Args:
        engine (Engine): SQLAlchemy database engine connection.

    Returns:
        pd.DataFrame: DataFrame containing city names, countries, and coordinates.
    """
    query = "SELECT city, country, latitude, longitude FROM cities ORDER BY city ASC;"
    return pd.read_sql(query, engine)


def get_processed_air_quality(
    engine: Engine, city: str = None
) -> pd.DataFrame:
    """Fetch processed daily air quality data from the database.

    Args:
        engine (Engine): SQLAlchemy database engine connection.
        city (str, optional): City name to filter by. Defaults to None.

    Returns:
        pd.DataFrame: DataFrame containing processed daily air quality records.
    """
    if city:
        query = text("SELECT * FROM processed_air_quality WHERE city = :city ORDER BY date ASC;")
        return pd.read_sql(query, engine, params={"city": city})

    query = "SELECT * FROM processed_air_quality ORDER BY date ASC;"
    return pd.read_sql(query, engine)


def get_forecasted_air_quality(
    engine: Engine, city: str = None
) -> pd.DataFrame:
    """Fetch forecasted air quality predictions from the database.

    Args:
        engine (Engine): SQLAlchemy database engine connection.
        city (str, optional): City name to filter by. Defaults to None.

    Returns:
        pd.DataFrame: DataFrame containing air quality forecast records.
    """
    if city:
        query = text("SELECT * FROM forecasted_air_quality WHERE city = :city ORDER BY date ASC;")
        return pd.read_sql(query, engine, params={"city": city})

    query = "SELECT * FROM forecasted_air_quality ORDER BY date ASC;"
    return pd.read_sql(query, engine)


# ==========================================
# UI QUERIES
# ==========================================


def get_pollutant_thresholds(engine: Engine) -> pd.DataFrame:
    """Fetch pollutant limit thresholds for map color coding.

    Args:
        engine (Engine): SQLAlchemy database engine connection.

    Returns:
        pd.DataFrame: DataFrame with pollutant names, middle limits, and high limits.
    """
    query = "SELECT pollutant_name, middle_limit, high_limit FROM pollutant_details WHERE is_active = TRUE;"
    return pd.read_sql(query, engine)


def get_latest_map_data(engine: Engine, pollutant: str) -> pd.DataFrame:
    """Fetch the latest recorded reading for every city for a specific pollutant column.

    Args:
        engine (Engine): SQLAlchemy database engine connection.
        pollutant (str): The pollutant column name to select (e.g., 'pm2_5').

    Returns:
        pd.DataFrame: City coordinates, country, date and latest processed pollutant reading according to the variable pollutant input.
    """
    query = text(f"""
        SELECT DISTINCT ON (c.city)
            c.city,
            c.country,
            c.latitude,
            c.longitude,
            p.date,
            p.{pollutant} AS value
        FROM processed_air_quality p
        JOIN cities c ON p.city = c.city
        WHERE p.{pollutant} IS NOT NULL
        ORDER BY c.city, p.date DESC;
    """)
    return pd.read_sql(query, engine)


def get_forecast_air_quality(engine: Engine, city: str, pollutant: str) -> pd.DataFrame:
    """Fetch forecast air quality data for a specific city.

    Args:
        engine (Engine): SQLAlchemy database engine connection.
        city (str): The city name to filter by.
        pollutant (str): The pollutant column name to select.

    Returns:
        pd.DataFrame: City, country, date, and forecast pollutant readings for the specified city.
    """
    query = text(f"""
        SELECT city,
            country,
            date,
            {pollutant} as value
        FROM forecast_air_quality
        WHERE city = :city
        ORDER BY date ASC;
    """)
    return pd.read_sql(query, engine, params={"city": city})


def get_processed_air_quality(engine: Engine, city: str, pollutant: str) -> pd.DataFrame:
    """Fetch processed air quality data for a specific city.

    Args:
        engine (Engine): SQLAlchemy database engine connection.
        city (str): The city name to filter by.
        pollutant (str): The pollutant column name to select.

    Returns:
        pd.DataFrame: City, country, date, and processed pollutant readings for the specified city.
    """
    query = text(f"""
        SELECT city,
            country,
            date,
            {pollutant} as value
        FROM processed_air_quality
        WHERE city = :city
        ORDER BY date ASC;
    """)
    return pd.read_sql(query, engine, params={"city": city})