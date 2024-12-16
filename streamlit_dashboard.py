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
from plots.plot_7 import plot_7
from plots.plot_8 import plot_8
from plots.plot_9 import plot_9
from plots.plot_10 import plot_10


warnings.filterwarnings("ignore")

st.set_page_config(page_title="BSL Dashboard", layout="wide", page_icon=":bar_chart:")

st.title(":bar_chart: BSL Dashboard")
st.markdown(
    "<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True
)


plot_2()

plot_1()



# plot_3()

# plot_4()

plot_5()

plot_6()

plot_7()

# plot_8()

# plot_9()

plot_10()
