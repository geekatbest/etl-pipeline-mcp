import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="E-Commerce Analytics Dashboard", layout="wide")
st.title("🧮 E-Commerce Analytics Dashboard")

st.sidebar.header("Settings")
db_path = st.sidebar.text_input("SQLite DB Path", value="D:/ml_projects/quantifai-assignment/v1_ecommerce.db")

if "theme" not in st.session_state:
    st.session_state.theme = "light"
if st.sidebar.button("Toggle Theme"):
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
st.write(f"Current Theme: {st.session_state.theme.title()}")

@st.cache_data(show_spinner=False)
def load_data():
    conn = sqlite3.connect(db_path)
    orders = pd.read_sql("SELECT * FROM orders", conn)
    customers = pd.read_sql("SELECT * FROM customers", conn)
    products = pd.read_sql("SELECT * FROM products", conn)
    conn.close()
    return orders, customers, products

try:
    orders, customers, products = load_data()
except Exception as e:
    st.error(f"Failed to load database: {e}")
    st.stop()

# Convert order_datetime to proper datetime format
orders['order_datetime'] = pd.to_datetime(orders['order_datetime'], errors='coerce')

tabs = st.tabs(["Overview", "Orders Analytics", "Customer Insights", "Product Performance", "Data Quality"])


# 1. Overview Tab
with tabs[0]:
    st.subheader("📊 Business Overview")
    total_revenue = orders["order_total"].sum()
    total_orders = len(orders)
    total_customers = orders["cust_id"].nunique()
    avg_order_value = total_revenue / total_orders if total_orders else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"₹{total_revenue:,.2f}")
    col2.metric("Total Orders", total_orders)
    col3.metric("Total Customers", total_customers)
    col4.metric("Avg Order Value", f"₹{avg_order_value:,.2f}")

    st.markdown("---")

    st.write("📈 Revenue Over Time")
    orders['order_date'] = pd.to_datetime(orders['order_datetime']).dt.date
    rev_over_time = orders.groupby('order_date')['order_total'].sum().reset_index()
    st.line_chart(data=rev_over_time.rename(columns={'order_date': 'index'}).set_index('index'))

    st.write("📊 Orders per Payment Method")
    method_counts = orders['payment_method'].value_counts().reset_index()
    method_counts.columns = ['method', 'orders']
    st.bar_chart(data=method_counts.set_index('method'))



# 2. Orders Analytics
with tabs[1]:
    st.subheader("🧾 Orders Analytics")
        # --- Filters ---
    st.markdown("### 🔍 Filters")
    min_date = orders['order_datetime'].min()
    max_date = orders['order_datetime'].max()

    date_range = st.date_input("Date Range", [min_date, max_date])
    selected_methods = st.multiselect(
        "Payment Methods",
        options=orders['payment_method'].dropna().unique(),
        default=orders['payment_method'].dropna().unique()
    )

    # Filtered DataFrame
    filtered_orders = orders.copy()
    filtered_orders = filtered_orders[
        (filtered_orders['order_datetime'].dt.date >= date_range[0]) &
        (filtered_orders['order_datetime'].dt.date <= date_range[1]) &
        (filtered_orders['payment_method'].isin(selected_methods))
    ]

    # --- Orders by Month ---
    st.markdown("### 📅 Orders by Month")
    with st.spinner("Loading monthly order trends..."):
        orders_by_month = (
            filtered_orders
            .assign(month=lambda df: df['order_datetime'].dt.to_period("M").astype(str))
            .groupby("month")
            .size()
            .reset_index(name="orders")
        )
        st.line_chart(orders_by_month.set_index("month"))
        st.caption("Shows how many orders were placed each month.")


    # --- Shipping Cost vs Revenue ---
    st.markdown("### 🚚 Shipping Cost vs Revenue Over Time")
    with st.spinner("Generating shipping vs revenue chart..."):
        ship_rev = (
            filtered_orders
            .assign(date=filtered_orders['order_datetime'].dt.date)
            .groupby('date')[['shipping_cost', 'order_total']]
            .sum()
            .reset_index()
        )
        st.line_chart(ship_rev.set_index('date'))
        st.caption("Compares daily shipping costs against total revenue.")


