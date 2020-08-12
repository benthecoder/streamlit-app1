import streamlit as st
import pandas as pd
import numpy as np
import plotly as plt

st.title("Covid-19 Dashboard")
st.subheader("Data Source: Our World in Data")

DATA_URL = ('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')

@st.cache
def load_data():
    data = pd.read_csv(DATA_URL)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    return data
df = load_data()

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df)
