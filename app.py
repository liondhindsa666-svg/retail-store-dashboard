import streamlit as st
import pandas as pd
from pathlib import Path
from data_cleaning import clean_data
import visualizations as viz

st.set_page_config(page_title="Retail Store Dashboard", layout="wide")

DATA_PATH = "data/cleaned_transactions.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

if not Path(DATA_PATH).exists():
    clean_data()

df = load_data()
df["date"] = pd.to_datetime(df["date"], errors="coerce")

st.title("Retail Store Transactions Dashboard")

st.sidebar.header("Filters")

min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input("Select Date Range", value=(min_date, max_date))

locations = sorted(df["location"].dropna().unique())
products = sorted(df["product"].dropna().unique())
payments = sorted(df["paymenttype"].dropna().unique())
cashiers = sorted(df["cashier"].dropna().unique())
managers = sorted(df["storemanager"].dropna().unique())

selected_locations = st.sidebar.multiselect("Location", locations)
selected_products = st.sidebar.multiselect("Product", products)
selected_payments = st.sidebar.multiselect("Payment Type", payments)
selected_cashiers = st.sidebar.multiselect("Cashier", cashiers)
selected_managers = st.sidebar.multiselect("Store Manager", managers)

filtered_df = df.copy()

if len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
    filtered_df = filtered_df[(filtered_df["date"] >= start_date) & (filtered_df["date"] <= end_date)]

if selected_locations:
    filtered_df = filtered_df[filtered_df["location"].isin(selected_locations)]

if selected_products:
    filtered_df = filtered_df[filtered_df["product"].isin(selected_products)]

if selected_payments:
    filtered_df = filtered_df[filtered_df["paymenttype"].isin(selected_payments)]

if selected_cashiers:
    filtered_df = filtered_df[filtered_df["cashier"].isin(selected_cashiers)]

if selected_managers:
    filtered_df = filtered_df[filtered_df["storemanager"].isin(selected_managers)]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Transactions", len(filtered_df))
c2.metric("Total Sales", f"{filtered_df['totalprice'].sum():,.2f}")
c3.metric("Avg Order Value", f"{filtered_df['totalprice'].mean():,.2f}")
c4.metric("Total Quantity", f"{filtered_df['quantity'].sum():,.0f}")

st.divider()

r1, r2 = st.columns(2)
with r1:
    st.plotly_chart(viz.sales_over_time(filtered_df), use_container_width=True)
with r2:
    st.plotly_chart(viz.sales_by_product(filtered_df), use_container_width=True)

r3, r4 = st.columns(2)
with r3:
    st.plotly_chart(viz.sales_by_location(filtered_df), use_container_width=True)
with r4:
    st.plotly_chart(viz.payment_distribution(filtered_df), use_container_width=True)

r5, r6 = st.columns(2)
with r5:
    st.plotly_chart(viz.quantity_by_day(filtered_df), use_container_width=True)
with r6:
    st.plotly_chart(viz.store_product_heatmap(filtered_df), use_container_width=True)

st.subheader("Filtered Data")
st.dataframe(filtered_df, use_container_width=True)

csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_transactions.csv",
    mime="text/csv"
)