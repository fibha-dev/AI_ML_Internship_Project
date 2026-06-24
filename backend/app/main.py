from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pathlib import Path
import numpy as np
import joblib
import traceback
import sklearn

app = FastAPI(
    title="Credit Card Fraud Detection API",
    description="Predict whether a transaction is fraudulent",
    version="1.0"
)

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# GLOBAL VARIABLES
# =========================
model = None
scaler = None

# =========================
# PATHS
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "fraud_model.pkl"
SCALER_PATH = BASE_DIR / "models" / "scaler.pkl"

print("CURRENT FILE =", __file__)
print("BASE_DIR =", BASE_DIR)
print("MODEL PATH =", MODEL_PATH)
print("SCALER PATH =", SCALER_PATH)

# =========================
# LOAD MODELS ON STARTUP
# =========================
@app.on_event("startup")
def load_models():
    
    global model, scaler
       
    print("JOBLIB VERSION:", joblib.__version__)
    print("NUMPY VERSION:", np.__version__)
    print("SKLEARN VERSION:", sklearn.__version__)
    try:
        print("================================================")
        print("STARTING MODEL LOAD")
        print("MODEL PATH =", MODEL_PATH)
        print("SCALER PATH =", SCALER_PATH)

        print("Loading model...")
        model = joblib.load(MODEL_PATH)
        print("MODEL LOADED")

        print("Loading scaler...")
        scaler = joblib.load(SCALER_PATH)
        print("SCALER LOADED")

        print("MODEL TYPE =", type(model))
        print("SCALER FEATURES =", scaler.n_features_in_)
        print("MODEL LOADED SUCCESSFULLY")
        print("================================================")

    except Exception:
        print("MODEL LOAD FAILED")
        traceback.print_exc()


# =========================
# INPUT SCHEMA
# =========================
class Transaction(BaseModel):
    features: list[float] = Field(
        ...,
        min_length=30,
        max_length=30,
        description="Time, Amount, V1-V28 (30 values total)"
    )


# =========================
# HOME ROUTE
# =========================
@app.get("/")
def home():
    return {
        "message": "Credit Card Fraud Detection API is running",
        "docs": "/docs"
    }


# =========================
# TEST ROUTE
# =========================
@app.get("/test-results")
def test_results():
    return {"status": "API running"}


# =========================
# PREDICT ROUTE
# =========================
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
            "result": "Fraud" if prediction == 1 else "Normal"
        }

    except Exception as e:
        return {
            "error": str(e)
        }
