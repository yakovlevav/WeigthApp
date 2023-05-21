import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import datetime

st.title('Weight calculator')
# uploaded_file = st.file_uploader("Upload files")
uploaded_file = 'weight_data.csv'
df_weights_clean = pd.read_csv(uploaded_file, 
                parse_dates = [0], 
                index_col='Date',
                ).dropna()

add_date = st.date_input(
    "Date",
    datetime.datetime.now())
weight_input = st.number_input('Insert weight')
insert_new_data = pd.DataFrame([weight_input], index=[add_date], columns=["Weight"])

csv = df_weights_clean.to_csv()

st.dataframe(df_weights_clean)

# st.download_button(
# "Press to Download",
# csv,
# "weight_data.csv",
# "text/csv",
# key='download-csv'
# )

df_weights = df_weights_clean

df_weights['week'] = df_weights.index.strftime('%yw%V')
df_weights['Weight'] = df_weights['Weight'].astype('float')
df_weights[ 'roll' ] = df_weights.Weight.rolling(7).mean()

d_start = st.date_input(
    "Start date",
    datetime.date(2023, 1, 1))

d_end = st.date_input(
    "End date",
    datetime.datetime.now())

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

st.header("Running")
df_run = pd.read_csv('Activities.csv', parse_dates=['Date', 'Time'], index_col='Date')

def find_speed(a):
    # Return km in h spead 
    return( (a.hour+a.minute/60+a.second/(60*60) ))

def convert_pace(pace, pulse):
    #Convert to speed in km per hour
    speed = 1/pace*60
    effectiveness = 1/(speed / (pulse * 60) )/1000
    return(effectiveness)

df_run['Time_h'] = df_run['Time'].map(find_speed)
df_run['Speed'] = df_run['Distance']/df_run['Time_h']
df_run['Effective'] = 1/ ( df_run['Speed']/ ( df_run['Avg HR']*60 ) )/1000# beats to meter
df_run['week'] = df_run.index.strftime('%yw%V')
df_run[ 'roll' ] = df_run.Effective.rolling(7).mean()

run_effective_plot = px.box(df_run, x="week", y="Effective")
st.plotly_chart(run_effective_plot)