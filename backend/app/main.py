from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pathlib import Path
import numpy as np
import pandas as pd
import random
import joblib
import traceback
import sklearn

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

X_TEST_PATH = BASE_DIR / "models" / "X_test.csv"
Y_TEST_PATH = BASE_DIR / "models" / "y_test.csv"

print("CURRENT FILE =", __file__)
print("BASE_DIR =", BASE_DIR)

@app.on_event("startup")
def load_models():

    global model, scaler, X_test, y_test

    print("JOBLIB VERSION:", joblib.__version__)
    print("NUMPY VERSION:", np.__version__)
    print("SKLEARN VERSION:", sklearn.__version__)

    try:
        print("================================================")
        print("STARTING LOAD")

        print("Loading model...")
        model = joblib.load(MODEL_PATH)
        print("MODEL LOADED")

        print("Loading scaler...")
        scaler = joblib.load(SCALER_PATH)
        print("SCALER LOADED")

        print("Loading X_test...")
        X_test = pd.read_csv(X_TEST_PATH)

        print("Loading y_test...")
        y_test = pd.read_csv(Y_TEST_PATH)

        print("TEST DATA LOADED")

        print("MODEL TYPE =", type(model))
        print("SCALER FEATURES =", scaler.n_features_in_)
        print("================================================")

    except Exception:
        print("LOAD FAILED")
        traceback.print_exc()


class Transaction(BaseModel):
    features: list[float] = Field(
        ...,
        min_length=30,
        max_length=30,
        description="Time, Amount, V1-V28 (30 values total)"
    )

    actual: int


@app.get("/")
def home():
    return {
        "message": "Credit Card Fraud Detection API is running",
        "docs": "/docs"
    }


@app.get("/test-results")
def test_results():
    return {"status": "API running"}


@app.get("/debug")
def debug():
    return {
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "x_test_loaded": X_test is not None,
        "y_test_loaded": y_test is not None,
        "model_type": str(type(model)) if model else None
    }


@app.get("/random-test")
def random_test():

    if X_test is None or y_test is None:
        return {"error": "Test data not loaded"}

    idx = random.randint(0, len(X_test)-1)

    features = X_test.iloc[idx].tolist()

    actual = int(y_test.iloc[idx, 0])

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

        print("INPUT SHAPE:", features.shape)

        scaled_features = scaler.transform(features)

        prediction = int(model.predict(scaled_features)[0])

        return {
            "prediction": prediction,
            "actual": data.actual,
            "correct": prediction == data.actual,
            "result": "Fraud" if prediction == 1 else "Normal"
        }

    except Exception as e:

        traceback.print_exc()

        return {
            "error": str(e)
        }