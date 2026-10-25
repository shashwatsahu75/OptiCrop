# OptiCrop — Smart Agricultural Production & Advisory Engine

[![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask%203.x-green.svg)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn%20Random%20Forest-orange.svg)](https://scikit-learn.org/)
[![Weather API](https://img.shields.io/badge/Climate-Open--Meteo%20Live%20Sync-informational.svg)](https://open-meteo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An intelligent, data-driven precision agricultural platform that recommends optimal crop cultivars based on soil macronutrients and climate telemetry. Powered by a high-precision **Random Forest** classification ensemble, OptiCrop provides multi-class confidence scoring, alternative viable crops, nutrient deficit diagnostics, customized fertilizer advice, and real-time meteorological synchronization.

---

## Project Links

| Resource | Link |
|---|---|
| 🌐 **Live Web Application** | [https://opticrop-jb42.onrender.com/](https://opticrop-jb42.onrender.com/) |
| 💻 **GitHub Repository** | [https://github.com/shashwatsahu75/OptiCrop](https://github.com/shashwatsahu75/OptiCrop) |

---

## Key Features

- **🌱 ML-Powered Cultivar Recommendation**: Calibrated multi-class classification supporting 22 distinct commercial and food security crops.
- **🎯 Match Confidence & Top-3 Alternatives**: Provides percentage confidence scores along with runner-up viable crops for flexible agricultural planning.
- **⛅ Real-Time Live Weather Synchronization**: Automatically fetch current ambient temperature, relative humidity, and rainfall estimate using the Open-Meteo API (by city or device GPS) with zero API keys required.
- **🌾 One-Click Farm Presets**: Instantly load realistic agricultural benchmarks (*Alluvial Rice Paddy, Black Cotton Soil, Himalayan Apple Orchard, Western Ghats Coffee, Semi-Arid Chickpea, Riverbed Melon*).
- **🧪 Dynamic Soil & Nutrient Gap Analysis**: Compares tested soil parameters ($N$, $P$, $K$, $\text{pH}$) against species-specific benchmarks to identify nutrient deficiencies or excesses.
- **📋 Actionable Field Advisory**: Provides specific fertilizer amendment steps (e.g. Urea, Single Super Phosphate, MOP, Lime/Gypsum) and Integrated Pest Management (IPM) guidelines.
- **🖨️ Exportable Field Dossier**: Dedicated print and PDF stylesheet for generating clean, professional field advisory reports for agronomists and farmers.
- **⚡ Dual Mode (UI + REST API)**: Access via responsive web interface or programmatically via `/api/predict` and `/api/weather`.

---

## Supported Crops (22 Cultivars)

OptiCrop models 22 agricultural cultivars across cereal grains, legumes, horticulture, and commercial plantation crops:

| Category | Cultivars |
|---|---|
| **Cereals & Grains** | Rice, Maize |
| **Pulses & Legumes** | Chickpea, Kidney Beans (Rajma), Pigeonpeas (Arhar), Blackgram (Urad), Mungbean, Mothbeans, Lentil (Masoor) |
| **Fruits & Melons** | Apple, Banana, Grapes, Mango, Orange, Papaya, Pomegranate, Watermelon, Muskmelon |
| **Commercial & Fiber** | Cotton, Jute |
| **Plantation Crops** | Coffee, Coconut |

---

## Technology Stack

| Layer | Technologies |
|---|---|
| **Programming Language** | Python 3.9+ |
| **Web Framework** | Flask 3.x, Jinja2, Werkzeug |
| **Machine Learning** | Scikit-Learn (RandomForestClassifier, 100 Estimators) |
| **Data Processing** | Pandas, NumPy |
| **Climate Integration** | Open-Meteo Geocoding & Weather API |
| **Frontend UI/UX** | HTML5, Modern CSS (Glassmorphism, Responsive Grid, Print Stylesheet), Vanilla JS |
| **Production Server** | Gunicorn (Procfile configured) |
| **Deployment Target** | Render / PaaS Cloud |

---

## Project Structure

```bash
OptiCrop/
├── static/
│   ├── app.js                     # Interactive client (sliders, weather fetch, presets)
│   ├── pexels-pixabay-207247.jpg   # Agricultural backdrop imagery
│   └── style.css                  # Modern Agro-Tech design system & print styles
├── templates/
│   ├── home.html                  # Main diagnostic input dashboard
│   └── result.html                # Comprehensive advisory & recommendation dossier
├── app.py                         # Flask application & REST API routes
├── crop_advisory.py               # Agronomic knowledge base & diagnostic engine
├── Crop_recommendation.csv        # Multi-variable agricultural training dataset
├── model_train.py                 # Model training & serialization pipeline
├── model.pkl                      # Serialized Random Forest model
├── test_app.py                    # Unit & integration test suite
├── Procfile                       # Deployment configuration for Render
├── requirements.txt               # Python package dependencies
├── .gitignore                     # Git ignore rules
└── README.md                      # Documentation
```

---

## Installation & Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/shashwatsahu75/OptiCrop.git
cd OptiCrop
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run automated tests
```bash
python test_app.py
```

### 5. Launch the application
```bash
python app.py
```

Open your browser at **`http://localhost:5000`**.

---

## REST API Reference

### 1. Predict Best Crop
**`POST /api/predict`**

*Request body (JSON):*
```json
{
  "N": 90,
  "P": 42,
  "K": 43,
  "temperature": 20.8,
  "humidity": 82.0,
  "ph": 6.5,
  "rainfall": 202.9
}
```

*Response:*
```json
{
  "status": "success",
  "data": {
    "top_crop": "rice",
    "confidence": 99.0,
    "alternatives": [
      {
        "category": "Commercial Fiber Crop",
        "confidence": 1.0,
        "crop": "jute",
        "display_name": "Jute (Corchorus olitorius)",
        "icon": "🌾"
      }
    ],
    "soil_analysis": [
      {
        "badge_class": "status-success",
        "message": "Soil Nitrogen is well-aligned (90.0 kg/ha) with Rice's baseline requirements.",
        "param": "Nitrogen (N)",
        "status": "Optimal"
      }
    ]
  }
}
```

### 2. Live Weather Query
**`GET /api/weather?city=Pune`** or **`GET /api/weather?lat=18.52&lon=73.85`**

*Response:*
```json
{
  "status": "success",
  "location": "Pune, India",
  "temperature": 28.9,
  "humidity": 43.0,
  "rainfall": 30.0
}
```

### 3. Farm Presets
**`GET /api/presets`**

Returns ready-to-use soil profiles for one-click testing.

---

## Authors & Acknowledgments

- **Shashwat Sahu** — [GitHub Profile](https://github.com/shashwatsahu75)
- Open-source dataset sourced from agricultural research trials.
