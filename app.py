import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pydeck as pdk

st.title("Covid-19 Dashboard")
st.subheader("Data Source: CSSE at Johns Hopkins University ")

#Load and Cache the data
@st.cache(persist=True)
def getmedata():
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    df = pd.read_csv(url, delimiter=',', header='infer')
    df.rename(index=lambda x: df.at[x, 'Country/Region'], inplace=True)
    dft = df.loc[df['Province/State'].isnull()]
    dft = dft.transpose()
    dft = dft.drop(['Province/State', 'Country/Region', 'Lat', 'Long'])
    dft.index = pd.to_datetime(dft.index)
    dft['Worldwide']= dft.sum(axis=1)
    return(dft, df)
df1 = getmedata()[0]

countrylist = df1.columns.tolist()
countrylist1 = ['Worldwide']
x = st.multiselect('Choose countries', countrylist, countrylist1)
df1_inscope = df1[x]
dailytotal = st.selectbox('Toggle between Daily and Total number of deaths', ('Total', 'Daily'))
if dailytotal == 'Total':
    plotdata = df1_inscope #day on day changes
else:
    plotdata = df1_inscope.diff()

# Move to Line graph
if dailytotal == 'Total':
    st.header('Total Number of deaths: ' + str(plotdata.iloc[:, 0][plotdata.index[-1]]))
else:
    st.header('Daily number of deaths')
fig = px.line()
for i,n in enumerate(plotdata.columns):
    fig.add_scatter(x=plotdata.index, y= plotdata[plotdata.columns[i]], name= plotdata.columns[i])
fig.update_layout(
     xaxis_title = 'Dates'
    ,yaxis_title = 'Number of Deaths'
    ,template = 'seaborn' #"plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"
    ,legend=dict(orientation="h", yanchor = 'top', y = 1.2)
)
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=2, label="2m", step="month", stepmode="backward"),
            dict(step="all")
        ]),
        font = dict( color='#000000', size = 11),
    )
)
st.plotly_chart(fig, use_container_width=True)

showdata = st.sidebar.checkbox('Show Line graph data')
if showdata == True:
    st.dataframe(plotdata)
else:
    st.write()


# Plot a streamlit map
st.header('Explore the epidemic spreading with a map')
df2 = getmedata()[1]
df2.rename(columns={'Lat': 'lat', 'Long': 'lon', 'Province/State': 'Province', 'Country/Region': 'Country'}, inplace=True)

maxslide = len(df2.columns) - 5
slide = st.slider('Day of epidemic spread', 0, maxslide, 50)
datecolumn = df2.columns[slide + 4]
datecolumnlist = [datecolumn]
st.subheader('Cases Recorded on ' + datecolumn)

dfmap = df2[['Country','Province', 'lat', 'lon', datecolumn]]
dfmap = dfmap.replace(0,np.nan).dropna(subset = [datecolumn, 'lat', 'lon'])

st.map(dfmap[['lat','lon']])

mapgraph = st.sidebar.checkbox('Show map data')
if mapgraph == True:
    st.dataframe(dfmap)
    st.write()
else:
    st.write()
