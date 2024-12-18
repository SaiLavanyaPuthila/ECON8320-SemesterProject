import streamlit as st
import pandas as pd
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plots.plot_1 import plot_1
from plots.plot_2 import plot_2
from plots.plot_3 import plot_3
from plots.plot_4 import plot_4
from plots.plot_5 import plot_5
from plots.plot_6 import plot_6


warnings.filterwarnings("ignore")

st.set_page_config(page_title="BLS Dashboard", layout="wide", page_icon=":bar_chart:")

st.title(":bar_chart: BLS Dashboard")
st.markdown(
    "<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True
)

plot_1()

plot_2()

plot_3()

plot_4()

plot_5()

plot_6()
