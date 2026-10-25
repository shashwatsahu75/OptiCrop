from flask import Flask, render_template, request
import numpy as np
import pickle
import os

app = Flask(__name__)

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predict", methods=["POST"], strict_slashes=False)
def predict():
    try:
        N = float(request.form["N"])
        P = float(request.form["P"])
        K = float(request.form["K"])
        temperature = float(request.form["temperature"])
        humidity = float(request.form["humidity"])
        ph = float(request.form["ph"])
        rainfall = float(request.form["rainfall"])

        features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        prediction = model.predict(features)[0]

        return render_template("result.html", prediction=prediction)
    except Exception:
        return render_template("result.html", prediction="Invalid input")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)