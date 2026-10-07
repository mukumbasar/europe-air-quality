# dashboard/helpers.py

def format_pollutant_name(name: str) -> str:
    mapping = {
        "pm2_5": "PM2.5",
        "pm10": "PM10",
        "ozone": "Ozone",
        "nitrogen_dioxide": "Nitrogen Dioxide",
        "sulphur_dioxide": "Sulphur Dioxide",
        "carbon_monoxide": "Carbon Monoxide",
    }
    
    if name in mapping:
        return mapping[name]
    return name.replace("_", " ").title()


def categorize_air_quality(
    value: float, middle_limit: float, high_limit: float
) -> str:
    if value < middle_limit:
        return "Low Risk"
    elif value < high_limit:
        return "Moderate Risk"
    else:
        return "High Risk"