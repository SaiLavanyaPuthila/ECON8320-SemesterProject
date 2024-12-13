import streamlit as st
import pandas as pd
import warnings
import numpy
import plotly
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from dataframes import *
import plotly.express as px


warnings.filterwarnings("ignore")

st.set_page_config(page_title="BSL Dashboard", layout="wide", page_icon=":bar_chart:")

st.title(":bar_chart: BSL Dashboard")
st.markdown(
    "<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True
)

# st.header("Header")
# st.subheader("Subheader")
# st.info("Info")
# st.warning("Warning")


# st.subheader("Economic Expansion and Job Growth")
# Load the data

# Load the datasets
df_ces = df_CES0000000001
df_lns = df_LNS12000000


# Sort and prepare each dataframe
def prepare_df(df):
    df = df.sort_values(by=["year", "period"])
    df["year_period"] = df["year"].astype(str) + " " + df["periodName"]
    return df


df_ces = prepare_df(df_ces)
df_lns = prepare_df(df_lns)

# Find the common year range
min_year = max(df_ces["year"].min(), df_lns["year"].min())
max_year = min(df_ces["year"].max(), df_lns["year"].max())


# Sidebar for year selection
st.sidebar.header("Filter Data")
selected_year = st.sidebar.slider(
    "Select Year",
    min_value=int(min_year),
    max_value=int(max_year),
    value=(int(min_year), int(max_year)),
    step=1,
    key=5,
)


# Filter data based on selected year range
def filter_df(df, selected_year):
    return df[(df["year"] >= selected_year[0]) & (df["year"] <= selected_year[1])]


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


# Load the datasets
df_ces = pd.read_csv("data/CES0000000001.csv")
df_lns_unemp = pd.read_csv("data/LNS14000000.csv")  # Unemployment Rate
df_lns_civ_emp = pd.read_csv("data/LNS12000000.csv")  # Civilian Employment


# Sort and prepare each dataframe
def prepare_df(df):
    df = df.sort_values(by=["year", "period"])
    df["year_period"] = df["year"].astype(str) + " " + df["periodName"]
    return df


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


st.sidebar.header("Filter Data")
selected_year = st.sidebar.slider(
    "Select Year",
    min_value=int(min_year),
    max_value=int(max_year),
    value=(int(min_year), int(max_year)),
    step=1,
    key=6,
)


# Filter data based on selected year range
def filter_df(df, selected_year):
    return df[(df["year"] >= selected_year[0]) & (df["year"] <= selected_year[1])]


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
fig_dual.update_yaxes(title_text="<b>Total Nonfarm Employment</b>", secondary_y=False)
fig_dual.update_yaxes(title_text="<b>Unemployment Rate</b>", secondary_y=True)

st.plotly_chart(fig_dual, use_container_width=True)

# ------------------------------------ Heatmap --------------------------------------
st.header("Heatmap of Monthly Changes")
st.write(
    "Create a heatmap showing monthly changes in Unemployment Rate and Total Nonfarm Employment across time."
)
st.write(
    "Visualizes which industries were hit hardest during recessions, identifying patterns of recovery or prolonged decline."
)


def calculate_monthly_change(df):
    df["value_previous"] = df["value"].shift(1)
    df["change"] = df["value"] - df["value_previous"]
    # Drop the first row for calculation purpose
    df = df.iloc[1:, :]

    # Extract the numeric part of 'period'
    df["month"] = df["period"].str[1:].astype(int)  # Slice from index 1 onwards.
    df["year"] = df["year"].astype(int)
    return df


df_ces_change = calculate_monthly_change(filtered_df_ces)
df_lns_unemp_change = calculate_monthly_change(filtered_df_lns_unemp)

merged_df_heatmap = pd.merge(
    df_ces_change[["year", "month", "change"]],
    df_lns_unemp_change[["year", "month", "change"]],
    on=["year", "month"],
    suffixes=("_ces", "_unemp"),
)

