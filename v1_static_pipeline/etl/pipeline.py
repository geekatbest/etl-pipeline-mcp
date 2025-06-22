from extract import extract_all
from transform import clean_orders, clean_customers, clean_products
from load import load_to_db
from load import export_schema
from IPython.display import display

# step 1 extract

orders_raw, customers_raw, products_raw = extract_all()

# step 2 transform
orders_clean = clean_orders(orders_raw)
customers_clean = clean_customers(customers_raw)
products_clean = clean_products(products_raw)

# step 3 display outputs
print("✅ Orders Cleaned:")
display(orders_clean.head())
display(orders_clean.info())

print("\n✅ Customers Cleaned:")
display(customers_clean.head())
display(customers_clean.info())

print("\n✅ Products Cleaned:")
display(products_clean.head())
display(products_clean.info())


# step 4 load to database
load_to_db(orders_clean, customers_clean, products_clean)

# step 5 export schema
export_schema()