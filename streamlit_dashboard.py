import streamlit as st
import plotly
import pandas
import os

import warnings

warnings.filterwarnings("ignore")


st.set_page_config(
    page_title="BSL Dashboard", layout="wide", page_icon=":bar_chart:"
)

st.title(":bar_chart: BSL Dashboard")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>',unsafe_allow_html=True)

st.header("header")
st.subheader("subheader")
st.info("info")
st.warning("warning")
