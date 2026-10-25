
# OptiCrop

A machine learning-based web application that recommends the most suitable crop based on soil nutrients and environmental conditions. The application leverages a classification model integrated with the Flask web framework to provide real-time crop recommendations through a simple and responsive web interface.
## Project Links
| Resource | Link |
|---|---|
| Live Demo | [https://opticrop-jb42.onrender.com/](https://opticrop-jb42.onrender.com/) |
| GitHub Repository | [https://github.com/sahushashwat75/OptiCrop](https://github.com/sahushashwat75/OptiCrop) |

## Project Overview

OptiCrop helps users identify the most suitable crop to grow based on environmental and soil parameters. Traditional farming decisions often rely on experience, but this project uses machine learning to make crop selection more data-driven and efficient. Similar crop recommendation systems analyze soil nutrients and climate variables to support intelligent agricultural decision-making. 
This project follows the complete machine learning lifecycle, including data preprocessing, model training, evaluation, deployment, and user interaction through a Flask web application. The overall idea is to convert agricultural inputs into an instant crop recommendation through a user-friendly interface.

## Features

- Soil and weather parameter input through an intuitive web interface.
- Crop recommendation prediction using machine learning.
- Real-time prediction results.
- Input validation for all parameters.
- Responsive and user-friendly interface.
- Classification-based prediction model.
- Flask backend integration.
- Cloud deployment on Render.

## Machine Learning

The following machine learning algorithms were trained and evaluated:

- Decision Tree
- Random Forest
- K-Nearest Neighbors (KNN)
- SVM
- XGBoost

After performance evaluation, the best-performing model was selected as the final deployed model. Crop recommendation work commonly compares these supervised classification algorithms and chooses the one with the best test performance.

## Technology Stack

| Layer | Technologies |
|---|---|
| Programming Language | Python |
| Web Framework | Flask |
| Machine Learning | Scikit-learn, XGBoost |
| Data Processing | Pandas, NumPy |
| Model Storage | Joblib / Pickle |
| Frontend | HTML5, CSS3, Jinja2 |
| Development Tools | Jupyter Notebook, VS Code |
| Version Control | Git, GitHub |
| Deployment | Render |

## Project Structure

```bash
OptiCrop/
│
├── static/
│   ├── pexels-pixabay-207247.jpg
│   └── style.css
│
├── templates/
│   ├── home.html
│   └── result.html
│
├── app.py
├── Crop_recommendation.csv
├── model_train.py
├── model.pkl
├── Procfile
└── requirements.txt
```

## Installation

### Clone the repository
```bash
git clone https://github.com/sahushashwat75/OptiCrop.git
```

### Navigate to the project directory
```bash
cd OptiCrop
```

### Create a virtual environment
```bash
python -m venv venv
```

### Activate the virtual environment

**Windows**
```bash
venv\Scripts\activate
```

**Linux / macOS**
```bash
source venv/bin/activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the application
```bash
python app.py
```

### Open in browser
```bash
http://127.0.0.1:5000
```

## Input Features

The prediction model uses the following agricultural parameters:

- Nitrogen
- Phosphorus
- Potassium
- Temperature
- Humidity
- pH
- Rainfall

These are the standard inputs used in crop recommendation systems because they strongly influence which crop will grow best in a given region.
## Prediction Output

The system predicts the most suitable crop for the given conditions.

## Future Improvements

- Fertilizer recommendation.
- Crop yield prediction.
- Live weather API integration.
- Location-based crop recommendation.
- Interactive agriculture visualizations.
- Mobile application.
- Advanced ensemble or deep learning models.
- Multilingual support.
- SMS or email alert system. 

## Deployment

The application is deployed on Render and is publicly accessible. 

## Live Application

[https://opticrop-jb42.onrender.com/](https://opticrop-jb42.onrender.com/)

## Authors

- Shashwat Sahu

## License

This project is developed for educational and academic purposes.
