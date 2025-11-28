import sys
import os

# Get project root: global-econ-dashboard/
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

print("PYTHONPATH ->", sys.path[0])  # debug

from src.db.query import load_all_data, load_countries, load_years

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Global Economic Dashboard", layout="wide")

st.title("🌍 Global Economic Dashboard")
st.markdown("Live data from PostgreSQL • Inflation • Wages • Commodities")

# Load data
df = load_all_data()
# FIX: Convert date column to datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Sidebar filters
st.sidebar.header("🔎 Filters")
countries = load_countries()
years = load_years()

# 🔥 FIX: Convert years to integers + sort
years = sorted([int(y) for y in years])

selected_country = st.sidebar.selectbox("Select Country", ["ALL"] + countries)

# 🔥 FIX: Make sure slider gets int values
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=min(years),
    max_value=max(years),
    value=(min(years), max(years)),
    step=1
)

df_filtered = df[
    (df["date"].dt.year >= year_range[0]) &
    (df["date"].dt.year <= year_range[1])
]

if selected_country != "ALL":
    df_filtered = df_filtered[df_filtered["iso3"] == selected_country]

# ======= 1️⃣ Inflation Trend =======
st.subheader("📈 Inflation Over Time")

fig_inf = px.line(df_filtered, x="date", y="inflation_rate", color="iso3",
                  title="Inflation Trend")
st.plotly_chart(fig_inf, use_container_width=True)

# ======= 2️⃣ Wage Trend =======
st.subheader("💼 Wage Index Over Time")
fig_wage = px.line(df_filtered, x="date", y="wage_index", color="iso3",
                   title="Wage Index Trend")
st.plotly_chart(fig_wage, use_container_width=True)

# ======= 3️⃣ Inflation vs Wages =======
st.subheader("📉 Inflation vs Wage Index")
fig_scatter = px.scatter(df_filtered, x="inflation_rate", y="wage_index",
                         color="iso3", title="Inflation vs Wages")
st.plotly_chart(fig_scatter, use_container_width=True)

# ======= 4️⃣ Commodity Prices =======
st.subheader("🛢️ Commodity Price Trend")
fig_com = px.line(df_filtered, x="date", y="commodity_price",
                  title="Commodity Price Trend")
st.plotly_chart(fig_com, use_container_width=True)

st.success("✨ Dashboard Loaded Successfully")
