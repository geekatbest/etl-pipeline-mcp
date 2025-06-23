# app.py
from flask import Flask, request, jsonify
from utils.debounce import should_trigger
from utils.utils import append_order_to_csv
from etl.pipeline import run_pipeline  

CSV_PATH = 'D:/ml_projects/quantifai-assignment/v2_dynamic_pipeline/datasets/orders_unstructured_data.csv'

app = Flask(__name__)

from utils.logger_config import setup_logger
logger = setup_logger("API")

@app.route('/new_order', methods=['POST'])
def new_order():
    new_order = request.get_json()
    logger.info(f"Received new order: {new_order}")

    try:
        append_order_to_csv(CSV_PATH, new_order)
        logger.info("Order appended to CSV")
    except Exception as e:
        logger.exception("Failed to append to CSV")
        return jsonify({'status': 'CSV append failed', 'error': str(e)}), 500

    if should_trigger():
        try:
            run_pipeline()
            logger.info("Pipeline triggered by API")
            return jsonify({'status': 'Pipeline triggered'}), 200
        except Exception as e:
            logger.exception("Pipeline execution failed")
            return jsonify({'status': 'Pipeline error', 'error': str(e)}), 500
    else:
        logger.warning("Debounced too many triggers")
        return jsonify({'status': 'Debounced Try again later'}), 429


if __name__ == '__main__':
    app.run(debug=True)
