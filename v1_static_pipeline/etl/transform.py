import pandas as pd

# Transform functions to clean and standardize data
# These fuctions are designed to handle missing values, standardize formats, and remove duplicates in the DataFrames.


# Cleaning fuction for Orders DataFrame
def clean_orders(df: pd.DataFrame, null_threshold: float = 0.9) -> pd.DataFrame:
    df = df.copy()
    df.replace(['', 'null', 'NULL', 'N/A', 'na'], pd.NA, inplace=True)
    df = df.loc[:, df.isnull().mean() < null_threshold]
    str_cols = df.select_dtypes(include='object').columns
    df[str_cols] = df[str_cols].applymap(lambda x: x.strip().lower() if isinstance(x, str) else x)
    for col in ['shipping_cost', 'tax', 'discount', 'unit_price', 'price', 'order_total', 'total_amount']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    if 'order_datetime' in df.columns:
        df['order_datetime'] = pd.to_datetime(df['order_datetime'], errors='coerce')
    elif 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df.drop_duplicates(inplace=True)
    keep_cols = [
        'order_id', 'cust_id', 'product_id',
        'order_datetime', 'payment_method', 'shipping_address',
        'shipping_cost', 'tax', 'discount', 'order_total'
    ]
    df = df[[col for col in keep_cols if col in df.columns]]
    return df

# Cleaning function for Customers DataFrame
def clean_customers(df: pd.DataFrame, null_threshold: float = 0.9) -> pd.DataFrame:
    df = df.copy()
    drop_cols = [
        'customer_id', 'customer_name', 'email', 'phone', 'phone_number',
        'email_address', 'customer_status', 'reg_date', 'registration_date'
    ]
    df.drop(columns=[col for col in drop_cols if col in df.columns], inplace=True)
    df.replace(['', 'null', 'NULL', 'N/A', 'na'], pd.NA, inplace=True)
    def standardize_name(name):
        if not isinstance(name, str):
            return pd.NA
        if '@' in name or '.' in name.split()[-1]:
            return pd.NA
        name = name.strip().lower().replace('_', ' ').replace('-', ' ')
        return ' '.join(part.capitalize() for part in name.split())
    if 'full_name' in df.columns:
        df['full_name'] = df['full_name'].apply(standardize_name)
    numeric_cols = ['total_spent', 'loyalty_points', 'age', 'total_orders']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    if 'birth_date' in df.columns:
        df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')
    for col in ['preferred_payment', 'gender', 'segment']:
        if col in df.columns:
            df[col] = df[col].str.lower().str.strip()
    if 'status' in df.columns:
        df['status'] = df['status'].str.lower().map({
            'active': 'active',
            'suspended': 'suspended',
            'cancelled': 'cancelled'
        })
    df = df.loc[:, df.isnull().mean() < null_threshold]
    df.drop_duplicates(inplace=True)
    return df

# Cleaning function for Products DataFrame
def clean_products(df: pd.DataFrame, null_threshold: float = 0.9) -> pd.DataFrame:
    df = df.copy()
    drop_cols = [
        'item_name', 'product_category', 'manufacturer',
        'list_price', 'dimensions'
    ]
    df.drop(columns=[col for col in drop_cols if col in df.columns], inplace=True)
    df.replace(['', 'null', 'NULL', 'N/A', 'na'], pd.NA, inplace=True)
    str_cols = df.select_dtypes(include='object').columns
    df[str_cols] = df[str_cols].applymap(lambda x: x.strip() if isinstance(x, str) else x)
    if 'is_active' in df.columns:
        df['is_active'] = df['is_active'].str.lower().map({
            'yes': True,
            'no': False,
            'active': True,
            'inactive': False
        })
    numeric_cols = ['price', 'cost', 'weight', 'stock_quantity', 'stock_level', 'reorder_level', 'rating']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    for col in ['created_date', 'last_updated']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    for col in ['brand', 'category', 'color', 'size']:
        if col in df.columns:
            df[col] = df[col].str.lower()
    df = df.loc[:, df.isnull().mean() < null_threshold]
    df.drop_duplicates(inplace=True)

    return df
