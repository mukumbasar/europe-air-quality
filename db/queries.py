# db/db.py

import pandas as pd
from sqlalchemy import Engine

def get_active_pollutants(engine: Engine) -> list[str]:
    """Fetches the list of active pollutants from the database."""

    query = "SELECT pollutant_name FROM pollutant_details WHERE is_active = TRUE;"
    df = pd.read_sql(query, engine)
    
    return df['pollutant_name'].tolist()

def get_cities(engine: Engine) -> pd.DataFrame:
    """Fetches all the cities and their coordinates from the database."""

    query = "SELECT city, country, latitude, longtitude FROM cities ORDER BY city ASC;"
    return pd.read_sql(query, engine)
    