merged_df_heatmap = merged_df_heatmap.rename(
    columns={"change_ces": "Nonfarm Emp Change", "change_unemp": "Unemp Rate Change"}
)

pivot_df = merged_df_heatmap.pivot_table(
    index="year", columns="month", values=["Nonfarm Emp Change", "Unemp Rate Change"]
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


# Simulate recession periods
def categorize_period(year):
    if year < 2008:
        return "Pre-Recession"
    elif year >= 2008 and year <= 2009:
        return "During Recession"
    elif year >= 2010:
        return "Post-Recession"
    return "Other"


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


df_cpi = pd.read_csv("data/CUUR0000SA0.csv")  # CPI-U
df_earnings = pd.read_csv("data/CES0500000003.csv")  # Hourly earnings


# Sort and prepare each dataframe
def prepare_df(df):
    df = df.sort_values(by=["year", "period"])
    df["year_period"] = df["year"].astype(str) + " " + df["periodName"]
    return df


df_cpi = prepare_df(df_cpi)
df_earnings = prepare_df(df_earnings)

# Find the common year range
min_year = max(df_cpi["year"].min(), df_earnings["year"].min())
max_year = min(df_cpi["year"].max(), df_earnings["year"].max())

# Sidebar for year selection
st.sidebar.header("Filter Data")
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


df_unemployment = pd.read_csv("data/LNS14000000.csv")  # Unemployment Rate
df_eci = pd.read_csv("data/CIU2010000000000A.csv")  # Employment Cost Index

df_unemployment = prepare_df(df_unemployment)
df_eci = prepare_df(df_eci)

min_year_scatter = max(df_unemployment["year"].min(), df_eci["year"].min())
max_year_scatter = min(df_unemployment["year"].max(), df_eci["year"].max())

st.sidebar.header("Filter Data for Scatter Plot")
selected_year_scatter = st.sidebar.slider(
    "Select Year (Scatter Plot)",
    min_value=int(min_year_scatter),
    max_value=int(max_year_scatter),
    value=(int(min_year_scatter), int(max_year_scatter)),
    step=1,
    key=8,
)

st.title("Labor Market Tightness and Employment Costs")
st.write(
    "Plot Unemployment Rate against Employment Cost Index to illustrate the relationship between labor market tightness and rising employment costs."
)
st.write("Reveals the impact of a tight labor market on wage inflation.")


# Merging dataframes
merged_df_scatter = pd.merge(
    df_unemployment[["year", "value"]],
    df_eci[["year", "value"]],
    on="year",
    suffixes=("_unemployment", "_eci"),
)
merged_df_scatter = merged_df_scatter.rename(
    columns={
        "value_unemployment": "Unemployment Rate",
        "value_eci": "Employment Cost Index",
    }
)
# Scatter plot
fig_scatter = px.scatter(
    merged_df_scatter,
    x="Unemployment Rate",
    y="Employment Cost Index",
    color="year",  # Use 'year' for coloring
    title="<b>Unemployment Rate vs. Employment Cost Index</b>",
    labels={
        "Unemployment Rate": "Unemployment Rate",
        "Employment Cost Index": "Employment Cost Index",
        "year": "Year",
    },  # Label for the color legend
)

st.plotly_chart(fig_scatter, use_container_width=True)



# Load datasets
df_productivity = pd.read_csv("data/PRS85006092.csv")  # Output Per Hour
df_real_compensation = pd.read_csv("data/PRS85006152.csv")  # Real Hourly Compensation


# Sort and prepare each dataframe
def prepare_df(df):
    df = df.sort_values(by=["year", "period"])
    df["year_period"] = df["year"].astype(str) + " " + df["periodName"]
    return df


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


# Filter data based on selected year range
def filter_df(df, selected_year):
    return df[(df["year"] >= selected_year[0]) & (df["year"] <= selected_year[1])]


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


#-----------------------------------------------------------------------------------------------------------------------

# Load datasets
df_avg_weekly_hours = pd.read_csv("data/CES0500000002.csv")  # Average Weekly Hours
df_hourly_earnings = pd.read_csv("data/CES0500000003.csv")  # Hourly Earnings

# Sort and prepare each dataframe
def prepare_df(df):
    df = df.sort_values(by=["year", "period"])
    df["year_period"] = df["year"].astype(str) + " " + df["periodName"]
    return df

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
st.sidebar.header("Filter Data")
selected_year = st.sidebar.slider(
    "Select Year",
    min_value=int(min_year),
    max_value=int(max_year),
    value=(int(min_year), int(max_year)),
    step=1,
    key=10,
)

# Filter data based on selected year range
def filter_df(df, selected_year):
    return df[(df["year"] >= selected_year[0]) & (df["year"] <= selected_year[1])]

filtered_df_avg_weekly_hours = filter_df(df_avg_weekly_hours, selected_year)
filtered_df_hourly_earnings = filter_df(df_hourly_earnings, selected_year)

# ----------------------------------- Clustered Bar Chart ------------------------------------
st.title("Sectoral Trends in Employment and Earnings")
st.write(
    "Compare Average Weekly Hours and Hourly Earnings across sectors to visualize sector-specific trends.")
st.write(
    "Highlights disparities in work hours and wages between industries.")

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
)

