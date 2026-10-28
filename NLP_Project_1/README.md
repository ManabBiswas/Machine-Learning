# NLP Project 1 - Emotion Detection

Emotion classification on the Kaggle *"Emotion"* dataset: **16,000** labelled sentences, 6 emotions
(sadness, anger, love, surprise, fear, joy), plus 2,000 unseen test sentences.

## Pipeline (`notebooks/nlp.ipynb`)

1. **Load** `data/raw/train.txt` (`text;emotion` csv)
2. **Clean** - lowercase, strip punctuation / digits / urls / emojis, remove stopwords
3. **Vectorize** - one-hot encoding, bag of words, TF-IDF (demo on a toy corpus + applied to the dataset)
4. **Model** - Multinomial Naive Bayes vs Random Forest, confusion matrix, vectorizer comparison
5. **Evaluate** - final model scored on unseen `data/raw/db.txt` (2000 rows)
6. **Save** - vectorizer + model pickled to `models/emotion_pipeline.pkl`, with `predict_emotion()` for real-time use

## Results

| Model | Validation accuracy | Unseen test accuracy |
|---|---|---|
| Naive Bayes + one-hot (binary) | 0.8253 | - |
| Naive Bayes + bag of words | 0.8234 | - |
| Naive Bayes + TF-IDF | 0.7156 | - |
| **Random Forest + TF-IDF (final model)** | **0.8919** | **0.8895** |

## Outputs

- `data/processed/train_cleaned.csv` - cleaned text + numeric labels
- `models/emotion_pipeline.pkl` - fitted TF-IDF vectorizer + Random Forest (predict with `predict_emotion()` in the notebook)

## Run

```bash
cd notebooks
jupyter notebook nlp.ipynb  # Run All
```

Requires: `pandas, numpy, matplotlib, seaborn, scikit-learn, nltk, emoji`
(punk/punkt_tab/stopwords download on first run).
