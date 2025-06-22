import sqlite3
import pandas as pd

conn = sqlite3.connect("ecommerce.db")
conn.execute("PRAGMA foreign_keys = ON")
df = pd.read_sql_query("PRAGMA foreign_key_list(products);", conn)
print(df)

conn.close()

# SELECT full_name, total_spent FROM customers ORDER BY total_spent DESC LIMIT 5;
# SELECT * FROM orders LIMIT 5
# SELECT order_id, cust_id FROM orders WHERE order_datetime IS NULL;
# SELECT product_id, item_id, product_name FROM products WHERE stock_quantity < 10 ORDER BY stock_quantity ASC;
# SELECT product_id, SUM(order_total) as total_revenue FROM orders GROUP BY product_id ORDER BY total_revenue DESC LIMIT 5;