import os
import time
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# Use the flash model for lower quota usage
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def prompt_gemini(new_col, sample_values, reference_schema):
    prompt = f"""
You are reconciling column schemas.

- New column: "{new_col}"
- Sample values: {sample_values}
- Reference schema: {reference_schema}

Question:
Is this new column equivalent to any of the reference fields?
Respond in JSON format:

{{
  "equivalent": true/false,
  "standard_name": "...",
  "confidence": 0-1 float,
  "reason": "short explanation"
}}
"""
    response = model.generate_content(prompt)
    return response.text

def generate_sample_values(csv_path, column, n=2):
    df = pd.read_csv(csv_path, usecols=[column])
    samples = df[column].dropna().unique().tolist()
    return samples[:n]

if __name__ == "__main__":
    mapping_df = pd.read_csv(
        "ai_reconciliation_bonus/fuzzy_mapping_output.csv",  
        header=0,
        names=["new_column", "suggested_reference"]
    )
    data_df = pd.read_csv("ai_reconciliation_bonus/Dataset/reconciliation_challenge_data.csv")
    reference_schema = data_df.columns.tolist()
    
    results = []
    max_requests = 5
    count = 0

    for _, row in mapping_df.iterrows():
        if count >= max_requests:
            break
        new_col = row['new_column']
        suggested = row['suggested_reference']

        try:
            sample_values = generate_sample_values("ai_reconciliation_bonus/Dataset/reconciliation_challenge_data.csv", new_col)
            gemini_response = prompt_gemini(new_col, sample_values, reference_schema)
            results.append({
                "new_column": new_col,
                "gemini_response": gemini_response
            })
            time.sleep(10)  
        except Exception as e:
            results.append({
                "new_column": new_col,
                "gemini_response": f"ERROR: {str(e)}"
            })
        count += 1

    pd.DataFrame(results).to_csv("gemini_mapping_responses.csv", index=False)
