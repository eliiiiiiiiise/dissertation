import pandas as pd
import numpy as np
import ast
import html
import bm25s
import json
from urllib.request import urlopen
import plotly.express as px
from streamlit_plotly_events import plotly_events


import streamlit as st

from utils import *

# ------------- Loading the data -------------
# --------------------------------------------

data = load_data("data/full_cleaned_dataset.csv")

data_to_use = data.copy()

# ------------- Setting the page configuration -------------
# ----------------------------------------------------------

st.set_page_config(page_title="Dashboard",
                   layout="wide")

# ------------- First row : title -------------
# ---------------------------------------------

st.markdown(
    """
    <h1 style="text-align: center;">
        Human Rights Watch: Albinism in Africa
    </h1>
    """,
    unsafe_allow_html=True
)

main_row = st.columns([0.6, 0.4])

# ------------- Left row -------------
# ------------------------------------



with main_row[0]:

    # choosing themes

    option_map = return_theme_options(data_to_use)

    selection = st.pills(
        label="Select the themes you want to see displayed",
        options=option_map.keys(),
        selection_mode="multi",
        format_func=lambda option: option_map[option],
        default=option_map.keys()
        )

    data_to_use = return_theme_selection(data_to_use, selection)

    # map
    countries = load_africa_geojson()

    data_to_plot = get_data_to_plot(data_to_use)

    fig = plot_map(data_to_plot, countries)

    event = st.plotly_chart(fig,
                            on_select="rerun")

    points = event.selection.points

    if points:

        country = points[0]["location"]

        show_country_detail(
            country,
            data_to_use
        )
        st.write(f"{country} was selected, click on the country again to view the full map")

        data_to_use = get_country_data(country, data_to_use)
        
    else:
        pass


# ------------- Right row -------------
# -------------------------------------


with main_row[1]:

    # search bar

    query = st.text_input(
        "Search extracts",
        icon=":material/search:",
        placeholder="Enter keywords..."
    )

    if len(data_to_use) > 0:

        # getting the retriever object based on the options that were selected above
        retriever = load_index(data_to_use)

        if query:

            data_to_use = search_documents(query=query, df=data_to_use, retriever=retriever)

        # number of rows displayed
        st.badge(f"{len(data_to_use)} rows displayed below", color="gray")

        # show the search results
        scrollable_results(data_to_use)

    else:
        st.badge("No data to display", color="red", icon="🚨")
        







