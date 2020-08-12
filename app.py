import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache
def get_data():
    url = "http://data.insideairbnb.com/united-states/ny/new-york-city/2019-09-12/visualisations/listings.csv"
    return pd.read_csv(url)
df = get_data()

st.title("Hello streamlit")
st.subheader("My first streamlit app")
st.write("COVID-19 dashboard app coming soon")

st.dataframe(df.head())
