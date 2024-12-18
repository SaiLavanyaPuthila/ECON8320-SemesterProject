# Load the datasets

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio


# Sort and prepare each dataframe
def prepare_df(df):
    df = df.sort_values(by=["year", "period"])
    df["year_period"] = df["year"].astype(str) + " " + df["periodName"]
    return df


# Filter data based on selected year range
def filter_df(df, selected_year):
    return df[(df["year"] >= selected_year[0]) & (df["year"] <= selected_year[1])]


def calculate_monthly_change(df):
    df["value_previous"] = df["value"].shift(1)
    df["change"] = df["value"] - df["value_previous"]
    # Drop the first row for calculation purpose
    df = df.iloc[1:, :]

    # Extract the numeric part of 'period'
    df["month"] = df["period"].str[1:].astype(int)  # Slice from index 1 onwards.
    df["year"] = df["year"].astype(int)
    return df


# Simulate recession periods
def categorize_period(year):
    if year < 2008:
        return "Pre-Recession"
    elif year >= 2008 and year <= 2009:
        return "During Recession"
    elif year >= 2010:
        return "Post-Recession"
    return "Other"
    return df


def plot_1():
    df_ces = pd.read_csv("data/CES0000000001.csv")
    df_lns_unemp = pd.read_csv("data/LNS14000000.csv")  # Unemployment Rate
    df_lns_civ_emp = pd.read_csv("data/LNS12000000.csv")  # Civilian Employment

    df_ces = prepare_df(df_ces)
    df_lns_unemp = prepare_df(df_lns_unemp)
    df_lns_civ_emp = prepare_df(df_lns_civ_emp)

    # Find the common year range
    min_year = max(
        df_ces["year"].min(), df_lns_unemp["year"].min(), df_lns_civ_emp["year"].min()
    )
    max_year = min(
        df_ces["year"].max(), df_lns_unemp["year"].max(), df_lns_civ_emp["year"].max()
    )

    st.sidebar.header("Filter data for plot 1")
    selected_year = st.sidebar.slider(
        "Select Year",
        min_value=int(min_year),
        max_value=int(max_year),
        value=(int(min_year), int(max_year)),
        step=1,
        key=200,
    )

    filtered_df_ces = filter_df(df_ces, selected_year)
    filtered_df_lns_unemp = filter_df(df_lns_unemp, selected_year)
    filtered_df_lns_civ_emp = filter_df(df_lns_civ_emp, selected_year)

    # ------------------------------- Dual-Axis Line Chart -----------------------------------
    st.title("Employment Growth and Unemployment Trends: A Dual-Axis Analysis:")
    st.write(
        "This graph visualizes the relationship between Total Nonfarm Employment and the Unemployment Rate over time. It highlights how shifts in employment levels correlate with changes in the unemployment rate during economic cycles."
    )

    merged_df_dual = pd.merge(
        filtered_df_ces[["year_period", "value"]],
        filtered_df_lns_unemp[["year_period", "value"]],
        on="year_period",
        suffixes=("_ces", "_unemp"),
    )
    merged_df_dual = merged_df_dual.rename(
        columns={
            "value_ces": "Total Nonfarm Employment",
            "value_unemp": "Unemployment Rate",
        }
    )
    pio.templates["google"] = go.layout.Template(
        layout_colorway=[
            "#FFD1DC",
            "#F0E68C",
            "#D3C7F3",
            "#ADD8E6",
            "#90EE90",
            "#F8BBD0",
            "#FFB347",
            "#D8BFD8",
        ]
    )

    # setting Google color palette as default
    pio.templates.default = "google"
    # Create the dual-axis plot
    fig_dual = make_subplots(specs=[[{"secondary_y": True}]])

    fig_dual.add_trace(
        go.Scatter(
            x=merged_df_dual["year_period"],
            y=merged_df_dual["Total Nonfarm Employment"],
            name="Total Nonfarm Employment",
            mode="lines",
        ),
        secondary_y=False,
    )
    fig_dual.add_trace(
        go.Scatter(
            x=merged_df_dual["year_period"],
            y=merged_df_dual["Unemployment Rate"],
            name="Unemployment Rate",
            mode="lines",
        ),
        secondary_y=True,
    )

    # Add title and axis labels
    fig_dual.update_layout(
        title_text="<b>Total Nonfarm Employment vs Unemployment Rate</b>",
        xaxis_title="Year Period",
        legend_title="Indicator",
    )
    fig_dual.update_xaxes(title_text="<b>Period</b>")
    fig_dual.update_yaxes(
        title_text="<b>Total Nonfarm Employment</b>", secondary_y=False
    )
    fig_dual.update_yaxes(title_text="<b>Unemployment Rate</b>", secondary_y=True)

    st.plotly_chart(fig_dual, use_container_width=True, key=201)


if __name__ == "__main__":
    plot_1()
