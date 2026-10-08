# app.py

import streamlit as st

from dashboard import (
    get_cached_map_data,
    get_cached_thresholds,
    render_city_modal,
    render_main_page_layout,
    render_map,
    render_monitor_info,
    render_pollutant_info,
    render_pollutant_selector,
)

# Configure page settings and apply styles from main_page
render_main_page_layout()

st.title("Europe Air Quality")

def main():
    # Fetch active thresholds from cache for selector and map color coding 
    thresholds_df = get_cached_thresholds()
    
    # ==========================================
    # SELECTOR & INFO BOX
    # ==========================================
    
    col_selector, _, col_info = st.columns([0.5, 0.2, 0.2])

    with col_selector:
        selected_pollutant = render_pollutant_selector(
            thresholds_df
        )
        # Fetch latest readings per city from cache
        map_data = get_cached_map_data(selected_pollutant)
        mid_limit, high_limit = render_monitor_info(
            selected_pollutant, thresholds_df, map_data
        )

    with col_info:
        render_pollutant_info()

    # ==========================================
    # MAP
    # ==========================================

    # Render map component
    map_event = render_map(map_data, selected_pollutant, mid_limit, high_limit)

    # ==========================================
    # MODAL
    # ==========================================

    # Utilize map_event to trigger modal
    if map_event and map_event.selection and map_event.selection.get("points"):
        clicked_point = map_event.selection["points"][0]
        city_name = clicked_point["customdata"][3] # Assume city_name is on the 4th index
        render_city_modal(city_name, selected_pollutant)


if __name__ == "__main__":
    main()