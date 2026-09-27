# db/db.py

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine

load_dotenv()


def get_engine() -> Engine:
    """Creates and returns a SQLAlchemy database engine.

    Returns:
        Engine: A SQLAlchemy Engine instance configured with the database URL.
    """
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "postgrespassword")
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        db_name = os.getenv("POSTGRES_DB", "europe_air_quality_db")

        db_url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

    return create_engine(db_url, pool_pre_ping=True)