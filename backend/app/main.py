from fastapi import FastAPI
from pydantic import BaseModel, Field
import numpy as np
import pickle
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Credit Card Fraud Detection API",
    description="Predict whether a transaction is fraudulent",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://ai-ml-internship-project.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "../models/fraud_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "../models/scaler.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(SCALER_PATH, "rb") as f:
    scaler = pickle.load(f)


class Transaction(BaseModel):
    features: list[float] = Field(
        ...,
        min_length=30,
        max_length=30,
        description="Time, Amount, V1-V28 (30 values total)"
    )


@app.get("/")
def home():
    return {
        "message": "Fraud Detection API is running"
    }


@app.post("/predict")
def predict(data: Transaction):

    features = np.array(data.features).reshape(1, -1)

    scaled_features = scaler.transform(features)

    prediction = model.predict(scaled_features)[0]

    return {
        "prediction": int(prediction),
        "result": "Fraud" if prediction == 1 else "Normal"
    }