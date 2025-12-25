import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

from services.detector import detect_disease
from services.weather import get_weather
from services.forecast import predict_progression, advice_for

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # 1) read inputs
        file = request.files.get("image")
        city = request.form.get("city", "").strip()

        if not file or file.filename == "":
            return jsonify({"error": "No image uploaded"}), 400
        if not city:
            return jsonify({"error": "City is required"}), 400

        # 2) save upload
        fname = secure_filename(file.filename)
        fpath = os.path.join(UPLOAD_DIR, fname)
        file.save(fpath)

        # 3) disease detection (dummy for now, fast on low PC)
        disease, confidence = detect_disease(fpath)

        # 4) weather fetch (temp °C, humidity %, rainfall mm)
        weather = get_weather(city)  # returns dict or {"error": "..."}
        if "error" in weather:
            # graceful fallback: assume dry/low risk weather
            weather = {"temp": None, "humidity": 40, "rainfall": 0.0, "city": city, "note": "Weather fallback"}

        # 5) rule-based risk forecast (today / +7d / +14d)
        today, risk7, risk14 = predict_progression(
            disease=disease,
            temp=weather["temp"],
            humidity=weather["humidity"],
            rainfall=weather["rainfall"]
        )

        # 6) prevention/treatment advice
        tips = advice_for(disease, risk7, weather)

        return jsonify({
            "disease": disease,
            "confidence": round(confidence, 3),
            "today_severity": today,
            "risk_7_days": risk7,
            "risk_14_days": risk14,
            "weather": weather,
            "advice": tips
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run: python app.py  → open http://127.0.0.1:5000
    app.run(debug=True)
