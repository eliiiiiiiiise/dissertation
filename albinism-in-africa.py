import pandas as pd
import numpy as np
import ast

import streamlit as st

from utils import home_page_cards, load_data

# ------------- Downloading the data -------------
# ------------------------------------------------

data = load_data("data/full_cleaned_dataset.csv")


st.set_page_config(page_title="Home Page",
                   layout="wide",
                   initial_sidebar_state="collapsed")


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

row1 = st.columns([0.9, 0.1])


with row1[1]:
    st.page_link(page="pages/dashboard.py",
                     label=":orange-background[See more]",
                     icon=":material/arrow_forward:")

st.space("small")


# ------------- Second row : total numbers -------------
# ------------------------------------------------------

row2 = st.columns([1, 1])

with row2[0]:

    n_documents_analysed = len(pd.unique(data['url']))

    home_page_cards(title=str(n_documents_analysed),
                    text="Documents analysed",
                    width="90%",
                    height="70px",
                    background_color="#f29e62")

with row2[1]:

    n_human_rights_violations = len(data)

    home_page_cards(title=str(n_human_rights_violations),
                    text="Human rights violations found",
                    width="90%",
                    height="70px",
                    background_color="#f29e62")


st.space("small")

# ------------- Third / fourth row : numbers by theme -------------
# -----------------------------------------------------------------

row3 = st.columns([1, 1, 1, 1])

with row3[0]:

    n_right_to_life = len(data[data['theme'].apply(lambda x: "right to life" in x)])

    home_page_cards(title=str(n_right_to_life),
                    text="Human rights violations related to the right to life",
                    width="90%",
                    height="100px",
                    background_color="#f4c6a5")

with row3[1]:

    n_access_to_justice = len(data[data['theme'].apply(lambda x: "access to justice" in x)])
    
    home_page_cards(title=str(n_access_to_justice),
                    text="Human rights violations related to access to justice",
                    width="90%",
                    height="100px",
                    background_color="#f4c6a5")

with row3[2]:

    n_right_to_education = len(data[data['theme'].apply(lambda x: "right to education" in x)])

    home_page_cards(title=str(n_right_to_education),
                    text="Human rights violations related to the right to education",
                    width="90%",
                    height="100px",
                    background_color="#f4c6a5")
with row3[3]:

    n_right_to_work = len(data[data['theme'].apply(lambda x: "right to work" in x)])

    home_page_cards(title=str(n_right_to_work),
                    text="Human rights violations related to the right to work",
                    width="90%",
                    height="100px",
                    background_color="#f4c6a5")

st.space("xsmall")

row4 = st.columns([1, 1, 1])

with row4[0]:

    n_adequate_standard_of_living = len(data[data['theme'].apply(lambda x: "adequate standard of living" in x)])

    home_page_cards(title=str(n_adequate_standard_of_living),
                    text="Human rights violations related to adequate standards of living",
                    width="90%",
                    height="100px",
                    background_color="#f4c6a5")

with row4[1]:

    n_right_to_health = len(data[data['theme'].apply(lambda x: "right to health" in x)])

    home_page_cards(title=str(n_right_to_health),
                    text="Human rights violations related to the right to health",
                    width="90%",
                    height="100px",
                    background_color="#f4c6a5")

with row4[2]:

    n_others = len(data[data['theme'].apply(lambda x: x == [])])

    home_page_cards(title=n_others,
                    text="Other types of human rights violations",
                    width="90%",
                    height="100px",
                    background_color="#f4c6a5")