st.plotly_chart(fig_bar, use_container_width=True)


#-----------------------------------------------------------------------------------------------------------

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Load datasets
df_cpi = pd.read_csv("data/CUUR0000SA0.csv")  # CPI-U Components
df_real_compensation = pd.read_csv("data/PRS85006152.csv")  # Real Hourly Compensation


# Function to convert monthly to quarterly data
def monthly_to_quarterly(df):
    df['period'] = df['period'].str[1:].astype(int)
    df['quarter'] = (df['period'] - 1) // 3 + 1
    df['periodName'] = "Q" + df['quarter'].astype(str) + " Quarter"
    df['year_period'] = df['year'].astype(str) + " " + df["periodName"]
    df_quarterly = df.groupby(['year', 'quarter', 'periodName', 'year_period'], as_index=False)['value'].mean()
    return df_quarterly

# Sort and prepare each dataframe
def prepare_df(df, cpi=False):
    if cpi:
        df = monthly_to_quarterly(df)
        df = df.sort_values(by=["year", "quarter"])
    else:
        df = df.sort_values(by=["year", "period"])
        df["year_period"] = df["year"].astype(str) + " " + df["periodName"]
    return df


df_cpi = prepare_df(df_cpi, cpi=True)
df_real_compensation = prepare_df(df_real_compensation)

# Find the common year range
min_year = max(
    df_cpi["year"].min(),
    df_real_compensation["year"].min(),
)
max_year = min(
    df_cpi["year"].max(),
    df_real_compensation["year"].max(),
)

# Sidebar for year selection
st.sidebar.header("Filter Data")
selected_year = st.sidebar.slider(
    "Select Year",
    min_value=int(min_year),
    max_value=int(max_year),
    value=(int(min_year), int(max_year)),
    step=1,
    key=13,
)

# Filter data based on selected year range
def filter_df(df, selected_year):
    return df[(df["year"] >= selected_year[0]) & (df["year"] <= selected_year[1])]

filtered_df_cpi = filter_df(df_cpi, selected_year)
filtered_df_real_compensation = filter_df(df_real_compensation, selected_year)

# ----------------------------------- Stacked Area Chart ------------------------------------
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Load datasets
df_imports = pd.read_csv("data/EIUIR.csv")  # Import Volumes
df_exports = pd.read_csv("data/EIUIQ.csv")  # Export Volumes

