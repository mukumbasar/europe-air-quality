# forecasting/forecast.py

import pandas as pd
from prophet import Prophet

from config import DEFAULT_POLLUTANTS, FORECAST_DATA_COLUMN_ORDER


def forecast_air_quality(
    df: pd.DataFrame,
    pollutants: list[str] = None,
    forecast_days: int = 1095,
    covid_start: str = "2020-03-01",
    covid_end: str = "2020-12-31",
) -> pd.DataFrame:
    """Create daily air quality forecasts for each city and pollutant."""
    pollutants = pollutants or DEFAULT_POLLUTANTS

    covid_holidays = pd.DataFrame({
        "holiday": "covid_lockdown",
        "ds": pd.date_range(covid_start, covid_end),
        "lower_window": 0,
        "upper_window": 0,
    })

    all_city_forecasts = []

    for city in df["city"].unique():
        city_data = df[df["city"] == city]
        country = city_data["country"].iloc[0]

        city_forecast = pd.DataFrame()

        for pollutant in pollutants:
            model_data = (
                city_data[["date", pollutant]]
                .rename(columns={"date": "ds", pollutant: "y"})
                .dropna()
            )

            model = Prophet(
                holidays=covid_holidays,
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=False,
            )
            model.fit(model_data)

            future = model.make_future_dataframe(
                periods=forecast_days, freq="D", include_history=False
            )
            forecast = model.predict(future)

            if "date" not in city_forecast.columns:
                city_forecast["date"] = forecast["ds"]

            city_forecast[pollutant] = forecast["yhat"]

        city_forecast["city"] = city
        city_forecast["country"] = country
        all_city_forecasts.append(city_forecast)

    forecast_df = pd.concat(all_city_forecasts, ignore_index=True)
    return forecast_df[FORECAST_DATA_COLUMN_ORDER]