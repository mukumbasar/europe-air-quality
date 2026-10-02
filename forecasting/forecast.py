# forecasting/forecast.py

import pandas as pd
from prophet import Prophet

from config import DEFAULT_POLLUTANTS, FORECAST_DATA_COLUMN_ORDER


def forecast_air_quality(
    historical_df: pd.DataFrame,
    pollutants: list[str] = None,
    forecast_days: int = 1095,
    covid_start: str = "2020-03-01",
    covid_end: str = "2020-12-31",
) -> pd.DataFrame:
    """Create daily air quality forecasts for each city and pollutant."""
    target_pollutants = pollutants or DEFAULT_POLLUTANTS

    covid_lockdown_holidays = pd.DataFrame({
        "holiday": "covid_lockdown",
        "ds": pd.date_range(covid_start, covid_end),
        "lower_window": 0,
        "upper_window": 0,
    })

    city_forecast_list = []

    for city in historical_df["city"].unique():
        city_historical_df = historical_df[historical_df["city"] == city]
        country_name = city_historical_df["country"].iloc[0]

        city_forecast_df = pd.DataFrame()

        for pollutant in target_pollutants:
            prophet_train_df = (
                city_historical_df[["date", pollutant]]
                .rename(columns={"date": "ds", pollutant: "y"})
                .dropna() ## Drop rows with null values
            )

            prophet_model = Prophet(
                holidays=covid_lockdown_holidays,
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=False,
            )
            prophet_model.fit(prophet_train_df)

            future_dates_df = prophet_model.make_future_dataframe(
                periods=forecast_days, freq="D", include_history=False
            )
            pollutant_forecast = prophet_model.predict(future_dates_df)

            if "date" not in city_forecast_df.columns:
                city_forecast_df["date"] = pollutant_forecast["ds"]

            city_forecast_df[pollutant] = pollutant_forecast["yhat"]

        city_forecast_df["city"] = city
        city_forecast_df["country"] = country_name
        city_forecast_list.append(city_forecast_df)

    final_forecast_df = pd.concat(city_forecast_list, ignore_index=True)
    return final_forecast_df[FORECAST_DATA_COLUMN_ORDER]