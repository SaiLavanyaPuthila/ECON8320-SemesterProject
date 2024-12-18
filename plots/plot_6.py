import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# from utils import prepare_df, filter_df
import plotly.express as px


# Sort and prepare each dataframe
def prepare_df(df, cpi=False):
    if cpi:
        df = df.sort_values(by=["year", "period"])
        df["year_period"] = df["year"].astype(str) + " " + df["periodName"]
        df = df.rename(columns={"value": "cpi_value"})
    else:
        df = df.sort_values(by=["year", "period"])
        df["year_period"] = df["year"].astype(str) + " " + df["periodName"]
        df = df.rename(columns={"value": "earnings_value"})
    return df

    # Filter data based on selected year range


def filter_df(df, selected_year):
    return df[(df["year"] >= selected_year[0]) & (df["year"] <= selected_year[1])]


def plot_6():
    # Load datasets
    df_cpi = pd.read_csv("data/CUUR0000SA0.csv")  # CPI-U
    df_earnings = pd.read_csv("data/CES0500000003.csv")  # Average Hourly Earnings

    df_cpi = prepare_df(df_cpi, cpi=True)
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
    st.sidebar.header("Filter data based on year for plot 6")
    selected_year = st.sidebar.slider(
        "Select Year",
        min_value=int(min_year),
        max_value=int(max_year),
        value=(int(min_year), int(max_year)),
        step=1,
        key=16,
    )

    filtered_df_cpi = filter_df(df_cpi, selected_year)
    filtered_df_earnings = filter_df(df_earnings, selected_year)

    # ----------------------------------- Stacked Bar Chart ------------------------------------
    st.title("Cost of Living vs. Wage Growth: A Breakdown of Economic Trends")
    st.write(
        "This chart analyzes the evolution of the Consumer Price Index for All Urban Consumers (CPI-U) across major categories like housing, transportation, food, and healthcare. It also compares these changes with hourly earnings as a reference. The insight helps to understand how cost of living adjustments relate to wage growth over time."
    )

    cpi_components = ["cpi_value"]

    # Merging dataframes
    merged_df_bar = pd.merge(
        filtered_df_cpi[["year_period"] + cpi_components],
        filtered_df_earnings[["year_period", "earnings_value"]],
        on="year_period",
    )

    merged_df_bar = merged_df_bar.rename(
        columns={"earnings_value": "Average Hourly Earnings"}
    )

    # Create a stacked bar chart
    fig_bar = make_subplots(specs=[[{"secondary_y": True}]])

    for component in cpi_components:
        fig_bar.add_trace(
            go.Bar(
                x=merged_df_bar["year_period"],
                y=merged_df_bar[component],
                name=component,
            ),
            secondary_y=False,
        )

    fig_bar.add_trace(
        go.Scatter(
            x=merged_df_bar["year_period"],
            y=merged_df_bar["Average Hourly Earnings"],
            name="Average Hourly Earnings",
            mode="lines",
            line=dict(color="black", width=2, dash="dash"),
        ),
        secondary_y=True,
    )

    # Update layout
    fig_bar.update_layout(
        title="<b>CPI-U Components and Average Hourly Earnings</b>",
        xaxis_title="Year Period",
        legend_title="Indicator",
    )
    fig_bar.update_yaxes(title_text="<b>CPI-U Components</b>", secondary_y=False)
    fig_bar.update_yaxes(title_text="<b>Average Hourly Earnings</b>", secondary_y=True)
    fig_bar.update_xaxes(title_text="<b>Period</b>")

    st.plotly_chart(fig_bar, use_container_width=True)


if __name__ == "__main__":
    plot_6()
