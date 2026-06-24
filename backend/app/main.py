from fastapi import FastAPI
from pydantic import BaseModel, Field
import numpy as np
import pickle
# import os
import os
import joblib

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/fraud_model.pkl")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "../models/scaler.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

print("MODEL TYPE:", type(model))
print("SCALER TYPE:", type(scaler))
print("SCALER EXPECTED FEATURES:", scaler.n_features_in_)

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

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# MODEL_PATH = os.path.join(BASE_DIR, "../models/fraud_model.pkl")
# SCALER_PATH = os.path.join(BASE_DIR, "../models/scaler.pkl")

# with open(MODEL_PATH, "rb") as f:
#     model = pickle.load(f)

# with open(SCALER_PATH, "rb") as f:
#     scaler = pickle.load(f)

# print("SCALER FEATURES:", scaler.n_features_in_)
# print("INPUT SHAPE EXPECTED:", model.n_features_in_)

class Transaction(BaseModel):
    features: list[float] = Field(
        ...,
        min_length=30,
        max_length=30,
        description="Time, Amount, V1-V28 (30 values total)"
    )


@app.get("/test-results")
def test_results():
    ...

@app.post("/predict")
def predict(data: Transaction):

    try:
        print("RAW INPUT:", data.features)

        features = np.array(data.features).reshape(1, -1)

        print("SHAPE:", features.shape)

        scaled_features = scaler.transform(features)

        print("SCALED DONE")

        prediction = model.predict(scaled_features)[0]

        return {
            "prediction": int(prediction),
            "result": "Fraud" if prediction == 1 else "Normal"
        }

    except Exception as e:
        print("ERROR OCCURRED:", str(e))
        raise e