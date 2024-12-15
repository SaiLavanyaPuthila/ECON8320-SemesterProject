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

    # Load datasets
    df_productivity = pd.read_csv("data/PRS85006092.csv")  # Output Per Hour
    df_real_compensation = pd.read_csv("data/PRS85006152.csv")  # Real Hourly Compensation





    df_productivity = prepare_df(df_productivity)
    df_real_compensation = prepare_df(df_real_compensation)

    # Find the common year range
    min_year = max(df_productivity["year"].min(), df_real_compensation["year"].min())
    max_year = min(df_productivity["year"].max(), df_real_compensation["year"].max())

    # Sidebar for year selection
    st.sidebar.header("Filter Data")
    selected_year = st.sidebar.slider(
        "Select Year",
        min_value=int(min_year),
        max_value=int(max_year),
        value=(int(min_year), int(max_year)),
        step=1,
        key=9,
    )




    filtered_df_productivity = filter_df(df_productivity, selected_year)
    filtered_df_real_compensation = filter_df(df_real_compensation, selected_year)

    # ----------------------------------- Dual Axis Line Chart ------------------------------------
    st.title("Productivity and Real Compensation")
    st.write(
        "Track Output Per Hour and Real Hourly Compensation on a dual-axis to explore productivity trends against real wages."
    )
    st.write(
        "Shows whether productivity gains translate into better real compensation for workers."
    )


    # Merging dataframes
    merged_df_line = pd.merge(
        filtered_df_productivity[["year_period", "value"]],
        filtered_df_real_compensation[["year_period", "value"]],
        on="year_period",
        suffixes=("_productivity", "_real_compensation"),
    )
    merged_df_line = merged_df_line.rename(
        columns={
            "value_productivity": "Output Per Hour",
            "value_real_compensation": "Real Hourly Compensation",
        }
    )


    # Create a dual-axis line chart
    fig_line = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig_line.add_trace(
        go.Scatter(
            x=merged_df_line["year_period"],
            y=merged_df_line["Output Per Hour"],
            name="Output Per Hour",
        ),
        secondary_y=False,
    )
    fig_line.add_trace(
        go.Scatter(
            x=merged_df_line["year_period"],
            y=merged_df_line["Real Hourly Compensation"],
            name="Real Hourly Compensation",
        ),
        secondary_y=True,
    )

    # Set x axis title
    fig_line.update_xaxes(title_text="Year Period")
    # Set y-axes titles
    fig_line.update_yaxes(title_text="<b>Output Per Hour</b>", secondary_y=False)
    fig_line.update_yaxes(title_text="<b>Real Hourly Compensation</b>", secondary_y=True)
    # Layout title
    fig_line.update_layout(title="<b>Productivity and Real Compensation Over Time</b>")

    st.plotly_chart(fig_line, use_container_width=True)

if __name__ == "__main__":
    plot_5()