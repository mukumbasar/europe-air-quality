# db/queries.py

import pandas as pd
from sqlalchemy import Engine, text


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