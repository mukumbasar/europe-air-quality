# config.py

RAW_DATA_COLUMN_ORDER = [
    "city",
    "country",
    "latitude",
    "longitude",
    "timestamp",
    "pm2_5",
    "pm10",
    "ozone",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "carbon_monoxide",
]

RAW_FILE_PATH = "data/raw_multi_city_air_quality.parquet"

TEST_EXTRACT_PARAMS = {
    "cities": ["Berlin", "Paris", "London"],
    "countries": ["Germany", "France", "United Kingdom"],
    "lats": [52.5200, 48.8566, 51.5074],
    "lons": [13.4050, 2.3522, -0.1278],
}

PROCESSED_DATA_COLUMN_ORDER = [
    "city",
    "country",
    "date",
    "pm2_5",
    "pm10",
    "ozone",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "carbon_monoxide",
    "hours_available",
    "processed_at",
]

PROCESSED_FILE_PATH = "data/processed_multi_city_air_quality.parquet"

DEFAULT_POLLUTANTS = [
    "pm2_5",
    "pm10",
    "ozone",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "carbon_monoxide",
]