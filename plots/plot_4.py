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
    # -----------------------------------------------------------------------------------------------------------------------

    # Load datasets
    df_avg_weekly_hours = pd.read_csv("data/CES0500000002.csv")  # Average Weekly Hours
    df_hourly_earnings = pd.read_csv("data/CES0500000003.csv")  # Hourly Earnings

    df_avg_weekly_hours = prepare_df(df_avg_weekly_hours)
    df_hourly_earnings = prepare_df(df_hourly_earnings)

    # Find the common year range
    min_year = max(
        df_avg_weekly_hours["year"].min(),
        df_hourly_earnings["year"].min(),
    )
    max_year = min(
        df_avg_weekly_hours["year"].max(),
        df_hourly_earnings["year"].max(),
    )

    # Sidebar for year selection
    st.sidebar.header("Filter data for plot 4")
    selected_year = st.sidebar.slider(
        "Select Year",
        min_value=int(min_year),
        max_value=int(max_year),
        value=(int(min_year), int(max_year)),
        step=1,
        key=10,
    )

    filtered_df_avg_weekly_hours = filter_df(df_avg_weekly_hours, selected_year)
    filtered_df_hourly_earnings = filter_df(df_hourly_earnings, selected_year)

    # ----------------------------------- Clustered Bar Chart ------------------------------------
    st.title("Analyzing Work Hours and Earnings Across Sectors:")
    st.write(
        "This chart compares Average Weekly Hours and Hourly Earnings across different sectors. It highlights the variations in work hours and wages, revealing disparities between industries."
    )

    # Merging dataframes for bar chart
    merged_df_bar = pd.merge(
        filtered_df_avg_weekly_hours[["year_period", "value"]],
        filtered_df_hourly_earnings[["year_period", "value"]],
        on="year_period",
        suffixes=("_weekly_hours", "_hourly_earnings"),
    )
    merged_df_bar = merged_df_bar.rename(
        columns={
            "value_weekly_hours": "Average Weekly Hours",
            "value_hourly_earnings": "Hourly Earnings",
        }
    )

    # Create a clustered bar chart
    fig_bar = go.Figure()

    fig_bar.add_trace(
        go.Bar(
            x=merged_df_bar["year_period"],
            y=merged_df_bar["Average Weekly Hours"],
            name="Average Weekly Hours",
        )
    )
    fig_bar.add_trace(
        go.Bar(
            x=merged_df_bar["year_period"],
            y=merged_df_bar["Hourly Earnings"],
            name="Hourly Earnings",
        )
    )

    # Update layout
    fig_bar.update_layout(
        barmode="group",
        title="<b>Sectoral Trends in Employment and Earnings</b>",
        xaxis_title="Year Period",
        yaxis_title="Values",
        legend_title="Indicator",
    )
    fig_bar.update_xaxes(title_text="<b>Period</b>")
    fig_bar.update_yaxes(title_text="<b>Hours/Earnings</b>")
    st.plotly_chart(fig_bar, use_container_width=True)


if __name__ == "__main__":
    plot_4()
