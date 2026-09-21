# forecast.py

import pandas as pd
from prophet import Prophet

from config import DEFAULT_POLLUTANTS, FORECAST_DATA_COLUMN_ORDER


def forecast_air_quality(
    df: pd.DataFrame,
    forecast_months: int = 36,
) -> pd.DataFrame:
    """Create monthly air quality forecasts for each city and pollutant.

    Args:
        df (pd.DataFrame): DataFrame containing historical monthly air
            quality data.
        forecast_months (int, optional): Number of future months to
            forecast. Defaults to 60.

    Returns:
        pd.DataFrame: DataFrame containing monthly forecasts for each
        city and pollutant.
    """

    forecast_df = pd.DataFrame()

    cities = df["city"].unique()

    for city in cities:

        city_rows = df["city"] == city
        city_data = df[city_rows]

        city_forecast = pd.DataFrame()

        for pollutant in DEFAULT_POLLUTANTS:

            model_data = city_data[["date", pollutant]].copy()

            model_data = model_data.rename(
                columns={
                    "date": "ds",
                    pollutant: "y",
                }
            )

            model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=False,
                daily_seasonality=False,
            )

            model.fit(model_data)

            future = model.make_future_dataframe(
                periods=forecast_months,
                freq="MS",
                include_history=False,
            )

            forecast = model.predict(future)

            city_forecast["date"] = forecast["ds"]
            city_forecast[pollutant] = forecast["yhat"]

        city_forecast["city"] = city
        city_forecast["country"] = city_data["country"].iloc[0]

        forecast_df = pd.concat(
            [forecast_df, city_forecast],
            ignore_index=True,
        )

    forecast_df = forecast_df[FORECAST_DATA_COLUMN_ORDER]

    return forecast_df