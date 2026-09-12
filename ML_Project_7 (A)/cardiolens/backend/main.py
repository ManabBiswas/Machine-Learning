"""
CardioLens API — FastAPI service wrapping the existing scikit-learn
logistic regression model + preprocessor. No retraining; this is a
straight port of the prediction logic that used to live in the
Streamlit app, exposed as a JSON API for the React frontend.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "logistic_regression_model.pkl"
PREPROCESSOR_PATH = BASE_DIR / "data" / "processed" / "preprocessor.joblib"
REPORTS_DIR = BASE_DIR / "reports"
LOG_FILE = REPORTS_DIR / "prediction_logs.csv"
METRICS_FILE = REPORTS_DIR / "metrics.json"

FEATURE_COLUMNS = [
    "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
    "thalach", "exang", "oldpeak", "slope", "ca", "thal",
]

FRIENDLY = {
    "age": "Age", "sex": "Sex", "cp": "Chest Pain", "trestbps": "Resting BP",
    "chol": "Cholesterol", "fbs": "Fasting Sugar", "restecg": "Resting ECG",
    "thalach": "Max Heart Rate", "exang": "Exercise Angina", "oldpeak": "Oldpeak",
    "slope": "ST Slope", "ca": "Major Vessels", "thal": "Thalassemia",
}

EXAMPLE_PATIENT = {
    "age": 57, "sex": 1, "cp": 2, "trestbps": 140, "chol": 289, "fbs": 0,
    "restecg": 0, "thalach": 122, "exang": 1, "oldpeak": 3.2, "slope": 1,
    "ca": 2, "thal": 2,
}

app = FastAPI(title="CardioLens API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only — tighten to your deployed frontend origin in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

_model = None
_preprocessor = None


def get_model():
    global _model, _preprocessor
    if _model is None:
        if not MODEL_PATH.exists() or not PREPROCESSOR_PATH.exists():
            raise HTTPException(status_code=503, detail="Model artifacts not found on server.")
        _model = joblib.load(MODEL_PATH)
        _preprocessor = joblib.load(PREPROCESSOR_PATH)
    return _model, _preprocessor


class PatientInput(BaseModel):
    age: int = Field(ge=18, le=100)
    sex: Literal[0, 1]
    cp: Literal[0, 1, 2, 3]
    trestbps: int = Field(ge=80, le=220)
    chol: int = Field(ge=100, le=600)
    fbs: Literal[0, 1]
    restecg: Literal[0, 1, 2]
    thalach: int = Field(ge=60, le=220)
    exang: Literal[0, 1]
    oldpeak: float = Field(ge=0.0, le=7.0)
    slope: Literal[0, 1, 2]
    ca: Literal[0, 1, 2, 3]
    thal: Literal[0, 1, 2, 3]


class Driver(BaseModel):
    feature: str
    label: str
    value: float


class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    risk_tier: Literal["low", "moderate", "high"]
    drivers: list[Driver]
    timestamp: str


def tier_of(probability: float) -> str:
    if probability >= 0.65:
        return "high"
    if probability >= 0.35:
        return "moderate"
    return "low"


def feature_contributions(transformed, model, preprocessor) -> list[Driver]:
    try:
        names = [n.split("__", 1)[1] for n in preprocessor.get_feature_names_out()]
    except Exception:
        names = [f"f{i}" for i in range(transformed.shape[1])]
    if len(names) != transformed.shape[1]:
        names = names[: transformed.shape[1]]
    coefs = model.coef_[0]
    contrib = pd.Series(transformed[0] * coefs, index=names)
    grouped: dict[str, float] = {}
    for name, value in contrib.items():
        parent = name.split("_")[0]
        grouped[parent] = grouped.get(parent, 0.0) + float(value)
    ranked = sorted(grouped.items(), key=lambda kv: abs(kv[1]), reverse=True)
    return [
        Driver(feature=k, label=FRIENDLY.get(k, k), value=round(v, 4))
        for k, v in ranked[:6]
    ]


def log_prediction(patient: dict, prediction: int, probability: float):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        **{k: patient[k] for k in FEATURE_COLUMNS},
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "prediction": prediction,
        "probability": round(probability, 4),
        "risk_label": "High Risk" if prediction == 1 else "Low Risk",
    }
    if LOG_FILE.exists():
        df = pd.read_csv(LOG_FILE)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    else:
        df = pd.DataFrame([record])
    df.to_csv(LOG_FILE, index=False)


@app.get("/api/health")
def health():
    ok = MODEL_PATH.exists() and PREPROCESSOR_PATH.exists()
    return {"status": "ok" if ok else "model_missing"}


@app.get("/api/metrics")
def metrics():
    defaults = {"model": "Logistic Regression", "model_version": "1.0", "accuracy": 0.836, "f1": 0.848}
    if METRICS_FILE.exists():
        try:
            return {**defaults, **json.loads(METRICS_FILE.read_text())}
        except (json.JSONDecodeError, OSError):
            return defaults
    return defaults


@app.get("/api/example-patient")
def example_patient():
    return EXAMPLE_PATIENT


@app.post("/api/predict", response_model=PredictionResponse)
def predict(patient: PatientInput):
    model, preprocessor = get_model()
    data = patient.model_dump()
    input_df = pd.DataFrame([data], columns=FEATURE_COLUMNS)
    transformed = preprocessor.transform(input_df)
    prediction = int(model.predict(transformed)[0])
    probability = float(model.predict_proba(transformed)[0][1])
    drivers = feature_contributions(transformed, model, preprocessor)
    log_prediction(data, prediction, probability)
    return PredictionResponse(
        prediction=prediction,
        probability=round(probability, 4),
        risk_tier=tier_of(probability),
        drivers=drivers,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


@app.get("/api/history")
def history(limit: int = 8):
    if not LOG_FILE.exists():
        return {"total": 0, "high_risk": 0, "avg_risk": 0.0, "recent": []}
    logs = pd.read_csv(LOG_FILE)
    if logs.empty:
        return {"total": 0, "high_risk": 0, "avg_risk": 0.0, "recent": []}
    total = len(logs)
    high = int((logs["prediction"] == 1).sum())
    avg = float(logs["probability"].mean())
    recent = logs.tail(limit).iloc[::-1]
    rows = [
        {
            "timestamp": r["timestamp"],
            "age": int(r["age"]),
            "sex": "M" if r["sex"] == 1 else "F",
            "max_hr": int(r["thalach"]),
            "probability": round(float(r["probability"]), 4),
            "risk_label": r["risk_label"],
        }
        for _, r in recent.iterrows()
    ]
    return {"total": total, "high_risk": high, "avg_risk": round(avg, 4), "recent": rows}


@app.get("/api/history/export")
def export_history():
    if not LOG_FILE.exists():
        raise HTTPException(status_code=404, detail="No history yet.")
    return {"csv": LOG_FILE.read_text()}
