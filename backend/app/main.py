from fastapi import FastAPI
from pydantic import BaseModel, Field
import numpy as np
import pickle
import os

# CORS (IMPORTANT for React frontend later)
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Credit Card Fraud Detection API",
    description="Predict whether a transaction is fraudulent",
    version="1.0"
)

# Allow frontend (React) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # later you can restrict to React URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Load model and scaler ----------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

model_path = os.path.join(BASE_DIR, "models", "fraud_model.pkl")
scaler_path = os.path.join(BASE_DIR, "models", "scaler.pkl")

with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(scaler_path, "rb") as f:
    scaler = pickle.load(f)


# ---------- Input schema ----------
class Transaction(BaseModel):
    features: list[float] = Field(
        ...,
        min_length=30,
        max_length=30,
        description="Time, Amount, V1-V28 (30 values total)"
    )


# ---------- Home route ----------
@app.get("/")
def home():
    return {
        "message": "Fraud Detection API is running"
    }


# ---------- Prediction route ----------
@app.post("/predict")
def predict(data: Transaction):

    features = np.array(data.features).reshape(1, -1)

    prediction = model.predict(features)[0]

    return {
        "prediction": int(prediction),
        "result": "Fraud" if prediction == 1 else "Normal"
    }