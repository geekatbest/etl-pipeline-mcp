# etl/pipeline.py

from .extract import extract_all
from .transform import clean_orders, clean_customers, clean_products
from .load import load_to_db, export_schema

from logger_config import setup_logger
logger = setup_logger("ETL")

def run_pipeline():
    logger.info("🚀 Starting ETL pipeline...")

    # Step 1: Extract
    try:
        orders_raw, customers_raw, products_raw = extract_all()
        logger.info("Data extraction complete")
    except Exception as e:
        logger.exception(f"Extraction failed: {e}")
        raise

    # Step 2: Transform
    try:
        orders_clean = clean_orders(orders_raw)
        customers_clean = clean_customers(customers_raw)
        products_clean = clean_products(products_raw)
        logger.info("Data transformed")
    except Exception as e:
        logger.exception(f"Transformation failed: {e}")
        raise

    # Step 3: Load to DB
    try:
        load_to_db(orders_clean, customers_clean, products_clean)
        logger.info("Data loaded into DB")
    except Exception as e:
        logger.exception(f"Load to DB failed: {e}")
        raise

    # Step 4: Export schema
    try:
        export_schema()
        logger.info("Schema exported successfully")
    except Exception as e:
        logger.exception(f"Schema export failed: {e}")
        raise

    logger.info("ETL pipeline finished")
