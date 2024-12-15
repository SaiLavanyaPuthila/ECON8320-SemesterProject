import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# from utils import prepare_df, filter_df
import plotly.express as px


# Sort and prepare the dataframe
def prepare_df(df):
    df = df.sort_values(by=["year", "period"])
    df["year_period"] = df["year"].astype(str) + " " + df["periodName"]
    df = df.rename(columns={"value": "labor_force"})
    return df


# Filter data based on selected year
def filter_df(df, selected_year):
    return df[df["year"] == selected_year]


def plot_8():

    # Load the dataset
    df_labor_force = pd.read_csv("data/LNS11000000.csv")

    df_labor_force = prepare_df(df_labor_force)

    # Find the common year range
    min_year = df_labor_force["year"].min()
    max_year = df_labor_force["year"].max()

    # Sidebar for year selection
    st.sidebar.header("Filter Data for pie chart")
    selected_year = st.sidebar.slider(
        "Select Year",
        min_value=int(min_year),
        max_value=int(max_year),
        value=int(min_year),
        step=1,
        key=800,
    )

    filtered_df_labor_force = filter_df(df_labor_force, selected_year)

    # ----------------------------------- Pie Chart ------------------------------------
    st.title("Workforce Demographics and Labor Force Trends!!!!!!!")
    st.write(
        "Show the distribution of the Civilian Labor Force across demographic segments."
    )
    st.write("Highlights shifts in workforce composition over time.")

    # Pie chart
    if not filtered_df_labor_force.empty:
        fig_pie = go.Figure(
            data=[
                go.Pie(
                    labels=filtered_df_labor_force["year_period"],
                    values=filtered_df_labor_force["labor_force"],
                    hoverinfo="label+percent+value",
                    textinfo="percent",
                )
            ]
        )

        # Update layout
        fig_pie.update_layout(
            title=f"<b>Civilian Labor Force Distribution in {selected_year}</b>",
            annotations=[
                {
                    "text": f"Total Labor Force: {filtered_df_labor_force['labor_force'].sum()}",
                    "x": 0.5,
                    "y": -0.1,
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 12},
                }
            ],
        )

        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.write(f"No data available for the selected year: {selected_year}")


if __name__ == "__main__":
    plot_8()