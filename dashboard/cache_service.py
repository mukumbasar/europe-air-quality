# dashboard/cache_service.py

import streamlit as st
from db import get_engine, get_latest_map_data, get_pollutant_thresholds, get_forecast_air_quality, get_processed_air_quality


@st.cache_resource
def _get_cached_engine():
    return get_engine()


@st.cache_data
def get_cached_thresholds():
    engine = _get_cached_engine()
    return get_pollutant_thresholds(engine)


@st.cache_data
def get_cached_map_data(pollutant: str):
    engine = _get_cached_engine()
    return get_latest_map_data(engine, pollutant)


@st.cache_data
def get_cached_forecast_data(city: str, pollutant: str):
    engine = _get_cached_engine()
    return get_forecast_air_quality(engine, city, pollutant)


@st.cache_data
def get_cached_processed_data(city: str, pollutant: str):
    engine = _get_cached_engine()
    return get_processed_air_quality(engine, city, pollutant)