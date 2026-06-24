from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pathlib import Path
import numpy as np
import joblib
import traceback
import sklearn
import pandas as pd
import random
from typing import Optional

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

model = None
scaler = None
X_test = None
y_test = None


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "fraud_model.pkl"
SCALER_PATH = BASE_DIR / "models" / "scaler.pkl"
XTEST_PATH = BASE_DIR / "models" / "X_test.csv"
YTEST_PATH = BASE_DIR / "models" / "y_test.csv"

print("MODEL PATH =", MODEL_PATH)
print("SCALER PATH =", SCALER_PATH)


@app.on_event("startup")
def load_models():

    global model, scaler, X_test, y_test

    print("STARTING BACKEND LOAD")

    try:
        print("Loading model...")
        model = joblib.load(MODEL_PATH)
        print("Model loaded")

        print("Loading scaler...")
        scaler = joblib.load(SCALER_PATH)
        print("Scaler loaded")

        try:
            print("Loading test data...")

            X_test = pd.read_csv(XTEST_PATH).head(200)
            y_test = pd.read_csv(YTEST_PATH).head(200)

            print("TEST DATA LOADED SUCCESSFULLY")

        except Exception as e:
            print("TEST DATA FAILED:", str(e))
            X_test = None
            y_test = None

        print("MODEL TYPE:", type(model))
        print("SCALER TYPE:", type(scaler))
        print("STARTUP COMPLETE")

    except Exception:
        print("MODEL LOAD FAILED")
        traceback.print_exc()




class Transaction(BaseModel):
    features: list[float] = Field(
        ...,
        min_length=30,
        max_length=30,
        description="Time, Amount, V1-V28 (30 values total)"
    )
    actual: Optional[int] = None


@app.get("/")
def home():
    return {"message": "API running", "docs": "/docs"}


@app.get("/debug")
def debug():
    return {
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "test_loaded": X_test is not None
    }


@app.get("/random-test")
def random_test():

    if X_test is None or y_test is None:
        return {"error": "Test data not loaded"}

    idx = random.randint(0, len(X_test) - 1)

    features = X_test.iloc[idx].tolist()
    actual = int(y_test.iloc[idx].values[0])

    return {
        "features": features,
        "actual": actual
    }


@app.post("/predict")
def predict(data: Transaction):

    try:
        if model is None or scaler is None:
            return {"error": "Model not loaded"}

        features = np.array(data.features).reshape(1, -1)

        scaled = scaler.transform(features)
        prediction = int(model.predict(scaled)[0])

        response = {
            "prediction": prediction,
            "result": "Fraud" if prediction == 1 else "Normal"
        }

        if data.actual is not None:
            response["actual"] = int(data.actual)
            response["correct"] = prediction == int(data.actual)

        return response

    except Exception as e:
        return {"error": str(e)}