# Sort and prepare each dataframe
def prepare_df(df):
    df = df.sort_values(by=["year", "period"])
    df["year_period"] = df["year"].astype(str) + " " + df["periodName"]
    return df

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

# Filter data based on selected year range
def filter_df(df, selected_year):
    return df[(df["year"] >= selected_year[0]) & (df["year"] <= selected_year[1])]

filtered_df_imports = filter_df(df_imports, selected_year)
filtered_df_exports = filter_df(df_exports, selected_year)

# ----------------------------------- Line Chart ------------------------------------
st.title("Trade and International Economics")
st.write("Compare Import and Export volumes over time to highlight changes in trade balances.")
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

#-----------------------------------------------------------------------------------------------------------------------------------------

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Load dataset
df_labor_force = pd.read_csv("data/LNS11000000.csv")

# Sort and prepare the dataframe
def prepare_df(df):
    df = df.sort_values(by=["year", "period"])
    df["year_period"] = df["year"].astype(str) + " " + df["periodName"]
    df = df.rename(columns={'15':'value'})
    return df

df_labor_force = prepare_df(df_labor_force)

# Find the common year range
min_year = df_labor_force["year"].min()
max_year = df_labor_force["year"].max()


# Sidebar for year selection
st.sidebar.header("Filter Data")
selected_year = st.sidebar.slider(
    "Select Year",
    min_value=int(min_year),
    max_value=int(max_year),
    value=int(min_year),
    step=1,
    key=11,
)

# Filter data based on selected year
def filter_df(df, selected_year):
    return df[df["year"] == selected_year]

filtered_df_labor_force = filter_df(df_labor_force, selected_year)

# ----------------------------------- Pie Chart ------------------------------------
st.title("Workforce Demographics and Labor Force Trends")
st.write("Show the distribution of the Civilian Labor Force across demographic segments.")
st.write("Highlights shifts in workforce composition over time.")

# For now, assuming a simple pie chart based on value,
# but you may need to further process your dataset if it includes demographic breakdowns

# Pie chart
fig_pie = go.Figure(data=[go.Pie(labels=filtered_df_labor_force['year_period'], values=filtered_df_labor_force['value'])])

# Update layout
fig_pie.update_layout(
    title=f"<b>Civilian Labor Force Distribution in {selected_year}</b>",
)

st.plotly_chart(fig_pie, use_container_width=True)


#-------------------------------------------------------------------------------------------------------------

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load datasets
df_cpi = pd.read_csv("data/CUUR0000SA0.csv")  # CPI-U
df_earnings = pd.read_csv("data/CES0500000003.csv")  # Average Hourly Earnings


# Sort and prepare each dataframe
def prepare_df(df):
    df = df.sort_values(by=["year", "period"])
    df["year_period"] = df["year"].astype(str) + " " + df["periodName"]
    df= df.rename(columns={'value':'value'})
    return df


df_cpi = prepare_df(df_cpi)
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
st.sidebar.header("Filter Data")
selected_year = st.sidebar.slider(
    "Select Year",
    min_value=int(min_year),
    max_value=int(max_year),
    value=(int(min_year), int(max_year)),
    step=1,
    key=12,
)

# Filter data based on selected year range
def filter_df(df, selected_year):
    return df[(df["year"] >= selected_year[0]) & (df["year"] <= selected_year[1])]


filtered_df_cpi = filter_df(df_cpi, selected_year)
filtered_df_earnings = filter_df(df_earnings, selected_year)


# ----------------------------------- Dual-Axis Line Chart ------------------------------------
st.title("Cost of Living and Consumer Economics")
st.write("Track CPI-U and Average Hourly Earnings over time to measure whether wages are keeping pace with the cost of living.")
st.write("Assesses the economic burden on consumers.")

