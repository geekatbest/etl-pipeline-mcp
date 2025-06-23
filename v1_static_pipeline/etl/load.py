import sqlite3

DB_NAME = "v1_ecommerce.db"

def create_tables(conn):
    """Create tables using SQL if they don't exist already"""
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        cust_id TEXT PRIMARY KEY,
        full_name TEXT,
        address TEXT,
        city TEXT,
        state TEXT,
        zip_code TEXT,
        postal_code TEXT,
        status TEXT,
        total_orders INTEGER,
        total_spent REAL,
        loyalty_points INTEGER,
        preferred_payment TEXT,
        age REAL,
        birth_date TEXT,
        gender TEXT,
        segment TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        item_id INTEGER,
        product_name TEXT,
        description TEXT,
        category TEXT,
        brand TEXT,
        price REAL,
        cost REAL,
        weight REAL,
        color TEXT,
        size TEXT,
        stock_quantity INTEGER,
        stock_level INTEGER,
        reorder_level INTEGER,
        supplier_id TEXT,
        created_date TEXT,
        last_updated TEXT,
        is_active TEXT,
        rating REAL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        cust_id TEXT,
        product_id TEXT,
        order_datetime TEXT,
        payment_method TEXT,
        shipping_address TEXT,
        shipping_cost REAL,
        tax REAL,
        discount REAL,
        order_total REAL,
        FOREIGN KEY (cust_id) REFERENCES customers(cust_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
    """)
    conn.commit()

def load_to_db(orders_df, customers_df, products_df, db_name=DB_NAME):
    """Load cleaned DataFrames into SQLite database"""
    conn = sqlite3.connect(db_name)
    print(f"🗄️ Connected to {db_name}")

    create_tables(conn)

    # Load data
    customers_df.to_sql("customers", conn, if_exists="replace", index=False)
    print("✅ Customers loaded")

    products_df.to_sql("products", conn, if_exists="replace", index=False)
    print("✅ Products loaded")

    orders_df.to_sql("orders", conn, if_exists="replace", index=False)
    print("✅ Orders loaded")

    conn.close()
    print("🔒 Connection closed")

# create schema as schema.sql file locally
def export_schema(db_path="v1_ecommerce.db", output_file="v1_schema.sql"):
    with sqlite3.connect(db_path) as conn:
        with open(output_file, "w", encoding="utf-8") as f:
            for line in conn.iterdump():
                # Only keep table creation lines
                if line.startswith("CREATE TABLE") or line.startswith("CREATE INDEX"):
                    f.write(f"{line}\n")
    print(f"✅ Schema exported to {output_file}")