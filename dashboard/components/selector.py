# dashboard/components/selector.py

import pandas as pd
import streamlit as st


def format_pollutant_name(name: str) -> str:
    mapping = {
        "pm2_5": "PM2.5",
        "pm10": "PM10",
        "ozone": "Ozone",
        "nitrogen_dioxide": "Nitrogen Dioxide",
        "sulphur_dioxide": "Sulphur Dioxide",
        "carbon_monoxide": "Carbon Monoxide",
    }
    key = name.lower().strip()
    if key in mapping:
        return mapping[key]
    return name.replace("_", " ").title()


def render_pollutant_selector(thresholds_df: pd.DataFrame) -> tuple[str, float, float]:
    if thresholds_df.empty:
        st.error("No active pollutant thresholds found in database.")
        return "", 0.0, 0.0

    available_pollutants = thresholds_df["pollutant_name"].tolist()

    col_select, _ = st.columns([1, 5])
    with col_select:
        selected_pollutant = st.selectbox(
            "Select Pollutant",
            options=available_pollutants,
            format_func=format_pollutant_name,
            index=0,
        )

    pollutant_row = thresholds_df[
        thresholds_df["pollutant_name"] == selected_pollutant
    ].iloc[0]

    mid_limit = float(pollutant_row["middle_limit"])
    high_limit = float(pollutant_row["high_limit"])
    formatted_name = format_pollutant_name(selected_pollutant)

    st.markdown(
        f"<span style='font-size: 0.8em; color: #808495;'>"
        f"Thresholds for <b>{formatted_name}</b>: "
        f"<span style='color: #00E676; font-weight: 600;'>Low Risk</span> &lt; {mid_limit} | "
        f"<span style='color: #FFB300; font-weight: 600;'>Moderate Risk</span> &lt; {high_limit} | "
        f"{high_limit} &nbsp;&lt;&nbsp; <span style='color: #FF5252; font-weight: 600;'>High Risk</span>"
        f"</span>",
        unsafe_allow_html=True,
    )

    return selected_pollutant, mid_limit, high_limit
