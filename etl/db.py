# etl/db.py

import pandas as pd
from sqlalchemy import Engine

def get_active_pollutants(engine: Engine) -> list[str]:
    """Fetches the list of active pollutants from the database."""

    query = "SELECT pollutant_name FROM pollutant_details WHERE is_active = TRUE;"
    df = pd.read_sql(query, engine)
    
    return df['pollutant_name'].tolist()