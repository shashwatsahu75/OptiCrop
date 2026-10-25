"""
Unit & Integration Tests for OptiCrop Platform
Tests machine learning prediction, confidence computation, agronomic advisory generation,
and Flask web endpoints.
"""

import unittest
import json
from app import app, get_prediction_details
from crop_advisory import CROP_PROFILES, BENCHMARKS, PRESETS, generate_crop_advisory


class OptiCropTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_crop_profiles_completeness(self):
        """Verify that all 22 crops from the dataset have complete agronomic profiles."""
        expected_crops = [
            "apple", "banana", "blackgram", "chickpea", "coconut", "coffee", "cotton",
            "grapes", "jute", "kidneybeans", "lentil", "maize", "mango", "mothbeans",
            "mungbean", "muskmelon", "orange", "papaya", "pigeonpeas", "pomegranate",
            "rice", "watermelon"
        ]
        for crop in expected_crops:
            self.assertIn(crop, CROP_PROFILES, f"Crop profile missing for: {crop}")
            prof = CROP_PROFILES[crop]
            self.assertTrue(prof.get("display_name"))
            self.assertTrue(prof.get("icon"))
            self.assertTrue(prof.get("season"))
            self.assertTrue(prof.get("growth_duration"))
            self.assertTrue(prof.get("fertilizer_guide"))
            self.assertTrue(prof.get("pest_management"))
            self.assertTrue(prof.get("economic_outlook"))

    def test_benchmarks_present(self):
        """Verify all crops have benchmark statistics."""
        self.assertEqual(len(BENCHMARKS), 22)
        for crop, stats in BENCHMARKS.items():
            for param in ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]:
                self.assertIn(param, stats)
                self.assertIn("min", stats[param])
                self.assertIn("max", stats[param])
                self.assertIn("mean", stats[param])

    def test_advisory_gap_analysis(self):
        """Test soil advisory logic for nutrient deficiency and pH alerts."""
        user_inputs = {"N": 20, "P": 45, "K": 40, "ph": 5.0, "rainfall": 220}
        advisory = generate_crop_advisory("rice", user_inputs)

        self.assertIn("profile", advisory)
        self.assertIn("soil_analysis", advisory)

        # Nitrogen should be detected as low for rice (benchmark is 60-100)
        n_analysis = next(item for item in advisory["soil_analysis"] if item["param"] == "Nitrogen (N)")
        self.assertEqual(n_analysis["status"], "Low")

        # pH should be detected as acidic (5.0 < 5.8)
        ph_analysis = next(item for item in advisory["soil_analysis"] if item["param"] == "Soil pH")
        self.assertEqual(ph_analysis["status"], "Acidic")

    def test_model_prediction_and_confidence(self):
        """Test model inference returns predicted crop, confidence %, and alternatives."""
        details = get_prediction_details(90, 42, 43, 20.8, 82.0, 6.5, 202.9)
        self.assertEqual(details["top_crop"], "rice")
        self.assertGreater(details["confidence"], 50.0)
        self.assertIsInstance(details["alternatives"], list)
        self.assertIn("profile", details)

    def test_home_route(self):
        """Test home page loads with HTTP 200."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"OptiCrop", response.data)
        self.assertIn(b"Nitrogen (N)", response.data)

    def test_predict_post_form(self):
        """Test HTML form submission to /predict."""
        form_data = {
            "N": "90",
            "P": "42",
            "K": "43",
            "temperature": "20.8",
            "humidity": "82.0",
            "ph": "6.5",
            "rainfall": "202.9"
        }
        response = self.client.post("/predict", data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Rice", response.data)
        self.assertIn(b"Model Match Confidence", response.data)

    def test_api_predict_json(self):
        """Test JSON REST endpoint /api/predict."""
        payload = {
            "N": 120,
            "P": 45,
            "K": 20,
            "temperature": 25.0,
            "humidity": 78,
            "ph": 7.0,
            "rainfall": 82
        }
        response = self.client.post(
            "/api/predict",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["top_crop"], "cotton")
        self.assertGreater(data["data"]["confidence"], 60.0)

    def test_api_presets(self):
        """Test presets endpoint returns list of farm profiles."""
        response = self.client.get("/api/presets")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        self.assertGreater(len(data["presets"]), 3)

    def test_api_weather_city(self):
        """Test weather API with city query."""
        response = self.client.get("/api/weather?city=Pune")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        self.assertIn("Pune", data["location"])
        self.assertIn("temperature", data)
        self.assertIn("humidity", data)
        self.assertIn("rainfall", data)


if __name__ == "__main__":
    unittest.main()
