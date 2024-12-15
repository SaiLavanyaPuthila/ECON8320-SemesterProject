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


def plot_7():

    # Load datasets
    df_imports = pd.read_csv("data/EIUIR.csv")  # Import Volumes
    df_exports = pd.read_csv("data/EIUIQ.csv")  # Export Volumes

    df_imports = prepare_df(df_imports)
    df_exports = prepare_df(df_exports)

    # Find the common year range
    min_year = max(
        df_imports["year"].min(),
        df_exports["year"].min(),
    )
    max_year = min(
        df_imports["year"].max(),
        df_exports["year"].max(),
    )

    # Sidebar for year selection
    st.sidebar.header("Filter Data")
    selected_year = st.sidebar.slider(
        "Select Year",
        min_value=int(min_year),
        max_value=int(max_year),
        value=(int(min_year), int(max_year)),
        step=1,
        key=14,
    )

    filtered_df_imports = filter_df(df_imports, selected_year)
    filtered_df_exports = filter_df(df_exports, selected_year)

    # ----------------------------------- Line Chart ------------------------------------
    st.title("Trade and International Economics")
    st.write(
        "Compare Import and Export volumes over time to highlight changes in trade balances."
    )
    st.write("Identifies periods of trade surplus or deficit and their trends.")

    # Merging dataframes for line chart
    merged_df_line = pd.merge(
        filtered_df_imports[["year_period", "value"]],
        filtered_df_exports[["year_period", "value"]],
        on="year_period",
        suffixes=("_imports", "_exports"),
    )
    merged_df_line = merged_df_line.rename(
        columns={
            "value_imports": "Import Volumes",
            "value_exports": "Export Volumes",
        }
    )

    # Create a line chart
    fig_line = go.Figure()

    fig_line.add_trace(
        go.Scatter(
            x=merged_df_line["year_period"],
            y=merged_df_line["Import Volumes"],
            name="Import Volumes",
            mode="lines",
        )
    )
    fig_line.add_trace(
        go.Scatter(
            x=merged_df_line["year_period"],
            y=merged_df_line["Export Volumes"],
            name="Export Volumes",
            mode="lines",
        )
    )

    # Update layout
    fig_line.update_layout(
        title="<b>Import and Export Volumes Over Time</b>",
        xaxis_title="Year Period",
        yaxis_title="Volume",
    )

    st.plotly_chart(fig_line, use_container_width=True)


if __name__ == "__main__":
    plot_7()
