import streamlit as st
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(page_title="BSL Dashboard", layout="wide", page_icon=":bar_chart:")

st.title(":bar_chart: BSL Dashboard")
st.markdown(
    "<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True
)

st.header("Header")
st.subheader("Subheader")
st.info("Info")
st.warning("Warning")

# Load the data
df = pd.read_csv("data/CES0000000001.csv")
df = df.sort_values(by=['year', 'period'])
print(df)
# Combine 'year' and 'periodName' for the x-axis
df['year_period'] = df['year'].astype(str) + " " + df['periodName']

# Sort the data


# Add a slider on the sidebar for year selection
st.sidebar.header("Filter Data")
selected_year = st.sidebar.slider(
    "Select Year",
    min_value=int(df['year'].min()),
    max_value=int(df['year'].max()),
    value=(int(df['year'].min()), int(df['year'].max())),
    step=1,
)

# Filter data based on selected year range
filtered_df = df[(df['year'] >= selected_year[0]) & (df['year'] <= selected_year[1])]

# Line Chart
st.title("Line Chart: Value Over Time")
st.write(
    "This chart shows the `value` over time using a combination of year and period as the x-axis."
)

st.line_chart(data=filtered_df, x='year_period', y='value', use_container_width=True, height=500)
