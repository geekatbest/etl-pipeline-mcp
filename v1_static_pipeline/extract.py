import pandas as pd
import os

DATA_DIR = "./datasets"

def load_orders(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    assert not df.empty, "Orders CSV is empty"
    return df

def load_customers(path: str) -> pd.DataFrame:
    df = pd.read_json(path)
    assert isinstance(df, pd.DataFrame), "Customers JSON did not parse correctly"
    return df

def load_products(path: str) -> pd.DataFrame:
    df = pd.read_json(path)
    assert isinstance(df, pd.DataFrame), "Products JSON did not parse correctly"
    return df

def extract_all(data_dir: str = DATA_DIR) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    print(f"📂 Loading datasets from {data_dir}")
    orders = load_orders(os.path.join(data_dir, "orders_unstructured_data.csv"))
    customers = load_customers(os.path.join(data_dir, "customers_messy_data.json"))
    products = load_products(os.path.join(data_dir, "products_inconsistent_data.json"))
    
    print("✅ All datasets loaded successfully")
    return orders, customers, products
