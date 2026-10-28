"""FastAPI backend for the GF Mood Predictor React app.

Run from the project root:
    uvicorn api:app --reload --port 8000

Docs: http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from mood import predict_mood

app = FastAPI(title="GF Mood Predictor API", version="1.0.0")

# allow the vite dev server (and anything local) to call the API directly too
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/predict")
def predict(request: PredictRequest) -> dict:
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=422, detail="text must not be empty")
    return predict_mood(text)
