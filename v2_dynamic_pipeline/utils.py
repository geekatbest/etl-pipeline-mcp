# utils.py
import csv
import os

def append_order_to_csv(csv_path, new_row):
    file_exists = os.path.isfile(csv_path)

    with open(csv_path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=new_row.keys())

        # Write header if file is empty
        if not file_exists or os.stat(csv_path).st_size == 0:
            writer.writeheader()

        writer.writerow(new_row)
