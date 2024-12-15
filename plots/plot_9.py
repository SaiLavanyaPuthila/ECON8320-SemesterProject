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
    df = df.rename(columns={"value": "value"})
    return df


# Filter data based on selected year range
def filter_df(df, selected_year):
    return df[(df["year"] >= selected_year[0]) & (df["year"] <= selected_year[1])]


def plot_9():
    # Load datasets
    df_cpi = pd.read_csv("data/CUUR0000SA0.csv")  # CPI-U
    df_earnings = pd.read_csv("data/CES0500000003.csv")  # Average Hourly Earnings

    df_cpi = prepare_df(df_cpi)
    df_earnings = prepare_df(df_earnings)

    # Find the common year range
    min_year = max(
        df_cpi["year"].min(),
        df_earnings["year"].min(),
    )
    max_year = min(
        df_cpi["year"].max(),
        df_earnings["year"].max(),
    )

    # Sidebar for year selection
    st.sidebar.header("Filter Data")
    selected_year = st.sidebar.slider(
        "Select Year",
        min_value=int(min_year),
        max_value=int(max_year),
        value=(int(min_year), int(max_year)),
        step=1,
        key=12,
    )

    filtered_df_cpi = filter_df(df_cpi, selected_year)
    filtered_df_earnings = filter_df(df_earnings, selected_year)

    # ----------------------------------- Dual-Axis Line Chart ------------------------------------
    st.title("Cost of Living and Consumer Economics")
    st.write(
        "Track CPI-U and Average Hourly Earnings over time to measure whether wages are keeping pace with the cost of living."
    )
    st.write("Assesses the economic burden on consumers.")

    # Merging dataframes for dual-axis line chart
    merged_df_dual = pd.merge(
        filtered_df_cpi[["year_period", "value"]],
        filtered_df_earnings[["year_period", "value"]],
        on="year_period",
        suffixes=("_cpi", "_earnings"),
    )
    merged_df_dual = merged_df_dual.rename(
        columns={
            "value_cpi": "CPI-U",
            "value_earnings": "Average Hourly Earnings",
        }
    )

    # Create dual-axis line chart
    fig_dual = make_subplots(specs=[[{"secondary_y": True}]])

    fig_dual.add_trace(
        go.Scatter(
            x=merged_df_dual["year_period"],
            y=merged_df_dual["CPI-U"],
            name="CPI-U",
            mode="lines",
        ),
        secondary_y=False,
    )

    fig_dual.add_trace(
        go.Scatter(
            x=merged_df_dual["year_period"],
            y=merged_df_dual["Average Hourly Earnings"],
            name="Average Hourly Earnings",
            mode="lines",
        ),
        secondary_y=True,
    )

    # Update layout
    fig_dual.update_layout(
        title="<b>CPI-U vs. Average Hourly Earnings</b>",
        xaxis_title="Year Period",
    )

    fig_dual.update_yaxes(title_text="<b>CPI-U</b>", secondary_y=False)
    fig_dual.update_yaxes(title_text="<b>Average Hourly Earnings</b>", secondary_y=True)

    st.plotly_chart(fig_dual, use_container_width=True)


if __name__ == "__main__":
    plot_9()
