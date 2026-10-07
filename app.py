# app.py

import streamlit as st

from dashboard import (
    get_cached_map_data,
    get_cached_thresholds,
    render_map,
    render_pollutant_info,
    render_pollutant_selector,
)
from dashboard.components.modal import render_city_modal

# Configure Streamlit page settings
st.set_page_config(
    page_title="European Air Quality Monitor",
    layout="wide",
)
st.title("European Air Quality Monitor")

def main():
    # Fetch active thresholds from cache for selector and map color coding 
    thresholds_df = get_cached_thresholds()
    
    # ==========================================
    # SELECTOR & INFO BOX
    # ==========================================
    
    # Create a two columns layout: one for pollutant selector, one for info box
    col_selector, col_info = st.columns([2, 1])

    with col_selector:
        selected_pollutant, mid_limit, high_limit = render_pollutant_selector(
            thresholds_df
        )

    with col_info:
        render_pollutant_info()

    # ==========================================
    # MAP
    # ==========================================

    # Fetch latest readings per city from cache
    map_data = get_cached_map_data(selected_pollutant)

    # Render map component
    map_event = render_map(map_data, selected_pollutant, mid_limit, high_limit)

    # ==========================================
    # MODAL
    # ==========================================

    # Listen for map click events on city nodes to trigger a details modal
    if map_event.selection.get("points"):
        clicked_point = map_event.selection["points"][0]
        city_name = clicked_point["customdata"][3] # Assume city_name is on the 4th index
        render_city_modal(city_name, selected_pollutant)


if __name__ == "__main__":
    main()
