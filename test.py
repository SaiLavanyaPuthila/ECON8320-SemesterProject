import streamlit as st
import pandas as pd
import plotly.express as px


# Prepare the dataframe for visualization
def prepare_df(df):
    df = df.sort_values(by=["year", "period"])
    df["year_period"] = df["year"].astype(str) + " " + df["periodName"]
    return df


# Filter data based on selected year range
def filter_df(df, selected_year):
    return df[(df["year"] >= selected_year[0]) & (df["year"] <= selected_year[1])]


def plot_stacked_bar_chart():
    # Load the datasets
    df_unemployment = pd.read_csv("data/LNS13000000.csv")
    df_nonfarm = pd.read_csv("data/CES0000000001.csv")
    df_hourly_earnings = pd.read_csv("data/CES0500000003.csv")

    # Prepare each dataframe
    df_unemployment = prepare_df(df_unemployment)
    df_nonfarm = prepare_df(df_nonfarm)
    df_hourly_earnings = prepare_df(df_hourly_earnings)

    # Find the common year range
    min_year = max(
        df_unemployment["year"].min(),
        df_nonfarm["year"].min(),
        df_hourly_earnings["year"].min(),
    )
    max_year = min(
        df_unemployment["year"].max(),
        df_nonfarm["year"].max(),
        df_hourly_earnings["year"].max(),
    )

    # Sidebar for year selection
    st.sidebar.header("Filter Data by Year")
    selected_year = st.sidebar.slider(
        "Select Year",
        min_value=int(min_year),
        max_value=int(max_year),
        value=(int(min_year), int(max_year)),
        step=1,
    )

    # Filter dataframes based on the selected year range
    filtered_unemployment = filter_df(df_unemployment, selected_year)
    filtered_nonfarm = filter_df(df_nonfarm, selected_year)
    filtered_hourly_earnings = filter_df(df_hourly_earnings, selected_year)

    # Merge the dataframes on 'year_period'
    merged_df = pd.merge(
        filtered_unemployment[["year_period", "value"]],
        filtered_nonfarm[["year_period", "value"]],
        on="year_period",
        suffixes=("_unemployment", "_nonfarm"),
    )
    merged_df = pd.merge(
        merged_df,
        filtered_hourly_earnings[["year_period", "value"]],
        on="year_period",
    )
    merged_df = merged_df.rename(
        columns={
            "value_unemployment": "Civilian Unemployment",
            "value_nonfarm": "Total Nonfarm Employment",
            "value": "Average Hourly Earnings",
        }
    )

    # Create a stacked bar chart using Plotly
    st.title("Economic Indicators: Stacked Bar Chart")
    st.write(
        "Visualize trends in Civilian Unemployment, Total Nonfarm Employment, and Average Hourly Earnings over time."
    )

    fig = px.bar(
        merged_df,
        x="year_period",
        y=[
            "Civilian Unemployment",
            "Total Nonfarm Employment",
            "Average Hourly Earnings",
        ],
        labels={"value": "Value", "year_period": "Year/Period"},
        title="Stacked Bar Chart of Economic Indicators",
    )

    st.plotly_chart(fig, use_container_width=True)


# if __name__ == "__main__":
#     plot_stacked_bar_chart()

plot_stacked_bar_chart()