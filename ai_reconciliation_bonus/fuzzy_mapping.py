import pandas as pd


df = pd.read_csv("ai_reconciliation_bonus/Dataset/reconciliation_challenge_data.csv")  

orders_schema = [
    "order_id", "cust_id", "product_id", "order_datetime", "payment_method",
    "shipping_address", "shipping_cost", "tax", "discount", "order_total"
]

def jaccard_similarity(a, b):
    set_a, set_b = set(a.lower()), set(b.lower())
    return len(set_a & set_b) / len(set_a | set_b)

fuzzy_mapping = {}
for new_col in df.columns:
    best_match = ""
    best_score = 0
    for ref_col in orders_schema:
        score = jaccard_similarity(new_col, ref_col)
        if score > best_score:
            best_match = ref_col
            best_score = score
    fuzzy_mapping[new_col] = best_match

mapping_df = pd.DataFrame(list(fuzzy_mapping.items()), columns=["new_column", "suggested_reference"])
mapping_df.to_csv("fuzzy_mapping_output.csv", index=False)

print("✅ Fuzzy mapping has been written to 'fuzzy_mapping_output.csv'.")

