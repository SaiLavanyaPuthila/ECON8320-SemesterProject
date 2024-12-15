import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Sort and prepare each dataframe
def prepare_df(df):
    df = df.sort_values(by=["year", "period"])
    df["year_period"] = df["year"].astype(str) + " " + df["periodName"]
    return df


def plot_3():
    df_cpi = pd.read_csv("data/CUUR0000SA0.csv")  # CPI-U
    df_earnings = pd.read_csv("data/CES0500000003.csv")  # Hourly earnings

    df_cpi = prepare_df(df_cpi)
    df_earnings = prepare_df(df_earnings)

    # Find the common year range
    min_year = max(df_cpi["year"].min(), df_earnings["year"].min())
    max_year = min(df_cpi["year"].max(), df_earnings["year"].max())

    # Sidebar for year selection
    st.sidebar.header("Filter data for the inflation pressure and wage growth")
    selected_year = st.sidebar.slider(
        "Select Year",
        min_value=int(min_year),
        max_value=int(max_year),
        value=(int(min_year), int(max_year)),
        step=1,
        key=7,
    )

    # Filter data based on selected year range
    def filter_df(df, selected_year):
        return df[(df["year"] >= selected_year[0]) & (df["year"] <= selected_year[1])]

    filtered_df_cpi = filter_df(df_cpi, selected_year)
    filtered_df_earnings = filter_df(df_earnings, selected_year)

    # ----------------------------------- Bar Chart ------------------------------------
    st.title("Inflationary Pressure and Wage Growth")
    st.write(
        "Display year-over-year changes in CPI-U and Hourly Earnings to assess the alignment between inflation and wages."
    )
    st.write("Demonstrates whether wages are keeping up with inflationary pressures.")

    def calculate_year_over_year_change(df):
        # Calculate the previous year values
        df["value_previous"] = df.groupby("period")["value"].shift(1)

        # Calculate the YoY difference
        df["yoy_change"] = df["value"] - df["value_previous"]
        # Drop null entries
        df = df.dropna(subset=["yoy_change"])
        return df

    df_cpi_change = calculate_year_over_year_change(filtered_df_cpi)
    df_earnings_change = calculate_year_over_year_change(filtered_df_earnings)

    # Merging dataframes to display on a common bar plot
    merged_df_bar = pd.merge(
        df_cpi_change[["year", "yoy_change"]],
        df_earnings_change[["year", "yoy_change"]],
        on="year",
        suffixes=("_cpi", "_earnings"),
    )
    merged_df_bar = merged_df_bar.rename(
        columns={
            "yoy_change_cpi": "CPI-U Change",
            "yoy_change_earnings": "Hourly Earnings Change",
        }
    )

    # Create a bar plot using plotly
    fig_bar = go.Figure(
        data=[
            go.Bar(
                name="CPI-U Change",
                x=merged_df_bar["year"],
                y=merged_df_bar["CPI-U Change"],
            ),
            go.Bar(
                name="Hourly Earnings Change",
                x=merged_df_bar["year"],
                y=merged_df_bar["Hourly Earnings Change"],
            ),
        ]
    )

    # Layout title
    fig_bar.update_layout(
        title="<b>Year-over-Year Change in CPI-U and Hourly Earnings</b>",
        xaxis_title="Year",
        yaxis_title="Year-over-Year Change",
    )

    st.plotly_chart(fig_bar, use_container_width=True)


if __name__ == "__main__":
    plot_3()
