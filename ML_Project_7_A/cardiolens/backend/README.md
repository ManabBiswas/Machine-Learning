---
title: CardioLens API
emoji: "🫀"
colorFrom: red
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# CardioLens API

FastAPI backend for interpretable heart-disease risk prediction (logistic regression + preprocessor).

Endpoints: `/health`, `/api/health`, `/api/metrics`, `/api/example-patient`, `/api/predict`, `/api/history`.

Set `ALLOWED_ORIGINS` in Space Settings to a comma-separated list of frontend origins, e.g. `https://cardiolens365.vercel.app`.
