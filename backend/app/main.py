from fastapi import FastAPI
from pydantic import BaseModel, Field
import numpy as np
import os
import joblib
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Credit Card Fraud Detection API",
    description="Predict whether a transaction is fraudulent",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# GLOBAL VARIABLES (SAFE INIT)
# =========================
model = None
scaler = None

# =========================
# LOAD MODELS ON STARTUP
# =========================
from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent  # goes from /app/app → /app

MODEL_PATH = BASE_DIR / "models" / "fraud_model.pkl"
SCALER_PATH = BASE_DIR / "models" / "scaler.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


# =========================
# INPUT SCHEMA
# =========================
class Transaction(BaseModel):
    features: list[float] = Field(
        ...,
        min_length=30,
        max_length=30,
        description="Time, Amount, V1–V28 (30 values total)"
    )


# =========================
# TEST ROUTE
# =========================
@app.get("/test-results")
def test_results():
    return {"status": "API running"}


# =========================
# PREDICT ROUTE (SAFE)
# =========================
@app.post("/predict")
def predict(data: Transaction):

    try:
        if model is None or scaler is None:
            return {"error": "Model not loaded"}

        features = np.array(data.features).reshape(1, -1)

        scaled_features = scaler.transform(features)
        prediction = model.predict(scaled_features)[0]

        return {
            "prediction": int(prediction),
            "result": "Fraud" if prediction == 1 else "Normal"
        }

    except Exception as e:
        return {
            "error": str(e)
        }