# 🫀 CardioLens

> **Interpretable heart-disease risk prediction** — a production-deployed, full-stack ML platform that turns 13 clinical features into an explainable risk tier in real time.

[![Live Demo](https://img.shields.io/badge/Live-cardiolens365.vercel.app-8b5cf6?style=flat-square&logo=vercel)](https://cardiolens365.vercel.app)
[![API](https://img.shields.io/badge/API-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://cardiolens-api-r1q7.onrender.com/health)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**Live App:** [cardiolens365.vercel.app](https://cardiolens365.vercel.app) · **API:** [cardiolens-api-r1q7.onrender.com](https://cardiolens-api-r1q7.onrender.com)

---

## ✨ Why CardioLens

Most ML demos stop at a notebook. CardioLens ships the whole loop:

**clean data → trained model → interpretable API → production UI → CI/CD**

Every prediction returns not just a score, but the **clinical drivers behind it** — the features that pushed the patient toward or away from risk — so the model is a decision-support tool, not a black box.

---

## 📊 Model Performance

| Metric | Value |
| :-- | :-- |
| **Algorithm** | Logistic Regression (scikit-learn) |
| **Accuracy** | **85.25%** |
| **F1 Score** | **0.8364** |
| **Features** | 13 clinical indicators (age, BP, cholesterol, chest pain, ECG, …) |
| **Model version** | 2.0 — label convention corrected (`target=1` = disease present) |

> **Bug fix worth noting:** the source dataset's target convention was inverted (class labels meant the opposite of what they appeared to). CardioLens documents and corrects this — a real-world example of why you verify your ground truth before shipping.

---

## 🏗️ Architecture

```
┌────────────────────┐        ┌─────────────────────┐        ┌──────────────────┐
│  React 19 + TS SPA │  REST  │   FastAPI (Docker)   │  joblib│  Logistic Reg.   │
│  Vercel            │ ─────► │   Render             │ ─────► │  + Preprocessor  │
│  /assess /insights │  JSON  │   /api/predict       │        │  .pkl / .joblib  │
└────────────────────┘        └─────────────────────┘        └──────────────────┘
      typed client                  CORS allow-list              trained in
      (axios)                       health checks                notebooks/
```

- **Frontend never touches the model** — everything goes through `/api/*`, so model, preprocessing, or UI can evolve independently.
- **Interpretability layer** ranks feature contributions from logistic coefficients → top drivers per prediction (e.g. *Oldpeak, Major Vessels, Exercise Angina*).
- **Prediction history** logged server-side and surfaced as a live dashboard with totals, high-risk counts, and recent runs.

---

## 🛠️ Tech Stack

| Layer | Tools |
| :-- | :-- |
| **ML / Data** | scikit-learn, pandas, NumPy, joblib |
| **API** | FastAPI, Pydantic, Uvicorn |
| **Frontend** | React 19, TypeScript, Vite, Tailwind CSS v4, Framer Motion, Recharts |
| **Infra** | Docker, Render (API), Vercel (SPA), GitHub Actions (CI) |

---

## ✅ Features

- **Real-time risk assessment** — 13-feature form → probability, risk tier (`low` / `moderate` / `high`), timestamped result
- **Explainable drivers** — top 6 feature contributions ranked per prediction
- **Insights dashboard** — prediction history, high-risk counts, average probability
- **Multi-page SPA** — Home / Assess / Insights / About, with dark ("Night Signal") & light ("Day Clinic") themes
- **Production API** — Pydantic-validated input, health checks, metrics endpoint, CSV export
- **Hardened deploy** — CORS locked to env-var allow-list, Dockerized, path-scoped CI, keep-alive cron

---

## 📁 Project Structure

```
cardiolens/
├── notebooks/                  EDA → training → evaluation (reproducible pipeline)
├── backend/
│   ├── main.py                 FastAPI app (all /api/* routes)
│   ├── models/                 trained .pkl artifacts
│   ├── data/processed/         preprocessor.joblib + processed CSVs
│   ├── reports/                metrics.json, prediction_logs.csv
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/                typed axios client (single source of truth)
│   │   ├── pages/              Home, Assess, Insights, About
│   │   ├── components/         form / results / history / layout / interaction
│   │   ├── context/            ThemeContext (dark/light)
│   │   └── hooks/              usePrediction, useDashboardData
│   ├── vercel.json
│   └── netlify.toml
├── docs/                       architecture.md, design.md
└── docker-compose.yml          one-command local full stack
```

---

## 🚀 Quick Start

**Option A — Docker Compose (recommended)**
```bash
docker compose up
# API  → http://localhost:8000
# App  → http://localhost:5173
```

**Option B — manual**
```bash
# Terminal 1 — backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Terminal 2 — frontend
cd frontend
npm install
npm run dev
```
Vite proxies `/api` → `localhost:8000` in dev — no `.env` needed locally.

---

## ☁️ Deployment

| Service | Platform | Config |
| :-- | :-- | :-- |
| **API** | Render | `render.yaml` (blueprint) + `backend/Dockerfile` |
| **SPA** | Vercel | `frontend/vercel.json`, env `VITE_API_URL` |
| **CI** | GitHub Actions | `.github/workflows/ci.yml` — Docker build, artifact checks, lint, build |

**Production env vars**

| Var | Where | Example |
| :-- | :-- | :-- |
| `ALLOWED_ORIGINS` | Render | `https://cardiolens365.vercel.app` |
| `VITE_API_URL` | Vercel | `https://cardiolens-api-r1q7.onrender.com` |

---

## 🔭 Roadmap

- [ ] Postgres-backed prediction history (replace CSV log)
- [ ] JWT / API-key auth on `/api/predict`
- [ ] SHAP values for per-patient contribution plots
- [ ] Model retraining pipeline on new clinical data

---

<p align="center">
  <sub>Built with FastAPI · scikit-learn · React — deployed end to end.</sub>
</p>
