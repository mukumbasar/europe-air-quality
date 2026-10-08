# dashboard/components/monitor_info.py

import pandas as pd
import streamlit as st
from config import COLOR_MAP
from dashboard.helpers import (
    categorize_air_quality,
    format_pollutant_name,
    get_pollutant_limits,
    get_status_color,
)

def render_monitor_info(selected_pollutant: str, thresholds_df: pd.DataFrame, df: pd.DataFrame) -> tuple[float, float]:
    mid_limit, high_limit = get_pollutant_limits(thresholds_df, selected_pollutant)
    formatted_name = format_pollutant_name(selected_pollutant)

    total_cities = len(df) if not df.empty else 0
    avg_level = df["value"].mean() if not df.empty else 0.0

    avg_status = categorize_air_quality(avg_level, mid_limit, high_limit)
    avg_color = get_status_color(avg_status)

    low_color = COLOR_MAP["Low Risk"]
    mod_color = COLOR_MAP["Moderate Risk"]
    high_color = COLOR_MAP["High Risk"]

    st.markdown(
        f"<span style='font-size: 0.8em; color: #808495;'>"
        f"Thresholds for <b>{formatted_name}</b>: "
        f"<span style='color: {low_color}; font-weight: 600;'>Low Risk</span> &lt; {mid_limit} | "
        f"<span style='color: {mod_color}; font-weight: 600;'>Moderate Risk</span> &lt; {high_limit} | "
        f"{high_limit} &nbsp;&lt;&nbsp; <span style='color: {high_color}; font-weight: 600;'>High Risk</span>"
        f"</span>",
        unsafe_allow_html=True,
    )

    col1, col2, _ = st.columns([0.18, 0.22, 0.6])
    with col1:
        st.metric(label="Total Cities Monitored:", value=total_cities)
    with col2:
        st.metric(label="Average Level:", value=f"{avg_level:.2f} µg/m³")
        st.markdown(
            f"""
            <style>
                [data-testid="stColumn"]:nth-of-type(2) [data-testid="stMetricValue"] {{
                    color: {avg_color};
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )

    return mid_limit, high_limit