# NLP Project 1 - Emotion Detection & GF Mood Predictor

Emotion classification on the Kaggle *"Emotion"* dataset: **16,000** labelled sentences, 6 emotions
(sadness, anger, love, surprise, fear, joy), plus 2,000 unseen test sentences - wrapped in a
**React + FastAPI** UI that turns any sentence into a **Girlfriend Mood prediction** (100% entertainment).

## Project structure

```
NLP_Project_1/
├── data/
│   ├── raw/                  train.txt (16k rows) + db.txt (2k unseen test rows)
│   └── processed/            train_cleaned.csv          <- notebook output
├── models/
│   └── emotion_pipeline.pkl  fitted TF-IDF vectorizer + Random Forest
├── notebooks/
│   └── nlp.ipynb             full pipeline, all cells executed
├── mood.py                   shared ML backend: artifact loading, cleaning, funny verdicts
├── api.py                    FastAPI backend (POST /api/predict)
├── frontend/                 React (Vite) UI - GF Mood Predictor
│   └── src/App.jsx           input, sample chips, verdict, probability bars
└── README.md
```

## Pipeline (`notebooks/nlp.ipynb`)

1. **Load** `data/raw/train.txt` (`text;emotion` csv)
2. **Clean** - lowercase, strip punctuation / digits / urls / emojis, remove stopwords
3. **Feature Extraction & Vectorization** - each section follows the same pattern:
   *a) manual demo on a tiny corpus -> b) with sklearn -> c) on the emotion dataset*
   - 1. One Hot Encoding (incl. one-hot for the target labels)
   - 2. Bag of Words (`CountVectorizer`)
   - 3. TF-IDF (manual TF x IDF walkthrough + `TfidfVectorizer` + lowest-IDF insight)
4. **Model Building** - Naive Bayes vs Random Forest on TF-IDF, confusion matrix,
   and a comparison of all three encodings with the same classifier
5. **Final Model** - refit on all data, saved to `models/emotion_pipeline.pkl`,
   with `predict_emotion()` for real-time use
6. **Evaluate** - final model scored on unseen `data/raw/db.txt` (2,000 rows)

## Results

| Model | Validation accuracy | Unseen test accuracy |
|---|---|---|
| Naive Bayes + one-hot (binary) | 0.8253 | - |
| Naive Bayes + bag of words | 0.8234 | - |
| Naive Bayes + TF-IDF | 0.7156 | - |
| **Random Forest + TF-IDF (final model)** | **0.8919** | **0.8895** |

## GF Mood Predictor (React app)

Two terminals from the project root:

```bash
# 1. ML API (FastAPI, docs at http://127.0.0.1:8000/docs)
uvicorn api:app --reload --port 8000

# 2. React UI (Vite dev server, proxies /api to port 8000)
cd frontend
npm install        # first time only
npm run dev        # http://localhost:5173
```

What it does:

- Paste *what she said* -> the app cleans it with the exact training pipeline
  (`mood.py`), predicts the emotion + probability over all 6 classes
- Funny verdict card + survival tip + confidence meter + per-emotion probability bars
- One-click sample chips, including the classic *"i am fine."*
- Low-confidence fallback: *"vibes unclear — just ask her"*
- Shows exactly what text the model saw after cleaning
- Production build: `cd frontend && npm run build` -> static files in `frontend/dist`
  (point any static server at it and keep the API running)

Disclaimer: predicts the emotion of the TEXT (16k Kaggle dataset), not her actual
mood. Real girlfriend > model.

## Outputs

- raw data -> `data/raw/train.txt` (16000 rows) and `data/raw/db.txt` (2000 unseen test rows)
- cleaned data -> `data/processed/train_cleaned.csv`
- fitted vectorizer + model -> `models/emotion_pipeline.pkl`
- the app cleans raw text with the exact training pipeline before predicting

## Run / Requirements

Python 3.10+ (tested on 3.14) with:
`pandas, numpy, matplotlib, seaborn, scikit-learn, nltk, emoji, fastapi, uvicorn`
(nltk punkt / punkt_tab / stopwords download on first run) - plus **Node 18+** for the frontend.

- Notebook: `cd notebooks && jupyter notebook nlp.ipynb` -> Run All (re-pickles the model)
- API: `uvicorn api:app --reload --port 8000`
- UI: `cd frontend && npm run dev` -> http://localhost:5173
