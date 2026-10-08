# dashboard/components/map.py

import pandas as pd
import plotly.express as px
import streamlit as st
from config import COLOR_MAP
from dashboard.helpers import categorize_air_quality, format_pollutant_name

def render_map(
    df: pd.DataFrame,
    pollutant_name: str,
    middle_limit: float,
    high_limit: float,
):
    if df.empty:
        st.warning(f"No recent data available for {pollutant_name}.")
        return None

    df["status"] = df["value"].apply(
        categorize_air_quality,
        args=(middle_limit, high_limit),
    )

    formatted_pollutant = format_pollutant_name(pollutant_name)

    date_str = ""
    if "date" in df.columns and not df["date"].empty:
        raw_date = pd.to_datetime(df["date"].iloc[0])
        date_str = f" ({raw_date.strftime('%d-%m-%Y')})"

    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.0rem !important;
            padding-bottom: 1.0rem !important;
            max-width: 98% !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    fig = px.scatter_map(
        df,
        lat="latitude",
        lon="longitude",
        hover_name="city",
        custom_data=["status", "country", "value", "city"],
        color="status",
        color_discrete_map=COLOR_MAP,
        zoom=3.4,
        center={"lat": 52.5, "lon": 20.0},
        map_style="carto-darkmatter",
        title=(
            f"Current {formatted_pollutant} Levels Across Europe{date_str}"
            "<br><sub>Air quality data by "
            "<a href='https://open-meteo.com/' target='_blank'>Open-Meteo.com</a> "
            "(CC BY 4.0), based on Copernicus CAMS ENSEMBLE data.</sub>"
        ),
)

    fig.update_traces(
        marker=dict(size=14, opacity=0.9),
        unselected=dict(marker=dict(opacity=0.9)),
        hovertemplate=(
            "<b>%{hovertext}</b><br><br>"
            "<b>Status:</b> %{customdata[0]}<br>"
            "<b>Country:</b> %{customdata[1]}<br>"
            "<b>Value:</b> %{customdata[2]:.2f} µg/m³<extra></extra>"
        ),
        hoverlabel=dict(
            bgcolor="rgba(15, 23, 42, 0.95)",
            bordercolor="rgba(255, 255, 255, 0.2)",
            font_size=13,
            font_color="#FFFFFF",
            font_family="sans-serif",
        ),
    )

    fig.update_layout(
        height=1000,
        margin={"r": 0, "t": 70, "l": 0, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text="Air Quality Status",
        legend=dict(
            yanchor="top",
            y=0.98,
            xanchor="right",
            x=0.99,
            bgcolor="rgba(15, 23, 42, 0.8)",
            bordercolor="rgba(255, 255, 255, 0.2)",
            borderwidth=1,
            font=dict(color="#FFFFFF"),
        ),
        font=dict(color="#FFFFFF"),
    )

    event = st.plotly_chart(
        fig, 
        on_select="rerun", 
        key="map_selection", 
        use_container_width=True
    )
    
    return event