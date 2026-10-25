"""
OptiCrop - Smart Agricultural Production Optimization Engine
Flask web application serving crop predictions, live weather integrations, and agronomic guidance.
"""

import os
import pickle
import numpy as np
import pandas as pd
import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for

from crop_advisory import CROP_PROFILES, BENCHMARKS, PRESETS, generate_crop_advisory

app = Flask(__name__)

# Load trained Random Forest model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except Exception as e:
    model = None
    print(f"Warning: Could not load model.pkl: {e}")

FEATURE_NAMES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

def get_prediction_details(n, p, k, temp, hum, ph, rain):
    """
    Computes top prediction, confidence probability, runner-up alternatives,
    and detailed agronomic soil gap advisory.
    """
    if model is None:
        raise RuntimeError("Model is not initialized.")

    features = pd.DataFrame([[n, p, k, temp, hum, ph, rain]], columns=FEATURE_NAMES)
    user_inputs = {
        "N": n,
        "P": p,
        "K": k,
        "temperature": temp,
        "humidity": hum,
        "ph": ph,
        "rainfall": rain,
    }

    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(features)[0]
        classes = model.classes_
        ranked = sorted(zip(classes, probs), key=lambda x: x[1], reverse=True)

        top_crop = str(ranked[0][0])
        top_confidence = round(float(ranked[0][1]) * 100, 1)

        alternatives = []
        for alt_crop, alt_prob in ranked[1:4]:
            alt_crop_str = str(alt_crop)
            alt_prof = CROP_PROFILES.get(alt_crop_str, {})
            alternatives.append({
                "crop": alt_crop_str,
                "display_name": alt_prof.get("display_name", alt_crop_str.title()),
                "icon": alt_prof.get("icon", "🌱"),
                "category": alt_prof.get("category", "Crop"),
                "confidence": round(float(alt_prob) * 100, 1),
            })
    else:
        top_crop = str(model.predict(features)[0])
        top_confidence = 95.0
        alternatives = []

    advisory = generate_crop_advisory(top_crop, user_inputs)

    return {
        "prediction": top_crop,
        "top_crop": top_crop,
        "confidence": top_confidence,
        "alternatives": alternatives,
        "advisory": advisory,
        "profile": advisory["profile"],
        "benchmarks": advisory["benchmark"],
        "soil_analysis": advisory["soil_analysis"],
        "inputs": user_inputs,
    }


@app.route("/")
def home():
    """Render home dashboard with form controls and farm presets."""
    return render_template("home.html", presets=PRESETS)


@app.route("/predict", methods=["GET", "POST"], strict_slashes=False)
def predict():
    """Handle standard HTML form submission."""
    if request.method == "GET":
        return redirect(url_for("home"))

    try:
        n = float(request.form.get("N", 0))
        p = float(request.form.get("P", 0))
        k = float(request.form.get("K", 0))
        temp = float(request.form.get("temperature", 0))
        hum = float(request.form.get("humidity", 0))
        ph = float(request.form.get("ph", 0))
        rain = float(request.form.get("rainfall", 0))

        details = get_prediction_details(n, p, k, temp, hum, ph, rain)
        return render_template("result.html", **details)
    except Exception as e:
        return render_template(
            "result.html",
            prediction="Invalid Input",
            error=str(e),
            profile={"display_name": "Unknown", "icon": "⚠️", "category": "Error"},
            confidence=0,
            alternatives=[],
            soil_analysis=[],
            inputs={},
            benchmarks={},
        )


@app.route("/api/predict", methods=["POST"])
def api_predict():
    """REST API endpoint for asynchronous prediction previews."""
    try:
        data = request.get_json(silent=True) or request.form
        n = float(data.get("N", 0))
        p = float(data.get("P", 0))
        k = float(data.get("K", 0))
        temp = float(data.get("temperature", 0))
        hum = float(data.get("humidity", 0))
        ph = float(data.get("ph", 0))
        rain = float(data.get("rainfall", 0))

        details = get_prediction_details(n, p, k, temp, hum, ph, rain)
        return jsonify({"status": "success", "data": details})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/presets", methods=["GET"])
def api_presets():
    """Returns realistic soil and climate presets for instant form autofill."""
    return jsonify({"status": "success", "presets": PRESETS})


@app.route("/api/weather", methods=["GET"])
def api_weather():
    """
    Fetches real-time environmental weather (temperature, humidity, precipitation)
    via Open-Meteo free API without requiring any API keys.
    """
    city = request.args.get("city", "").strip()
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    location_name = city

    try:
        # Step 1: Geocode city if provided
        if city:
            geo_url = (
                f"https://geocoding-api.open-meteo.com/v1/search?"
                f"name={requests.utils.quote(city)}&count=1&language=en&format=json"
            )
            geo_res = requests.get(geo_url, timeout=5)
            if geo_res.status_code != 200 or not geo_res.json().get("results"):
                return jsonify({"status": "error", "message": f"City '{city}' not found."}), 404

            first_match = geo_res.json()["results"][0]
            lat = first_match["latitude"]
            lon = first_match["longitude"]
            location_name = f"{first_match.get('name')}, {first_match.get('country', '')}".strip(", ")
        elif not (lat and lon):
            return jsonify({"status": "error", "message": "Please specify a city or latitude/longitude."}), 400

        # Step 2: Fetch current weather & 7-day precipitation estimate
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation"
            f"&daily=precipitation_sum&timezone=auto"
        )
        weather_res = requests.get(weather_url, timeout=5)
        if weather_res.status_code != 200:
            return jsonify({"status": "error", "message": "Failed to fetch weather data."}), 502

        w_json = weather_res.json()
        current = w_json.get("current", {})
        daily = w_json.get("daily", {})

        temperature = current.get("temperature_2m", 25.0)
        humidity = current.get("relative_humidity_2m", 60.0)

        # Estimate rainfall (precipitation sum over available window scaled to typical seasonal cycle or sum)
        precip_sums = daily.get("precipitation_sum", [])
        total_precip = sum([p for p in precip_sums if p is not None]) if precip_sums else 0.0
        # If total precipitation is minimal (dry spell), provide a healthy baseline scaled to monthly/seasonal
        estimated_rainfall = round(max(total_precip * 3.5, 30.0), 1)

        return jsonify({
            "status": "success",
            "location": location_name or f"Lat: {lat}, Lon: {lon}",
            "latitude": lat,
            "longitude": lon,
            "temperature": round(temperature, 1),
            "humidity": round(humidity, 1),
            "rainfall": estimated_rainfall,
            "current_rain_mm": current.get("precipitation", 0.0),
        })

    except requests.exceptions.Timeout:
        return jsonify({"status": "error", "message": "Weather service request timed out."}), 504
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)