# config.py

# ==========================================
# FILE PATHS
# ==========================================

RAW_FILE_PATH = "data/raw_multi_city_air_quality.parquet"
PROCESSED_FILE_PATH = "data/processed_multi_city_air_quality.parquet"


# ==========================================
# SCHEMA & COLUMN ORDER DEFINITIONS
# ==========================================

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

FORECAST_DATA_COLUMN_ORDER = [
    "city",
    "country",
    "date",
    "pm2_5",
    "pm10",
    "ozone",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "carbon_monoxide",
]


# ==========================================
# MODEL & PIPELINE CONFIGURATIONS
# ==========================================

DEFAULT_POLLUTANTS = [
    "pm2_5",
    "pm10",
    "ozone",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "carbon_monoxide",
]


# ==========================================
# TESTING CONFIGURATION
# ==========================================

TEST_FORECAST_DAYS = 12

TEST_EXTRACT_PARAMS = {
    "cities": ["Berlin", "Paris", "London"],
    "countries": ["Germany", "France", "United Kingdom"],
    "lats": [52.5200, 48.8566, 51.5074],
    "lons": [13.4050, 2.3522, -0.1278],
}

TEST_MOCK_POLLUTANT_VALUES = {
    "pm2_5": 12.5,
    "pm10": 25.0,
    "ozone": 40.0,
    "nitrogen_dioxide": 18.0,
    "sulphur_dioxide": 5.0,
    "carbon_monoxide": 0.8,
}


# ==========================================
# UI & VISUALIZATION CONFIGURATIONS
# ==========================================

COLOR_MAP = {
    "Low Risk": "#00E676",
    "Moderate Risk": "#FFB300",
    "High Risk": "#FF5252"
}

BG_COLOR_PRIMARY = "#1B3A65"
BG_COLOR_SECONDARY = "#18191C"

APP_BACKGROUND = f"radial-gradient(circle at 10% 40%, {BG_COLOR_PRIMARY} 0%, {BG_COLOR_SECONDARY} 50%)"

APP_TEXT_COLOR = "#F0F4FC"
TITLE_COLOR = "#FFFFFF"

FONT_IMPORT_URL = "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap"
TITLE_FONT_FAMILY = "'Space Grotesk', sans-serif"