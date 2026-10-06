# app.py

import streamlit as st

from dashboard import (
    render_map,
    render_pollutant_info,
    render_pollutant_selector,
)
from db import get_engine, get_latest_map_data, get_pollutant_thresholds

st.set_page_config(
    page_title="European Air Quality Monitor",
    layout="wide",
)


def main():
    st.title("European Air Quality Monitor")

    engine = get_engine()

    # Fetch active thresholds from DB
    thresholds_df = get_pollutant_thresholds(engine)

    # Side-by-side layout using columns
    col_selector, col_info = st.columns([2, 1])

    with col_selector:
        selected_pollutant, mid_limit, high_limit = render_pollutant_selector(
            thresholds_df
        )

    with col_info:
        render_pollutant_info()

    if not selected_pollutant:
        return

    # Fetch latest readings per city from DB
    map_data = get_latest_map_data(engine, selected_pollutant)

    # Render map component
    render_map(map_data, selected_pollutant, mid_limit, high_limit)


if __name__ == "__main__":
    main()
