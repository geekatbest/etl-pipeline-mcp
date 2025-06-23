import pandas as pd


df = pd.read_csv("ai_reconciliation_bonus/Dataset/reconciliation_challenge_data.csv")  


orders_schema = [
    "order_id", "cust_id", "product_id", "order_datetime", "payment_method",
    "shipping_address", "shipping_cost", "tax", "discount", "order_total"
]

corrected_mapping = {
    "transaction_ref": "order_id",
    "client_reference": "cust_id",
    "item_reference": "product_id",
    "transaction_date": "order_datetime",
    "amount_paid": "order_total",
    "discount_applied": "discount",
    "shipping_fee": "shipping_cost",
    "tax_amount": "tax"
}

print("\nCorrected Mapping After Gemini & Manual Reasoning:\n")
for k, v in corrected_mapping.items():
    print(f"{k} -> {v}")