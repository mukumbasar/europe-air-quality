# app.py

import streamlit as st

from dashboard import (
    get_cached_map_data,
    get_cached_thresholds,
    render_map,
    render_pollutant_info,
    render_pollutant_selector,
)

st.set_page_config(
    page_title="European Air Quality Monitor",
    layout="wide",
)


def main():
    st.title("European Air Quality Monitor")

    # Fetch active thresholds from cache
    thresholds_df = get_cached_thresholds()

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

    # Fetch latest readings per city from cache
    map_data = get_cached_map_data(selected_pollutant)

    # Render map component
    render_map(map_data, selected_pollutant, mid_limit, high_limit)


if __name__ == "__main__":
    main()
