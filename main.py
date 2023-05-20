import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
st.title('Weight calculator')

df_weights = pd.read_csv('weight.csv', 
                   sep=';', 
                   parse_dates = [0], 
                   names=['Date', 'Weight'], 
                   index_col='Date', 
                   decimal=',').dropna()

df_weights['week'] = df_weights.index.strftime('%yw%V')
df_weights['Weight'] = df_weights['Weight'].astype('float')
df_weights[ 'roll' ] = df_weights.Weight.rolling(7).mean()
m_weight = pd.DataFrame()
m_weight['Weight'] = df_weights.groupby('week').describe()['Weight']['mean']
fig, ax = plt.subplots(figsize = (10,6))
rs = sns.boxplot(x="week", y="Weight", data=df_weights, ax=ax)
plt.xticks(rotation=45)

st.pyplot(fig)
