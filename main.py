import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime

st.title('Weight calculator')

d = st.date_input(
    "Start date",
    datetime.date(2023, 1, 1))

df_weights = pd.read_csv('weight.csv', 
                   sep=';', 
                   parse_dates = [0], 
                   names=['Date', 'Weight'], 
                   index_col='Date',
                   decimal=',').dropna()

df_weights['week'] = df_weights.index.strftime('%yw%V')
df_weights['Weight'] = df_weights['Weight'].astype('float')
df_weights[ 'roll' ] = df_weights.Weight.rolling(7).mean()


df_weights = df_weights[df_weights.index.date > d]


m_weight = pd.DataFrame()
m_weight['Weight'] = df_weights.groupby('week').describe()['Weight']['mean']

fig = px.box(df_weights, x="week", y="Weight")

st.plotly_chart(fig)