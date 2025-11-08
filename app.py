from flask import Flask, request, jsonify, render_template
import numpy as np
import joblib
import tensorflow as tf
import csv
from datetime import datetime

# ---------------------------------------------
# Initialize Flask App
# ---------------------------------------------
app = Flask(__name__, template_folder="templates", static_folder="static")

# ---------------------------------------------
# Load Model and Scaler
# ---------------------------------------------
try:
    model = tf.keras.models.load_model("energy_forecast_model.h5", compile=False)
    feature_scaler = joblib.load("feature_scaler.pkl")
    print("✅ Model and Scaler loaded successfully.")
except Exception as e:
    print("❌ Error loading model or scaler:", e)

# ---------------------------------------------
# Frontend Route (Home Page)
# ---------------------------------------------
@app.route('/')
def home():
    return render_template("index.html")  # Loads frontend page

# ---------------------------------------------
# Prediction Endpoint (used by Frontend + Java)
# ---------------------------------------------
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Step 1: Get JSON data
        data = request.get_json()
        print("\n🔍 Raw data received:", data)

        # Step 2: Convert to numpy array
        X = np.array(data["input"])
        print("📏 Input shape before reshape:", X.shape)

        # Step 3: Ensure correct shape (1, 1, 36)
        if X.ndim == 2:
            X = X.reshape(1, 1, X.shape[1])
        elif X.ndim == 1:
            X = X.reshape(1, 1, -1)
        elif X.ndim == 4:
            X = X.reshape(1, 1, X.shape[-1])  # Fix accidental extra dimension

        print("✅ Final input shape:", X.shape)

        # Step 4: Scale features
        X_scaled = feature_scaler.transform(X.reshape(-1, X.shape[-1]))

        # Step 5: Predict using model
        y_pred = model.predict(X_scaled.reshape(1, 1, -1))
        prediction = float(y_pred[0][0])
        print("🔮 Predicted Load:", prediction)

        # Step 6: Log prediction with timestamp
        with open("prediction_log.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), prediction])
        print("📝 Prediction logged successfully.")

        # Step 7: Return result
        return jsonify({"status": "success", "predicted_load": prediction})

    except Exception as e:
        print("❌ Error during prediction:", e)
        return jsonify({"status": "error", "message": str(e)})

# ---------------------------------------------
# Optional Route to View Logs in Browser
# ---------------------------------------------
@app.route('/logs')
def view_logs():
    try:
        logs = []
        with open("prediction_log.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                logs.append({"timestamp": row[0], "predicted_load": row[1]})
        return jsonify({"status": "success", "logs": logs})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# ---------------------------------------------
# Run the Flask App
# ---------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
