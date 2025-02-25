from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd
import pickle
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Enable CORS to allow requests from React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all domains (change to specific domain for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Load pre-trained model and scaler
with open("mi_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# Define input data model
class PatientData(BaseModel):
    Age: int
    Sex: int  # 0 = Female, 1 = Male
    Chest_Pain: int
    Dizziness: int
    Shoulder_Pain: int
    Fatigue: int
    ECG_Abnormality: int
    Troponin_Level: float
    Hypertension: int
    Diabetes: int
    Prior_Heart_Disease: int

# API endpoint for MI prediction
@app.post("/predict")
def predict_mi(data: PatientData):
    # Convert input data into a dictionary
    input_dict = {
        "Age": data.Age,
        "Sex": data.Sex,
        "Chest_Pain": data.Chest_Pain,
        "Dizziness": data.Dizziness,
        "Shoulder_Pain": data.Shoulder_Pain,
        "Fatigue": data.Fatigue,
        "ECG_Abnormality": data.ECG_Abnormality,
        "Troponin_Level": data.Troponin_Level,
        "Hypertension": data.Hypertension,
        "Diabetes": data.Diabetes,
        "Prior_Heart_Disease": data.Prior_Heart_Disease
    }

    # Convert input dictionary to a Pandas DataFrame
    input_df = pd.DataFrame([input_dict])

    # Scale the input data using the fitted scaler
    input_scaled = scaler.transform(input_df)

    # Make prediction
    prediction = model.predict(input_scaled)
    probability = model.predict_proba(input_scaled)[:, 1]  # Probability of MI

    return {"MI_Prediction": int(prediction[0]), "Probability": float(probability[0])}
