import streamlit as st
import pandas as pd
import numpy as np
import ast
import html
import bm25s
import json
from urllib.request import urlopen
import plotly.express as px


def load_data(file):
    '''loads the data'''

    data = pd.read_csv(file)

    data['theme'] = data["theme"].apply(ast.literal_eval)
    data['country'] = data["country"].apply(ast.literal_eval)

    data['extract'] = data['extract'].str.replace("\n", " ")

    return data

def home_page_cards(title, text, width="100%", height="120px", background_color="#f29e62"):

    '''
    adds a card to the streamlit app
    '''

    st.markdown(
            f"""
            <div style="
                width: {width};
                height: {height};
                border-radius:15px;
                background:{background_color};
                text-align:center;
            ">
            <h2>{title}</h2>
            <p>{text}</p>
            </div>
            """,
            unsafe_allow_html=True
        )


def scrollable_results(results):

    cards_html = ""


    for _, row in results.iterrows():

        title = html.escape(str(row['title']))
        extract = html.escape(str(row["extract"]))

        if len(extract) > 200:
            extract = extract[:200] + "..."

        authors = row['authors']

        if not authors:
            authors = "No author found for this extract"

        date = row['date']

        if not date:
            date = "No date found for this extract"


        cards_html += f"""
        <div class="card">
            <h3><strong>Title</strong>: {title}</h3>
            <p><strong>Author</strong>: {authors}</p>
            <p><strong>Date</strong>: {date}</p>
            <p><strong>Extract</strong>: {extract}</p>
        </div>
        """


    st.markdown(
        f"""
        <style>

        .results-box {{
            height: 500px;
            overflow-y: auto;
            padding: 5px;
        }}

        .card {{
            background-color: #f4c6a5;
            border-radius: 15px;
            padding: 5px;
            margin-bottom: 5px;
        }}

        .card h3 {{
            font-size: 14px;
            text-align: justified;
        }}

        .card p {{
            font-size: 12px;
            text-align: justified;
        }}

        </style>

        <div class="results-box">

            {cards_html}

        </div>
        """,
        unsafe_allow_html=True
    )

@st.cache_resource
def load_index(df):

    df = df.reset_index(drop=True)

    # building the corpus to search on
    corpus = df['extract']
    corpus = list(corpus)


    # initialising the retriever
    retriever = bm25s.BM25(corpus=corpus)
    retriever.index(bm25s.tokenize(corpus))

    return retriever


def search_documents(query, df, retriever):

    # defining the number of results that should be returned
    k = len(df)

    # tokenising the query
    query = bm25s.tokenize(query)

    # searching
    results, scores = retriever.retrieve(query, k=k)

    # keeping only the relevant scores
    best_score = scores[0][0]
    results_to_keep = []

    for result, score in zip(results[0], scores[0]):

        if score > 0.1*best_score:
            results_to_keep.append(result)

    searched_df = df[df['extract'].apply(lambda x: x in results_to_keep)]

    return searched_df

@st.cache_resource
def get_data_to_plot(df):

    data_to_plot = (
        df['country']
        .explode() # getting one line per country in the country list
        .value_counts() # counting the number of occurences per country
        .reset_index(name="count") # resetting the index
    )

    return data_to_plot

@st.cache_resource
def load_africa_geojson():

    with urlopen('https://raw.githubusercontent.com/LiaScript/GeoJson/refs/heads/master/africa.geo.json') as response:
        countries = json.load(response)

    return countries

def plot_map(df, countries):

    if len(df) > 0:
        max_country = max(df['count'])
    else:
        max_country = 1

    fig = px.choropleth(df,
                     geojson=countries,
                     featureidkey="properties.name_long",
                     locations='country', 
                     color='count',
                     color_continuous_scale="oranges",
                     range_color=(0, max_country),
                     scope="africa",
                     labels={'count':'number of human rights violations found'}
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        coloraxis_colorbar={
                            "orientation":"h",
                            "yanchor":"bottom",
                            "y":-0.1,
                            "xanchor":"center",
                            "x":0.5,
                            "title":{"side":"top",
                                    "font":{"size":10}},
                            "len":0.75
                            }
                        )
    fig.update_traces(
        hovertemplate=
            "<b>%{location}</b><br>" +
            "%{z} human rights violations found<br>" +
            "<extra></extra>"
    )

    return fig

@st.cache_resource
def return_theme_options(df):

    options = pd.unique(df['theme'].explode())

    option_map = {}

    for option in options:
        if option is not np.nan:
            to_print_version = str.capitalize(option)

            n_results = len(df[df['theme'].apply(lambda x: option in x)])

        else:
            to_print_version = "Other"

            n_results = len(df[df['theme'].apply(lambda x: x == [])])
            
        to_print_version = to_print_version + f" ({n_results} results)"

        option_map[option] = to_print_version

    return(option_map)

def return_theme_selection(df, selection):

    if np.nan not in selection:
        df_selected = df[df['theme'].apply(lambda x: any(item in selection for item in x))]

    else:
        selection.remove(np.nan)

        df_selected = df[df['theme'].apply(lambda x: any(item in selection for item in x)
                                                or x == [])]

    return df_selected

@st.dialog("Country details")
def show_country_detail(country, df):
    # header: name of the selected country
    st.header(f"Selected country: {country}")

    # number of lines 
    selected_data = df[df['country'].apply(lambda x: country in x)]
    st.write(f"{len(selected_data)} human rights violations found")

    # bar chart
    selected_data_to_plot = (
        selected_data['theme']
        .explode()
        .value_counts()
        .reset_index(name="count")
        )

    fig = px.bar(selected_data_to_plot, x="count", y="theme")

    fig.update_traces(marker_color="orange",
                      hovertemplate=
                                  "<b>%{y}</b><br>" +
                                  "%{x} human rights violations found<br>" +
                                  "<extra></extra>")

    fig.update_layout(
        yaxis=dict(
            tickangle=-45,
            title=""
        ),
        xaxis=dict(title="Count")
    )
    st.plotly_chart(fig)








    



