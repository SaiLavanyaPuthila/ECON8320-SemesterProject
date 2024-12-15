# Load the datasets

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# from utils import prepare_df, filter_df
import plotly.express as px

# Sort and prepare each dataframe
def prepare_df(df):
    df = df.sort_values(by=["year", "period"])
    df["year_period"] = df["year"].astype(str) + " " + df["periodName"]
    return df


# Filter data based on selected year range
def filter_df(df, selected_year):
    return df[(df["year"] >= selected_year[0]) & (df["year"] <= selected_year[1])]

def plot_4():
    df_unemployment = pd.read_csv("data/LNS14000000.csv")  # Unemployment Rate

    df_eci = pd.read_csv("data/CIU2010000000000A.csv")  # Employment Cost Index

    df_unemployment = prepare_df(df_unemployment)
    df_eci = prepare_df(df_eci)

    min_year_scatter = max(df_unemployment["year"].min(), df_eci["year"].min())
    max_year_scatter = min(df_unemployment["year"].max(), df_eci["year"].max())

    st.sidebar.header("Filter Data for Scatter Plot")
    selected_year_scatter = st.sidebar.slider(
        "Select Year (Scatter Plot)",
        min_value=int(min_year_scatter),
        max_value=int(max_year_scatter),
        value=(int(min_year_scatter), int(max_year_scatter)),
        step=1,
        key=8,
    )

    st.title("Labor Market Tightness and Employment Costs")
    st.write(
        "Plot Unemployment Rate against Employment Cost Index to illustrate the relationship between labor market tightness and rising employment costs."
    )
    st.write("Reveals the impact of a tight labor market on wage inflation.")

    # Merging dataframes
    merged_df_scatter = pd.merge(
        df_unemployment[["year", "value"]],
        df_eci[["year", "value"]],
        on="year",
        suffixes=("_unemployment", "_eci"),
    )
    merged_df_scatter = merged_df_scatter.rename(
        columns={
            "value_unemployment": "Unemployment Rate",
            "value_eci": "Employment Cost Index",
        }
    )
    
    merged_df_scatter = filter_df(merged_df_scatter,selected_year_scatter)
    # Scatter plot
    fig_scatter = px.scatter(
        merged_df_scatter,
        x="Unemployment Rate",
        y="Employment Cost Index",
        color="year",  # Use 'year' for coloring
        title="<b>Unemployment Rate vs. Employment Cost Index</b>",
        labels={
            "Unemployment Rate": "Unemployment Rate",
            "Employment Cost Index": "Employment Cost Index",
            "year": "Year",
        },  # Label for the color legend
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

if __name__ == "__main__":
    plot_4()