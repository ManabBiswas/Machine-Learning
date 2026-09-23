# CardioLens

Interpretable heart disease risk prediction. A logistic regression model
(scikit-learn) served through a FastAPI backend, with a React + TypeScript
frontend.

## Architecture

```
cardiolens/
├── notebooks/       EDA, training, evaluation — not part of the deployed app
├── backend/         FastAPI service — wraps the existing model + preprocessor
│   ├── main.py
│   ├── models/               (your trained .pkl)
│   ├── data/processed/       (preprocessor.joblib)
│   ├── reports/               metrics.json, prediction_logs.csv
│   └── Dockerfile
└── frontend/         React (Vite) + TypeScript + Tailwind v4 + Framer Motion
    ├── src/
    │   ├── api/               typed API client (single source of truth for backend calls)
    │   ├── components/        layout / form / results / history — grouped by feature
    │   ├── context/           ThemeContext (dark/light)
    │   ├── hooks/              usePrediction, useDashboardData
    │   └── types/              shared PatientInput / PredictionResponse types
    └── vercel.json
```

The frontend never touches the model directly — everything goes through
`/api/*`, so backend, model, or preprocessing logic can change without
touching UI code, and vice versa.

## Local development

**Docker Compose (both services)**
```bash
docker compose up
```
Backend on `http://localhost:8000`, frontend on `http://localhost:5173`.

**Backend**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```
Vite proxies `/api` → `http://localhost:8000` in dev, so no `.env` is needed locally.

## Deployment (free-tier friendly)

Repo-root `render.yaml` + `backend/Dockerfile` cover the API;
`frontend/vercel.json` (Vercel) and `frontend/netlify.toml` (Netlify)
cover the SPA.

**Backend → Render (blueprint)**
1. Push the repo, then on render.com: **New → Blueprint**, pick the repo.
   Render reads `render.yaml` at the root and builds `backend/` via Docker.
2. Note the URL, e.g. `https://cardiolens-api.onrender.com`.

**Backend → Railway (manual)**
1. New project → deploy from repo, set **root directory** to
   `ML_Project_7 (A)/cardiolens/backend` (Dockerfile is auto-detected).
2. Note the generated URL.

**Frontend → Vercel**
1. Import the repo, root dir = `ML_Project_7 (A)/cardiolens/frontend`.
2. Build command `npm run build`, output dir `dist`.
3. Set env var `VITE_API_URL` to the backend URL (no trailing slash).
4. Deploy — `vercel.json` handles SPA routing.

**Frontend → Netlify**
1. Import the repo, base directory = `ML_Project_7 (A)/cardiolens/frontend`.
2. `netlify.toml` sets build command, publish dir, and SPA redirects.
3. Set env var `VITE_API_URL` the same way.

**CI:** `.github/workflows/ci.yml` builds the Docker image, imports the
API, and runs `npm run lint` + `npm run build` on every push/PR.

Scaling later: swap `prediction_logs.csv` for a real DB (Postgres on the
same host), and add JWT/API-key auth on `/api/predict` if this stops being
a demo — the API layer is already isolated so neither change touches the UI.
