# Just a test to check if the data is loaded correctly into the SQLite database
# and to verify the SQL queries work as expected.

import sqlite3
import pandas as pd

conn = sqlite3.connect("v1_ecommerce.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM orders LIMIT 5;")
print(cursor.fetchall())
conn.close()

# -- example queries --
# SELECT full_name, total_spent FROM customers ORDER BY total_spent DESC LIMIT 5;
# SELECT * FROM orders LIMIT 5
# SELECT order_id, cust_id FROM orders WHERE order_datetime IS NULL;
# SELECT product_id, item_id, product_name FROM products WHERE stock_quantity < 10 ORDER BY stock_quantity ASC;
# SELECT product_id, SUM(order_total) as total_revenue FROM orders GROUP BY product_id ORDER BY total_revenue DESC LIMIT 5;