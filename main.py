import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import datetime

st.title('Weight calculator')

d_start = st.date_input(
    "Start date",
    datetime.date(2023, 1, 1))

d_end = st.date_input(
    "End date",
    datetime.datetime.now())

df_weights_clean = pd.read_csv('weight.csv', 
                   sep=';', 
                   parse_dates = [0], 
                   names=['Date', 'Weight'], 
                   index_col='Date',
                   decimal=',').dropna()

csv = df_weights_clean.to_csv()
st.download_button(
   "Press to Download",
   csv,
   "weight_data.csv",
   "text/csv",
   key='download-csv'
)

df_weights = df_weights_clean

df_weights['week'] = df_weights.index.strftime('%yw%V')
df_weights['Weight'] = df_weights['Weight'].astype('float')
df_weights[ 'roll' ] = df_weights.Weight.rolling(7).mean()


df_weights = df_weights[df_weights.index.date >= d_start]
df_weights = df_weights[df_weights.index.date <= d_end]

weight_scatter = px.scatter(df_weights, y="Weight")
weight_roll = px.line(df_weights, y="roll")

weight_plot = go.Figure(data=weight_scatter.data + weight_roll.data)
st.header("Weight data plot")
st.plotly_chart(weight_plot)
# m_weight = pd.DataFrame()
# m_weight['Weight'] = df_weights.groupby('week').describe()['Weight']['mean']
st.header("Weight by week plot")
week_weight = px.box(df_weights, x="week", y="Weight")

st.plotly_chart(week_weight)


