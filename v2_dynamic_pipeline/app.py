# app.py
from flask import Flask, request, jsonify
from debounce import should_trigger
from utils import append_order_to_csv
from etl.pipeline import run_pipeline  # Your existing orchestrator

CSV_PATH = 'data/orders_unstructured_data.csv'

app = Flask(__name__)

@app.route('/new_order', methods=['POST'])
def new_order():
    new_order = request.get_json()

    # ✅ Append safely to CSV
    try:
        append_order_to_csv(CSV_PATH, new_order)
    except Exception as e:
        return jsonify({'status': 'CSV append failed', 'error': str(e)}), 500

    # 🔁 Trigger pipeline with debounce
    if should_trigger():
        try:
            run_pipeline()
            return jsonify({'status': 'Pipeline triggered'}), 200
        except Exception as e:
            return jsonify({'status': 'Pipeline error', 'error': str(e)}), 500
    else:
        return jsonify({'status': 'Debounced – Try again later'}), 429

if __name__ == '__main__':
    app.run(debug=True)
