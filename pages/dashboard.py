import pandas as pd
import numpy as np
import ast
import html
import bm25s
import json
from urllib.request import urlopen
import plotly.express as px


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

# ------------- Initialising session state variables -------------
# ----------------------------------------------------------------

option_map = return_theme_options(data)

if 'selection' not in st.session_state:
    st.session_state['selection'] = []

if 'query' not in st.session_state:
    st.session_state['query'] = None

# filtering the data

if st.session_state['selection'] != []:
    data_to_use = return_theme_selection(data_to_use, st.session_state['selection'])

if len(data_to_use):
    # getting the retriever object based on the options that were selected above
    retriever = load_index(data_to_use)

    if st.session_state['query']:
        data_to_use = search_documents(query=st.session_state['query'], df=data_to_use, retriever=retriever)


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

    selection = st.pills(
        label="Select the themes you want to see displayed",
        options=option_map.keys(),
        selection_mode="multi",
        format_func=lambda option: option_map[option],
        default=st.session_state['selection'],
        key="selection"
        )

    # map
    countries = load_africa_geojson()

    data_to_plot = get_data_to_plot(data_to_use)

    fig = plot_map(data_to_plot, countries)

    st.plotly_chart(fig)



# ------------- Right row -------------
# -------------------------------------


with main_row[1]:

    # search bar

    query = st.text_input(
        "Search extracts",
        icon=":material/search:",
        placeholder="Enter keywords...",
        key="query"
    )

    if len(data_to_use) > 0:
        # number of rows displayed
        st.badge(f"{len(data_to_use)} rows displayed below", color="gray")

        # show the search results
        scrollable_results(data_to_use)

    else:
        st.badge("No data to display", color="red", icon="🚨")
        







