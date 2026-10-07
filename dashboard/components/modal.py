# components/modal.py

import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard.cache_service import get_cached_forecast_data, get_cached_processed_data
from dashboard.helpers import format_pollutant_name


@st.dialog("City Air Quality Details", width="large")
def render_city_modal(city: str, pollutant: str):
    """Renders a modal popup containing historical and forecast charts for a selected city."""
    # Format the pollutant name using the helper function
    formatted_pollutant = format_pollutant_name(pollutant)
    st.caption(f"Analyzing pollutant metric: {formatted_pollutant}")

    # Fetch cached data for the selected city
    with st.spinner(f"Loading data for {city}..."):
        forecast_df = get_cached_forecast_data(city, pollutant)
        processed_df = get_cached_processed_data(city, pollutant)

    if forecast_df.empty and processed_df.empty:
        st.warning(f"No data available for {city}.")
        return

    # Visualize Forecast Data
    if not forecast_df.empty:
        st.subheader("14-Day Forecast")
        fig_forecast = px.line(
            forecast_df,
            x="date",
            y="value",
            markers=True,
        )
        fig_forecast.update_layout(
            xaxis_title="Date",
            yaxis_title="Value",
            margin=dict(l=20, r=20, t=40, b=20),
            height=300
        )
        st.plotly_chart(fig_forecast, use_container_width=True)

    # Visualize Processed/Historical Data if available
    if not processed_df.empty:
        st.subheader("Historical Data")
        col1, col2 = st.columns([1, 3])
        with col1:
            time_range = st.selectbox(
                "Select range",
                ["Last 14 Days", "Last 3 Months", "Last Year", "Entire Collected History"],
                key=f"hist_range_{city}_{pollutant}",
                label_visibility="collapsed"
            )
        
        df_filtered = processed_df.copy()
        df_filtered["date"] = pd.to_datetime(df_filtered["date"])
        max_date = df_filtered["date"].max()
        
        if time_range == "Last 14 Days":
            df_filtered = df_filtered[df_filtered["date"] >= max_date - pd.Timedelta(days=14)]
        elif time_range == "Last 3 Months":
            df_filtered = df_filtered[df_filtered["date"] >= max_date - pd.DateOffset(months=3)]
        elif time_range == "Last Year":
            df_filtered = df_filtered[df_filtered["date"] >= max_date - pd.DateOffset(years=1)]

        fig_processed = px.line(
            df_filtered,
            x="date",
            y="value",
        )
        fig_processed.update_layout(
            xaxis_title="Date",
            yaxis_title="Value",
            margin=dict(l=20, r=20, t=40, b=20),
            height=300
        )
        st.plotly_chart(fig_processed, use_container_width=True)