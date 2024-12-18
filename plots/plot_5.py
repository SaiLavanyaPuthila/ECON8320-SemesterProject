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


def plot_5():
    # Load the datasets
    df_earnings = pd.read_csv("data/CES0500000003.csv")
    df_employment = pd.read_csv("data/LNS12000000.csv")
    df_laborforce = pd.read_csv("data/LNS11000000.csv")

    # Prepare the dataframes
    df_earnings = prepare_df(df_earnings)
    df_employment = prepare_df(df_employment)
    df_laborforce = prepare_df(df_laborforce)

    # Find common year range
    min_year = max(
        df_earnings["year"].min(),
        df_employment["year"].min(),
        df_laborforce["year"].min(),
    )
    max_year = min(
        df_earnings["year"].max(),
        df_employment["year"].max(),
        df_laborforce["year"].max(),
    )

    # Sidebar for year selection
    st.sidebar.header("Filter data for plot 5")
    selected_year = st.sidebar.slider(
        "Select Year Range",
        min_value=int(min_year),
        max_value=int(max_year),
        value=(int(min_year), int(max_year)),
        step=1,
        key=7,
    )

    filtered_df_earnings = filter_df(df_earnings, selected_year)
    filtered_df_employment = filter_df(df_employment, selected_year)
    filtered_df_laborforce = filter_df(df_laborforce, selected_year)

    # Merge the dataframes
    merged_df = pd.merge(
        filtered_df_earnings[["year_period", "value"]],
        filtered_df_employment[["year_period", "value"]],
        on="year_period",
        suffixes=("_earnings", "_employment"),
    )
    merged_df = pd.merge(
        merged_df,
        filtered_df_laborforce[["year_period", "value"]],
        on="year_period",
    )
    # Rename columns
    merged_df = merged_df.rename(
        columns={
            "value_earnings": "Average Hourly Earnings",
            "value_employment": "Civilian Employment",
            "value": "Civilian Labor Force",
        }
    )
    # Stacked Area Chart
    st.title("Wage Growth in Relation to Employment and Labor Force Participation")
    st.write(
        "This analysis investigates the interplay between wage growth, employment levels, and labor force participation. It examines how these factors influence each other, revealing the dynamics of compensation within the labor market and providing insights into the relationship between workforce engagement and earnings trends."
    )

    fig = px.area(
        merged_df,
        x="year_period",
        y=[
            "Average Hourly Earnings",
            "Civilian Employment",
            "Civilian Labor Force",
        ],
        title="Wage Growth vs. Employment and Labor Force Participation",
        labels={"value": "Value"},
    )
    fig.update_layout(
        xaxis_title="Year Period",
        yaxis_title="Value",
        legend_title="Indicator",
    )
    fig.update_xaxes(title_text="<b>Period</b>")
    fig.update_yaxes(title_text="<b>Value</b>")
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    plot_5()
