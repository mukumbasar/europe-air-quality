# dashboard/components/selector.py

import pandas as pd
import streamlit as st
from dashboard.helpers import format_pollutant_name

def render_pollutant_selector(thresholds_df: pd.DataFrame) -> str:
    if thresholds_df.empty:
        st.error("No active pollutant thresholds found in database.")
        return ""

    available_pollutants = thresholds_df["pollutant_name"].tolist()

    col_select, _ = st.columns([1, 5])
    with col_select:
        selected_pollutant = st.selectbox(
            "Select Pollutant:",
            options=available_pollutants,
            format_func=format_pollutant_name,
            index=0,
        )

    return selected_pollutant