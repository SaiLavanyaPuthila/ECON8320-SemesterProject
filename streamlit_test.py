import streamlit as st
import pandas as pd
df = pd.read_csv('data/CES0000000001.csv')
st.dataframe(df.style.highlight_max(axis=0))

st.line_chart(df,x = 'year',y = 'value')