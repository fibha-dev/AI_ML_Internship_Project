# Credit Card Fraud Detection (Full Stack ML App)

A full-stack machine learning web app that detects fraudulent credit card transactions using a Logistic Regression model.

## Live Links

-  Frontend: https://ai-ml-internship-project.vercel.app  
-  Backend API: https://aimlinternshipproject-production.up.railway.app/docs  

## Problem Statement

Predict whether a transaction is:
- **0 → Normal**
- **1 → Fraud**

Input: 30 numerical features (Time, Amount, V1–V28)

## Tech Stack

**Frontend:** React, Axios  
**Backend:** FastAPI, Scikit-learn, NumPy  
**Deployment:** Vercel (Frontend), Railway (Backend), Docker  

## Architecture

Frontend (React)
→ FastAPI Backend
→ ML Model (Logistic Regression)
→ Prediction Response

## API

### POST `/predict`

**Request:**
```json
{
  "features": [30 numbers]
}

Response:

{
  "prediction": 0,
  "result": "Normal"
}


 How It Works
User enters 30 values
React sends request to API
Backend processes input
ML model predicts result
Output shown as SAFE or FRAUD


 Features
Real-time fraud detection
Cloud-deployed ML model
Full-stack integration
REST API communication


 Future Improvements
Authentication system
Database logging
Better UI dashboard
Advanced ML models