# Merging dataframes for dual-axis line chart
merged_df_dual = pd.merge(
    filtered_df_cpi[["year_period", "value"]],
    filtered_df_earnings[["year_period", "value"]],
    on="year_period",
    suffixes=("_cpi", "_earnings"),
)
merged_df_dual = merged_df_dual.rename(
    columns={
        "value_cpi": "CPI-U",
        "value_earnings": "Average Hourly Earnings",
    }
)


# Create dual-axis line chart
fig_dual = make_subplots(specs=[[{"secondary_y": True}]])

fig_dual.add_trace(
    go.Scatter(
        x=merged_df_dual["year_period"],
        y=merged_df_dual["CPI-U"],
        name="CPI-U",
        mode="lines",
    ),
    secondary_y=False,
)

fig_dual.add_trace(
    go.Scatter(
        x=merged_df_dual["year_period"],
        y=merged_df_dual["Average Hourly Earnings"],
        name="Average Hourly Earnings",
        mode="lines",
    ),
    secondary_y=True,
)

# Update layout
fig_dual.update_layout(
    title="<b>CPI-U vs. Average Hourly Earnings</b>",
    xaxis_title="Year Period",
)

fig_dual.update_yaxes(title_text="<b>CPI-U</b>", secondary_y=False)
fig_dual.update_yaxes(title_text="<b>Average Hourly Earnings</b>", secondary_y=True)

st.plotly_chart(fig_dual, use_container_width=True)

#----------------------------------------------------------------------------------------------------------------

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load datasets
df_cpi = pd.read_csv("data/CUUR0000SA0.csv")  # CPI-U
df_earnings = pd.read_csv("data/CES0500000003.csv")  # Average Hourly Earnings

# Sort and prepare each dataframe
def prepare_df(df,cpi=False):
    if cpi:
        df = df.sort_values(by=["year", "period"])
        df["year_period"] = df["year"].astype(str) + " " + df["periodName"]
        df= df.rename(columns={'value':'cpi_value'})
    else:
        df = df.sort_values(by=["year", "period"])
        df["year_period"] = df["year"].astype(str) + " " + df["periodName"]
        df = df.rename(columns={'value':'earnings_value'})
    return df


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
st.sidebar.header("Filter Data")
selected_year = st.sidebar.slider(
    "Select Year",
    min_value=int(min_year),
    max_value=int(max_year),
    value=(int(min_year), int(max_year)),
    step=1,
    key=16,
)

# Filter data based on selected year range
def filter_df(df, selected_year):
    return df[(df["year"] >= selected_year[0]) & (df["year"] <= selected_year[1])]


filtered_df_cpi = filter_df(df_cpi, selected_year)
filtered_df_earnings = filter_df(df_earnings, selected_year)

# ----------------------------------- Stacked Bar Chart ------------------------------------
st.title("Cost of Living and Consumer Economics")
st.write(
    "Break down the CPI-U into its major components over time. Add a secondary dataset for Hourly Earnings as a reference line."
)
st.write(
    "Shows how different aspects of cost of living evolve and whether wage growth matches these changes."
)

# Assuming a generic CPI breakdown. You might need to adjust this based on the structure of your CPI data.
cpi_components = ["cpi_value"]  # Replace this if you have CPI component columns

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
        secondary_y=False
    )


fig_bar.add_trace(
    go.Scatter(
        x=merged_df_bar["year_period"],
        y=merged_df_bar["Average Hourly Earnings"],
        name="Average Hourly Earnings",
        mode="lines",
        line=dict(color='black', width=2, dash='dash')
    ),
    secondary_y=True
)


# Update layout
fig_bar.update_layout(
    title="<b>CPI-U Components and Average Hourly Earnings</b>",
    xaxis_title="Year Period",
)
fig_bar.update_yaxes(title_text="<b>CPI-U Components</b>", secondary_y=False)
fig_bar.update_yaxes(title_text="<b>Average Hourly Earnings</b>", secondary_y=True)

st.plotly_chart(fig_bar, use_container_width=True)


#------------------------------------------------------------------------------------------------------------------------------------------------------

