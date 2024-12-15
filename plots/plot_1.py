import streamlit as st
import pandas as pd


def prepare_df(df):
    df = df.sort_values(by=["year", "period"])
    df["year_period"] = df["year"].astype(str) + " " + df["periodName"]
    return df


# Filter data based on selected year range
def filter_df(df, selected_year):
    return df[(df["year"] >= selected_year[0]) & (df["year"] <= selected_year[1])]


def plot_1():
    # Load the datasets
    df_ces = pd.read_csv("data/CES0000000001.csv")
    df_lns = pd.read_csv("data/LNS12000000.csv")

    # Sort and prepare each dataframe

    df_ces = prepare_df(df_ces)
    df_lns = prepare_df(df_lns)

    # Find the common year range
    min_year = max(df_ces["year"].min(), df_lns["year"].min())
    max_year = min(df_ces["year"].max(), df_lns["year"].max())

    # Sidebar for year selection
    st.sidebar.header("Filter the expansion and growth by Year")
    selected_year = st.sidebar.slider(
        "Select Year",
        min_value=int(min_year),
        max_value=int(max_year),
        value=(int(min_year), int(max_year)),
        step=1,
        key=5,
    )

    filtered_df_ces = filter_df(df_ces, selected_year)
    filtered_df_lns = filter_df(df_lns, selected_year)

    # Line Chart
    st.title("Economic Expansion and Job Growth")
    st.write(
        "Compare trends in Civilian Employment (LNS12000000) and Total Nonfarm Employment (CES0000000001) to visualize job growth over time."
    )
    st.write("Highlights periods of rapid expansion or stagnation in job creation.")

    # Merge the two dataframes on year_period
    merged_df = pd.merge(
        filtered_df_ces[["year_period", "value"]],
        filtered_df_lns[["year_period", "value"]],
        on="year_period",
        suffixes=("_ces", "_lns"),
    )

    # Rename the columns to indicate source
    merged_df = merged_df.rename(
        columns={
            "value_ces": "Total Nonfarm Employment",
            "value_lns": "Civilian Employment",
        }
    )

    # Display a line chart with both employment series
    st.line_chart(
        data=merged_df,
        x="year_period",
        y=["Total Nonfarm Employment", "Civilian Employment"],
        use_container_width=True,
        height=500,
    )


if __name__ == "__main__":
    plot_1()