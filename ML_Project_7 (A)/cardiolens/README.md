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

**Backend → Render or Railway**
1. Push `backend/` to a repo (or connect this repo, root dir = `backend`).
2. Render/Railway auto-detects the `Dockerfile`, or run
   `uvicorn main:app --host 0.0.0.0 --port $PORT` directly.
3. Note the deployed URL, e.g. `https://cardiolens-api.onrender.com`.

**Frontend → Vercel or Netlify**
1. Import the repo, root dir = `frontend`.
2. Build command `npm run build`, output dir `dist`.
3. Set env var `VITE_API_URL` to your backend URL from above.
4. Deploy — `vercel.json` handles SPA routing.

Scaling later: swap `prediction_logs.csv` for a real DB (Postgres on the
same host), and add JWT/API-key auth on `/api/predict` if this stops being
a demo — the API layer is already isolated so neither change touches the UI.
