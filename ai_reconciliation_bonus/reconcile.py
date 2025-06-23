import pandas as pd

recon_df = pd.read_csv("ai_reconciliation_bonus/Dataset/reconciliation_challenge_data.csv")


orders_df = pd.read_csv("ai_reconciliation_bonus/Dataset/orders_clean.csv")  


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


recon_renamed = recon_df.rename(columns=corrected_mapping)


for col in ["order_id", "cust_id", "product_id"]:
    recon_renamed[col] = recon_renamed[col].astype(str).str.strip()
    orders_df[col] = orders_df[col].astype(str).str.strip()


joined = pd.merge(
    recon_renamed,
    orders_df,
    on=["order_id", "cust_id", "product_id"],
    how="inner",
    suffixes=("_recon", "_orders")
)

joined.to_csv("reconciled_joined.csv", index=False)
print("Joined reconciliation and orders tables successfully. Output saved to 'reconciled_joined.csv'.")