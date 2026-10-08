# dashboard/pages/main_page.py

import streamlit as st
from config import (
    APP_BACKGROUND,
    APP_TEXT_COLOR,
    FONT_IMPORT_URL,
    TITLE_COLOR,
    TITLE_FONT_FAMILY,
)

def render_main_page_layout():
    st.set_page_config(
        page_title="Europe Air Quality",
        layout="wide",
    )

    st.markdown(
        f"""
<style>
    @import url('{FONT_IMPORT_URL}');

    header[data-testid="stHeader"] {{
        display: none !important;
    }}

    .block-container {{
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: 0rem !important;
    }}

    h1 {{
        padding-top: 1rem !important;
        margin-top: 0rem !important;
        font-family: {TITLE_FONT_FAMILY} !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
        letter-spacing: -0.8px !important;
        text-transform: uppercase !important;
        color: {TITLE_COLOR} !important;
    }}

    .stApp {{
        background: {APP_BACKGROUND} !important;
        color: {APP_TEXT_COLOR} !important;
    }}
</style>
""",
        unsafe_allow_html=True,
    )