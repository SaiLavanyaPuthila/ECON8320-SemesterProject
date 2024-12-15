# Load the datasets

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


def plot_2():
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

    st.sidebar.header("Filter data based on year for plot 2,3,4")
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
    st.title("Recession and Economic Slowdown")
    st.write(
        "Plot Unemployment Rate and Total Nonfarm Employment on a dual-axis line chart to identify correlations during economic downturns."
    )
    st.write("Shows how job losses impact unemployment rates during recessions.")

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
    )
    fig_dual.update_yaxes(
        title_text="<b>Total Nonfarm Employment</b>", secondary_y=False
    )
    fig_dual.update_yaxes(title_text="<b>Unemployment Rate</b>", secondary_y=True)

    st.plotly_chart(fig_dual, use_container_width=True, key=201)

    # ------------------------------------ Heatmap --------------------------------------
    st.header("Heatmap of Monthly Changes")
    st.write(
        "Create a heatmap showing monthly changes in Unemployment Rate and Total Nonfarm Employment across time."
    )
    st.write(
        "Visualizes which industries were hit hardest during recessions, identifying patterns of recovery or prolonged decline."
    )

    df_ces_change = calculate_monthly_change(filtered_df_ces)
    df_lns_unemp_change = calculate_monthly_change(filtered_df_lns_unemp)

    merged_df_heatmap = pd.merge(
        df_ces_change[["year", "month", "change"]],
        df_lns_unemp_change[["year", "month", "change"]],
        on=["year", "month"],
        suffixes=("_ces", "_unemp"),
    )

    merged_df_heatmap = merged_df_heatmap.rename(
        columns={
            "change_ces": "Nonfarm Emp Change",
            "change_unemp": "Unemp Rate Change",
        }
    )

    pivot_df = merged_df_heatmap.pivot_table(
        index="year",
        columns="month",
        values=["Nonfarm Emp Change", "Unemp Rate Change"],
    )

    # Create Heatmap using Plotly
    fig_heatmap = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=("Nonfarm Emp Change Heatmap", "Unemp Rate Change Heatmap"),
        vertical_spacing=0.15,
    )

    fig_heatmap.add_trace(
        go.Heatmap(
            z=pivot_df["Nonfarm Emp Change"].values,
            x=pivot_df["Nonfarm Emp Change"].columns.values,
            y=pivot_df["Nonfarm Emp Change"].index.values,
            colorscale="RdBu",
            showscale=True,
        ),
        row=1,
        col=1,
    )
    fig_heatmap.add_trace(
        go.Heatmap(
            z=pivot_df["Unemp Rate Change"].values,
            x=pivot_df["Unemp Rate Change"].columns.values,
            y=pivot_df["Unemp Rate Change"].index.values,
            colorscale="RdBu",
            showscale=True,
        ),
        row=2,
        col=1,
    )

    fig_heatmap.update_layout(height=700)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # ---------------------------------- Box Plot -------------------------------------
    st.header("Box Plot of Unemployment Rates")
    st.write(
        "Use a box plot to represent the distribution of unemployment rates before, during, and after recessions."
    )
    st.write(
        "Highlights variability in unemployment and how recessions exacerbate disparities in labor market conditions."
    )

    filtered_df_lns_unemp["recession_period"] = filtered_df_lns_unemp["year"].apply(
        categorize_period
    )

    # remove 'other' periods
    filtered_df_lns_unemp = filtered_df_lns_unemp[
        filtered_df_lns_unemp["recession_period"] != "Other"
    ]

    # Create Box Plot
    fig_box = go.Figure()

    for period in filtered_df_lns_unemp["recession_period"].unique():
        fig_box.add_trace(
            go.Box(
                y=filtered_df_lns_unemp[
                    filtered_df_lns_unemp["recession_period"] == period
                ]["value"],
                name=period,
            )
        )

    fig_box.update_layout(
        title="<b>Distribution of Unemployment Rates During Economic Cycles</b>",
        xaxis_title="Recession Period",
        yaxis_title="Unemployment Rate",
        showlegend=False,
    )

    st.plotly_chart(fig_box, use_container_width=True)


if __name__ == "__main__":
    plot_2()
