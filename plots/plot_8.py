import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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


def plot_8():
    df_labor_force = pd.read_csv("data/LNS11000000.csv")  # Civilian Labor Force
    df_lns_unemp = pd.read_csv("data/LNS14000000.csv")  # Unemployment Rate
    df_hourly_earnings = pd.read_csv(
        "data/CES0500000003.csv"
    )  # Total Private Avg Hourly Earnings

    df_labor_force = prepare_df(df_labor_force)
    df_lns_unemp = prepare_df(df_lns_unemp)
    df_hourly_earnings = prepare_df(df_hourly_earnings)

    # Find the common year range
    min_year = max(
        df_labor_force["year"].min(),
        df_lns_unemp["year"].min(),
        df_hourly_earnings["year"].min(),
    )
    max_year = min(
        df_labor_force["year"].max(),
        df_lns_unemp["year"].max(),
        df_hourly_earnings["year"].max(),
    )

    st.sidebar.header("Filter data based on year for plot 2,3,4")
    selected_year = st.sidebar.slider(
        "Select Year",
        min_value=int(min_year),
        max_value=int(max_year),
        value=(int(min_year), int(max_year)),
        step=1,
        key=800,
    )

    filtered_df_labor_force = filter_df(df_labor_force, selected_year)
    filtered_df_lns_unemp = filter_df(df_lns_unemp, selected_year)
    filtered_df_hourly_earnings = filter_df(df_hourly_earnings, selected_year)

    # Merge the three dataframes
    merged_df_heatmap = pd.merge(
        filtered_df_labor_force[["year_period", "value"]],
        filtered_df_lns_unemp[["year_period", "value"]],
        on="year_period",
        suffixes=("_laborforce", "_unemp"),
    )
    merged_df_heatmap = pd.merge(
        merged_df_heatmap,
        filtered_df_hourly_earnings[["year_period", "value"]],
        on="year_period",
        suffixes=("_temp", "_earnings"),
    )

    merged_df_heatmap = merged_df_heatmap.rename(
        columns={
            "value_laborforce": "Civilian Labor Force",
            "value_unemp": "Unemployment Rate",
            "value_earnings": "Avg Hourly Earnings",
        }
    )

    # Create the heatmap
    st.title("Heatmap: Labor Force Participation vs. Unemployment Rate and Wages")
    st.write(
        "A heatmap can illustrate the relationships between labor force participation, unemployment rate, and average hourly earnings. Each cell will represent a period (e.g., month or quarter), with color intensity showing the magnitude of each variable. This allows you to identify whether low unemployment coincides with higher wages or if rising labor force participation is reducing wage growth."
    )

    # Set 'year_period' as index for the heatmap
    merged_df_heatmap = merged_df_heatmap.set_index("year_period")

    # Use the plotly go.heatmap
    fig_heatmap = go.Figure(
        data=go.Heatmap(
            z=merged_df_heatmap[["Civilian Labor Force", "Unemployment Rate", "Avg Hourly Earnings"]].T.values,
            x=merged_df_heatmap.index.tolist(),
            y=["Civilian Labor Force", "Unemployment Rate", "Avg Hourly Earnings"],
            colorscale="Viridis",
        )
    )

    fig_heatmap.update_layout(
        title="<b>Heatmap of Labor Market Indicators</b>",
        xaxis_title="Year Period",
        yaxis_title="Indicators",
    )

    st.plotly_chart(fig_heatmap, use_container_width=True, key=801)


if __name__ == "__main__":
    plot_8()