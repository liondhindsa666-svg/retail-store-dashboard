import pandas as pd
import plotly.express as px

def sales_over_time(df):
    temp = df.copy()
    temp["date"] = pd.to_datetime(temp["date"], errors="coerce")
    grouped = temp.groupby(temp["date"].dt.date, as_index=False)["totalprice"].sum()
    grouped.columns = ["date", "sales"]
    fig = px.line(grouped, x="date", y="sales", title="Sales Over Time")
    fig.update_layout(xaxis_title="Date", yaxis_title="Sales")
    return fig

def sales_by_product(df):
    grouped = df.groupby("product", as_index=False)["totalprice"].sum().sort_values("totalprice", ascending=False)
    grouped.columns = ["product", "sales"]
    fig = px.bar(grouped, x="product", y="sales", title="Sales by Product", color="product")
    fig.update_layout(xaxis_title="Product", yaxis_title="Sales")
    return fig

def sales_by_location(df):
    grouped = df.groupby("location", as_index=False)["totalprice"].sum().sort_values("totalprice", ascending=False)
    grouped.columns = ["location", "sales"]
    fig = px.bar(grouped, x="location", y="sales", title="Sales by Location", color="location")
    fig.update_layout(xaxis_title="Location", yaxis_title="Sales")
    return fig

def payment_distribution(df):
    grouped = df.groupby("paymenttype", as_index=False)["totalprice"].sum()
    grouped.columns = ["paymenttype", "sales"]
    fig = px.pie(grouped, names="paymenttype", values="sales", title="Payment Type Distribution")
    return fig

def quantity_by_day(df):
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    grouped = df.groupby("dayofweek", as_index=False)["quantity"].sum()
    grouped["dayofweek"] = pd.Categorical(grouped["dayofweek"], categories=order, ordered=True)
    grouped = grouped.sort_values("dayofweek")
    fig = px.bar(grouped, x="dayofweek", y="quantity", title="Quantity Sold by Day")
    fig.update_layout(xaxis_title="Day", yaxis_title="Quantity")
    return fig

def store_product_heatmap(df):
    pivot = df.pivot_table(index="location", columns="product", values="totalprice", aggfunc="sum", fill_value=0)
    fig = px.imshow(pivot, title="Store vs Product Heatmap", aspect="auto")
    return fig