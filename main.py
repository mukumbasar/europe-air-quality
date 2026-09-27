# main.py

import logging
import pandas as pd

from config import TEST_EXTRACT_PARAMS, RAW_FILE_PATH, PROCESSED_FILE_PATH
from etl import fetch_open_meteo_air_quality, transform_air_quality_data
from forecasting import forecast_air_quality

# Configure logging for pipeline tracking
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def run_pipeline():
    """Run the pipeline."""

    logging.info("Step 0: Starting Air Quality ETL & Forecasting Pipeline...")

    try:
        # ==========================================
        # STEP 1: EXTRACT
        # ==========================================
        # TODO: Fetch cities, countries, lats, and lons from the database.
        
        logging.info("Step 1: Extracting raw air quality data from Open-Meteo...")
        raw_df = fetch_open_meteo_air_quality(
            cities=TEST_EXTRACT_PARAMS["cities"],
            countries=TEST_EXTRACT_PARAMS["countries"],
            lats=TEST_EXTRACT_PARAMS["lats"],
            lons=TEST_EXTRACT_PARAMS["lons"],
            years=10,  # 10 years historical scope
        )
        
        # Save raw_df in /data
        raw_df.to_parquet(RAW_FILE_PATH, index=False)
        logging.info(f"Raw data successfully saved to {RAW_FILE_PATH}")

        # ==========================================
        # STEP 2: TRANSFORM
        # ==========================================
        
        logging.info("Step 2A: Transforming and aggregating data into monthly averages...")
        processed_df = transform_air_quality_data(raw_df)
        
        # Save processed_df in /data
        processed_df.to_parquet(PROCESSED_FILE_PATH, index=False)
        logging.info(f"Processed data successfully saved to {PROCESSED_FILE_PATH}")

        logging.info("Step 2B: Generating 36-month air quality forecasts using Prophet...")
        forecasted_df = forecast_air_quality(processed_df, forecast_months=36)
        logging.info("Forecasting completed successfully.")       

        # ==========================================
        # STEP 3: LOAD
        # ==========================================
        # TODO: Insert raw_df into the database.
        # TODO: Insert processed_df into the database.
        # TODO: Insert forecasted_df into the database. 
        
        # ==========================================
        # STEP 4: PIPELINE COMPLETION
        # ==========================================
        logging.info("Pipeline execution finished successfully!")

    except Exception as e:
        logging.error(f"❌ Pipeline failed due to an error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    run_pipeline()