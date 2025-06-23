# utils.py
import csv
import os

def append_order_to_csv(csv_path, new_row):
    file_exists = os.path.isfile(csv_path)

    with open(csv_path, 'a', newline='') as csvfile:
        EXPECTED_FIELDS = [
            "order_id", "ord_id", "customer_id", "cust_id", "order_date", "order_datetime",
            "product_id", "item_id", "quantity", "qty", "unit_price", "price",
            "total_amount", "order_total", "shipping_cost", "tax", "discount",
            "status", "order_status", "payment_method", "shipping_address",
            "notes", "tracking_number"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=EXPECTED_FIELDS)

        # Write header if file is empty
        if not file_exists or os.stat(csv_path).st_size == 0:
            writer.writeheader()

        writer.writerow(new_row)
