# dashboard/components/info_box.py

import streamlit as st


def render_pollutant_info() -> None:
    """Renders an informational sidebar or box explaining the pollutants."""
    st.markdown("### Pollutant Guide")
    st.markdown(
        """
        * **PM2.5:** Fine particulate matter (under 2.5 micrometers) from dust, smoke, and combustion.
        * **PM10:** Coarse particulate matter (under 10 micrometers) from dust, smoke, and combustion.
        * **Ozone ($O_3$):** Ground-level gas created by chemical reactions in sunlight.
        * **Nitrogen Dioxide ($NO_2$):** Gas mainly from vehicle traffic and fossil fuel combustion.
        * **Sulphur Dioxide ($SO_2$):** Gas primarily emitted from industrial power plants.
        * **Carbon Monoxide ($CO$):** Colorless, odorless gas from incomplete combustion; measured on a larger scale.
        """
    )
