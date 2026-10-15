"""Interactive retail sales dashboard."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "processed" / "retail_sales.db"

st.set_page_config(page_title="Retail Sales Analytics", page_icon="📊", layout="wide")
st.title("Retail Sales Analytics")
st.caption(
    "UCI Online Retail · net revenue includes retained returns and cancellations; "
    "profit is not available in the source data."
)

if not DB_PATH.exists():
    st.error("Processed database not found. Run `python src/prepare_data.py` first.")
    st.stop()

with sqlite3.connect(DB_PATH) as connection:
    choices = pd.read_sql_query(
        "SELECT DISTINCT country FROM retail_sales ORDER BY country", connection
    )["country"].tolist()
    months = pd.read_sql_query(
        "SELECT DISTINCT invoice_month FROM retail_sales ORDER BY invoice_month", connection
    )["invoice_month"].tolist()

left, right = st.columns(2)
with left:
    selected_countries = st.multiselect(
        "Countries",
        choices,
        default=["United Kingdom"] if "United Kingdom" in choices else [],
        help="Leave blank to include every country.",
    )
with right:
    selected_months = st.multiselect(
        "Invoice months", months, default=months, help="Leave blank to include every month."
    )

conditions: list[str] = []
parameters: list[str] = []
if selected_countries:
    conditions.append(f"country IN ({','.join('?' for _ in selected_countries)})")
    parameters.extend(selected_countries)
if selected_months:
    conditions.append(f"invoice_month IN ({','.join('?' for _ in selected_months)})")
    parameters.extend(selected_months)
where = f"WHERE {' AND '.join(conditions)}" if conditions else ""

with sqlite3.connect(DB_PATH) as connection:
    data = pd.read_sql_query(
        f"SELECT * FROM retail_sales {where}", connection, params=parameters,
        parse_dates=["invoice_date"],
    )

if data.empty:
    st.warning("No transactions match the selected filters.")
    st.stop()

completed_invoices = data.loc[
    ~data["is_cancellation"].astype(bool) & (data["quantity"] > 0), "invoice_no"
].unique()
orders = len(completed_invoices)
net_revenue = data["revenue"].sum()
completed_order_revenue = data.loc[
    ~data["is_cancellation"].astype(bool) & data["invoice_no"].isin(completed_invoices),
    "revenue",
].sum()
average_order_value = completed_order_revenue / orders if orders else 0
return_rows = int(data["is_return"].astype(bool).sum())

kpis = st.columns(4)
kpis[0].metric("Net revenue", f"£{net_revenue:,.2f}")
kpis[1].metric("Completed orders", f"{orders:,}")
kpis[2].metric("Average order value", f"£{average_order_value:,.2f}")
kpis[3].metric("Return rows", f"{return_rows:,}")

monthly = (
    data.groupby("invoice_month", as_index=False)["revenue"]
    .sum()
    .sort_values("invoice_month")
)
country = (
    data.groupby("country", as_index=False)["revenue"]
    .sum()
    .sort_values("revenue", ascending=False)
    .head(15)
)
product = (
    data.groupby(["stock_code", "description"], as_index=False)["revenue"]
    .sum()
    .sort_values("revenue", ascending=False)
    .head(15)
)

chart_left, chart_right = st.columns(2)
with chart_left:
    st.subheader("Monthly net revenue")
    st.plotly_chart(
        px.line(monthly, x="invoice_month", y="revenue", markers=True,
                labels={"invoice_month": "Month", "revenue": "Net revenue (£)"}),
        use_container_width=True,
    )
with chart_right:
    st.subheader("Net revenue by country")
    st.plotly_chart(
        px.bar(country.sort_values("revenue"), x="revenue", y="country", orientation="h",
               labels={"country": "Country", "revenue": "Net revenue (£)"}),
        use_container_width=True,
    )

st.subheader("Top products by net revenue")
st.plotly_chart(
    px.bar(product.sort_values("revenue"), x="revenue", y="description", orientation="h",
           hover_data=["stock_code"],
           labels={"description": "Product", "revenue": "Net revenue (£)"}),
    use_container_width=True,
)

with st.expander("View filtered transactions"):
    st.dataframe(data, use_container_width=True, hide_index=True)
