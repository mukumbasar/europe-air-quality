A mono-repo city-based air quality monitoring and forecasting dashboard based on Open-Meteo data, which utilizes Streamlit for visualization.

# Pipeline:
- Extracts 4-year hourly historical air quality data from Open-Meteo API for each city in the scope, going back from the point of execution.
- Saves raw air quality data in parquet format locally. 
- Transforms hourly data to daily data in accordance with the project objective, risk assessment paradigm of WHO and to reduce potential forecasting noise.
- Forecasts 14-day air quality data on a daily basis for each city in the scope using Prophet by Meta.
- Loads both processed air quality and forecast air quality data into PostgreSQL database executed in Docker on a daily basis for each city in the scope.
- Visualizes the output on a one page Streamlit web application.

> **Disclaimer:** This project is a portfolio piece and provided as is. Data is sourced from Open-Meteo and forecasts are not guaranteed.

#

# Prerequisites

- Git
- Python 3.10+
- Docker & Docker Compose

# Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/mukumbasar/europe-air-quality.git](https://github.com/mukumbasar/europe-air-quality.git)
   cd europe-air-quality
   ```

2. **Set up virtual environment & install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Create environment file from template:**
   ```bash
   cp .env.example .env # Windows: copy .env.example .env
   ```

4. **Start the database:**
   ```bash
   docker compose up -d
   ```

# Running Tests

The project uses `pytest` for testing the ETL pipeline and forecasting modules.

Run tests with verbose output and live print/log statements enabled:
```bash
pytest -v -s
```

Run specific pipeline tests individually:
```bash
# Run extract pipeline tests
pytest tests/test_extract.py

# Run transform pipeline tests
pytest tests/test_transform.py

# Run forecast pipeline tests
pytest tests/test_forecast.py
```

Or run tests by keyword matching:
```bash
pytest -k extract
```

# Running the Pipeline

Execute the ETL and forecasting pipeline script:
```bash
python main.py
```

# Database Inspection (Docker)

To connect to PostgreSQL running in Docker and check your tables:

1. **Access PostgreSQL database through Docker container:**
   ```bash
   docker exec -it postgres_db psql -U postgres -d europe_air_quality_db
   ```

2. **Check tables:**
   ```sql
   \dt
   ```

3. **Select first 20 rows from forecasted:**
   ```sql
   SELECT * FROM forecast_air_quality ORDER BY city, date LIMIT 20;
   ```

4. **Exit database prompt:**
   ```sql
   \q
   ```

# Running the Dashboard

Launch the Streamlit web application:
```bash
streamlit run app.py
```


# Teardown & Cleanup

To stop containers, flush data, or exit your Python environment:

1. **Stop containers:**
   ```bash
   docker compose down
   ```

2. **Flush all database data & remove volumes:**
   ```bash
   docker compose down -v
   ```

3. **Deactivate Python virtual environment:**
   ```bash
   deactivate
   ```


# Frequently Asked Questions (FAQ)

### Why Meta Prophet?
Prophet handles seasonality, missing data, and outliers natively out of the box; avoiding manual parameter tuning, complex feature engineering or heavy compute overhead.

**Alternatives considered:** ARIMA/SARIMA, XGBoost/LightGBM, LSTM.