# 3. Customer Insights
with tabs[2]:
    st.subheader("🧑‍💼 Customer Insights")

    # --- Merge Orders with Customers ---
    customer_orders = orders.merge(customers, on="cust_id", how="left")

    # --- Repeat vs One-time Customers ---
    order_counts = customer_orders.groupby("cust_id").size().reset_index(name="order_count")
    repeat_customers = order_counts[order_counts["order_count"] > 1].shape[0]
    one_time_customers = order_counts[order_counts["order_count"] == 1].shape[0]

    st.metric("Repeat Customers", repeat_customers)
    st.metric("One-time Customers", one_time_customers)

    # --- Segment Distribution ---
    st.markdown("### 🧩 Segment Distribution")
    seg_counts = customers["segment"].value_counts(dropna=False).reset_index()
    seg_counts.columns = ["segment", "count"]
    if not seg_counts.empty:
        st.bar_chart(seg_counts.set_index("segment"))
    else:
        st.info("No segment data available.")

    # --- Top Customers by Spend ---
    st.markdown("### 💰 Top Customers by Spend")
    customer_orders['order_total'] = pd.to_numeric(customer_orders['order_total'], errors='coerce')
    top_spenders = (
        customer_orders.groupby(["cust_id", "full_name"])["order_total"]
        .sum()
        .reset_index()
        .sort_values(by="order_total", ascending=False)
        .head(10)
    )
    if not top_spenders.empty:
        st.bar_chart(top_spenders.set_index("full_name")["order_total"])
    else:
        st.info("No spend data available.")

    # --- Customer Table ---
    st.markdown("### 📋 All Customers")
    st.dataframe(
        customers[["cust_id", "full_name", "segment", "total_orders", "total_spent", "preferred_payment"]]
        .sort_values(by="total_spent", ascending=False)
        .reset_index(drop=True)
    )


# 4. Product Performance
with tabs[3]:
    st.subheader("📦 Product Performance")

    # --- KPIs ---
    total_products = products.shape[0]
    active_products = products[products["is_active"].astype(str).str.lower() == "true"].shape[0]
    st.metric("Total Products", total_products)
    st.metric("Active Products", active_products)

    # --- Top Selling Products ---
    st.markdown("### 🛒 Top Selling Products")
    top_products = (
        orders.groupby("product_id")
        .size()
        .reset_index(name="sales")
        .merge(products[["product_id", "product_name"]], on="product_id", how="left")
        .sort_values(by="sales", ascending=False)
        .head(10)
    )
    if not top_products.empty:
        st.bar_chart(top_products.set_index("product_name")["sales"])
    else:
        st.info("No product sales data available.")

    # --- Low Stock Products ---
    st.markdown("### 📉 Low Stock Products")
    low_stock = products[products["stock_quantity"] <= products["reorder_level"]]
    low_stock_sorted = low_stock.sort_values("stock_quantity").head(10)
    if not low_stock_sorted.empty:
        st.bar_chart(low_stock_sorted.set_index("product_name")["stock_quantity"])
    else:
        st.info("No low stock products found.")




# 5. Data Quality Tab
with tabs[4]:
    st.subheader("🧽 Data Quality Overview")

    # --- Missing Values Summary ---
    st.markdown("### ❗ Missing Values Summary")
    def missing_summary(df, name):
        missing = df.isnull().sum()
        percent = (missing / len(df)) * 100
        return pd.DataFrame({
            "dataset": name,
            "column": missing.index,
            "missing_count": missing.values,
            "missing_percent": percent.round(2)
        })

    missing_orders = missing_summary(orders, "orders")
    missing_customers = missing_summary(customers, "customers")
    missing_products = missing_summary(products, "products")

    full_missing = pd.concat([missing_orders, missing_customers, missing_products])
    st.dataframe(full_missing[full_missing["missing_count"] > 0].sort_values(by=["dataset", "missing_percent"], ascending=[True, False]), use_container_width=True)

    # --- Normalized Columns Checklist ---
    st.markdown("### ✅ Normalized Columns Checklist")
    st.write("""
    The following columns are expected to be lowercase and trimmed of whitespace:
    - `order_id`, `cust_id`, `product_id`, `payment_method` (orders)
    - `gender`, `status`, `segment` (customers)
    - `category`, `brand`, `color`, `size` (products)
    """)

   