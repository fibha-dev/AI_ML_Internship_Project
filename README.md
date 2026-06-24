# Credit Card Fraud Detection (Full Stack ML App)

A full-stack machine learning web application that detects fraudulent credit card transactions using an **XGBoost classifier**.

## Live Demo

* **Frontend:** https://ai-ml-internship-project.vercel.app
* **Backend API Docs:** https://endearing-liberation-production-8ee8.up.railway.app

## Problem Statement

Predict whether a credit card transaction is:

* **0 → Normal**
* **1 → Fraud**

**Input:** 30 numerical features (Time, Amount, V1–V28)

## Tech Stack

### Frontend

* React
* Axios

### Backend

* FastAPI
* NumPy
* Pandas
* Scikit-learn
* XGBoost

### Deployment

* Vercel (Frontend)
* Railway (Backend)
* Docker

## Architecture

```
React Frontend
       ↓
FastAPI Backend
       ↓
StandardScaler
       ↓
XGBoost Model
       ↓
Prediction Response
```

## API

### POST `/predict`

Request:

```json
{
  "features": [30 numbers],
  "actual": 0
}
```

Response:

```json
{
  "prediction": 0,
  "actual": 0,
  "correct": true,
  "result": "Normal"
}
```

### GET `/random-test`

Returns a random sample from the test dataset for evaluation.

## Features

* Real-time fraud detection
* XGBoost classification model
* Feature scaling with StandardScaler
* Actual vs predicted comparison
* Random test sample generation
* REST API with FastAPI
* Responsive React frontend
* Dockerized backend deployment
* Cloud deployment with Railway and Vercel

## How It Works

1. User enters transaction features or loads a sample transaction.
2. React sends the data to the FastAPI backend.
3. Features are scaled using StandardScaler.
4. The XGBoost model predicts the class.
5. The application displays:

   * Predicted class
   * Actual class
   * Whether the prediction was correct

## Future Improvements

* User authentication
* Prediction history database
* Analytics dashboard
* Batch predictions
* Model monitoring
* Additional ML model comparisons

