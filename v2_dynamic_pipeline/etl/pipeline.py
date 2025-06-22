# etl/pipeline.py

from .extract import extract_all
from .transform import clean_orders, clean_customers, clean_products
from .load import load_to_db, export_schema

def run_pipeline():
    print("🚀 Starting ETL pipeline...")

    # Step 1: Extract
    try:
        orders_raw, customers_raw, products_raw = extract_all()
        print("📥 Extraction completed")
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        raise

    # Step 2: Transform
    try:
        orders_clean = clean_orders(orders_raw)
        customers_clean = clean_customers(customers_raw)
        products_clean = clean_products(products_raw)
        print("🧼 Transformation completed")
    except Exception as e:
        print(f"❌ Transformation failed: {e}")
        raise

    # Step 3: Load to DB
    try:
        load_to_db(orders_clean, customers_clean, products_clean)
        print("💾 Loading to database completed")
    except Exception as e:
        print(f"❌ Load to DB failed: {e}")
        raise

    # Step 4: Export schema
    try:
        export_schema()
        print("📤 Schema exported successfully")
    except Exception as e:
        print(f"❌ Schema export failed: {e}")
        raise

    print("✅ ETL pipeline completed successfully")
