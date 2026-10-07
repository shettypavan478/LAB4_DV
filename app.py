import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="County Development Dashboard", layout="wide")

@st.cache_data
def load_data():
    return px.data.gapminder()

df = load_data()

st.title("County Development Dashboard")

st.sidebar.header("Filters")
years = sorted(df["year"].unique())
selected_year = st.sidebar.slider(
    "Year", int(min(years)), int(max(years)), int(max(years)), 5
)
continents = sorted(df["continent"].unique())
selected_continents = st.sidebar.multiselect(
    "Continent", continents, default=continents
)

filtered = df[
    (df["year"] == selected_year)
    & (df["continent"].isin(selected_continents))
].copy()

st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Countries", int(filtered["country"].nunique()))
col2.metric(
    "Median life expectancy",
    f'{filtered["lifeExp"].median():.1f} yrs' if not filtered.empty else "0.0 yrs",
)
col3.metric(
    "Total population",
    f'{filtered["pop"].sum() / 1_000_000:.2f} B' if not filtered.empty else "0.00 B",
)

st.subheader("GDP per Capita vs Life Expectancy")
if filtered.empty:
    st.warning("No records match the selected filters.")
else:
    fig = px.scatter(
        filtered,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=55,
        title=f"Development Overview — {selected_year}",
        labels={
            "gdpPercap": "GDP per capita",
            "lifeExp": "Life expectancy",
            "pop": "Population",
        },
    )
    fig.update_layout(height=620)
    st.plotly_chart(fig, use_container_width=True)

st.caption("LAB 4 — Git Basics for a Python Project")
