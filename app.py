from flask import Flask, request, jsonify
from flask.logging import create_logger
import logging
import os

import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

# Load the model and scaler once
MODEL_FILENAME = os.environ.get("MODEL_FILENAME", "GradientBoostingRegressor.joblib")
try:
    clf = joblib.load(MODEL_FILENAME)
    scaler = StandardScaler().fit(initial_payload)  # Assuming you have some initial_payload to fit the scaler
except Exception as e:
    LOG.error(f"Model loading error: {str(e)}")
    exit("Model not loaded. Error: {str(e)}")

def scale(payload):
    """Scale Payload"""
    LOG.info(f"Scaling Payload: {payload}")
    scaled_adhoc_predict = scaler.transform(payload)
    return scaled_adhoc_predict

@app.route("/")
def home():
    html = "<h3>Sklearn Prediction Home, Welcome to service</h3>"
    return html

@app.route("/predict", methods=['POST'])
def predict():
    try:
        json_payload = request.json
        LOG.info(f"JSON payload: {json_payload}")
        inference_payload = pd.DataFrame(json_payload)
        LOG.info(f"inference payload DataFrame: {inference_payload}")
        scaled_payload = scale(inference_payload)
        prediction = list(clf.predict(scaled_payload))
        return jsonify({'prediction': prediction})
    except Exception as e:
        LOG.error(f"Prediction error: {str(e)}")
        return jsonify({'error': f'Prediction failed. {str(e)}'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)