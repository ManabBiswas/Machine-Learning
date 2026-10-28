"""Shared backend for the GF Mood Predictor UI.

The ML pipeline (TF-IDF vectorizer + Random Forest) is trained and pickled by
``notebooks/nlp.ipynb``; this module loads the artifacts, applies the exact
same text-cleaning pipeline the model saw during training, and predicts.

Pure python (no streamlit import) so both the UI and smoke tests can use it.
"""

from __future__ import annotations

import pickle
import re
import string
from functools import lru_cache
from pathlib import Path

import emoji
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

ROOT = Path(__file__).resolve().parent
MODEL_DIR = ROOT / "models"

# funny verdict for every emotion the dataset knows
MOOD_ADVICE = {
    "joy": {
        "emoji": "😄",
        "status": "Green flag",
        "tip": "All is well - do not overthink it. Snacks and normal conversation are safe.",
    },
    "love": {
        "emoji": "💘",
        "status": "Maximum safety",
        "tip": "She likes you. Today at least. Reciprocate and ruin nothing.",
    },
    "sadness": {
        "emoji": "🥺",
        "status": "Hugs required",
        "tip": "'fine' never actually means fine. Listen first, do not try to fix.",
    },
    "anger": {
        "emoji": "😤",
        "status": "DEFCON 3",
        "tip": "NEVER say 'calm down'. Apologise - for something, anything, ideally in advance.",
    },
    "fear": {
        "emoji": "😨",
        "status": "Safety check",
        "tip": "Something is scaring her. Comfort mode ON, bad jokes OFF.",
    },
    "surprise": {
        "emoji": "😲",
        "status": "Investigate",
        "tip": "She found out about SOMETHING. Review your recent history, carefully.",
    },
}
NEUTRAL_ADVICE = {"emoji": "🤔", "status": "Unknown vibes", "tip": "Unknown mood - the ancient technique applies: just ask her."}


def ensure_nltk() -> None:
    """Download punkt / stopwords silently if they are missing."""
    for folder, pkg in (("tokenizers", "punkt"), ("tokenizers", "punkt_tab"), ("corpora", "stopwords")):
        try:
            nltk.data.find(f"{folder}/{pkg}")
        except LookupError:
            nltk.download(pkg, quiet=True)


ensure_nltk()


@lru_cache(maxsize=1)
def stop_words() -> frozenset[str]:
    return frozenset(stopwords.words("english"))


def preprocess(text: str) -> str:
    """Byte-for-byte the same cleaning order the training data got.

    lowercase -> punctuation -> digits -> urls -> ascii filter -> emoji lib -> stopwords
    (source: notebooks/nlp.ipynb, 'Text cleaning' section)
    """
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = text.translate(str.maketrans("", "", string.digits))
    text = re.sub(r"http\S+|www\S+", "", text)
    text = "".join(char for char in text if char.isascii())
    text = "".join(char for char in text if char not in emoji.EMOJI_DATA)
    tokens = word_tokenize(text)
    return " ".join(word for word in tokens if word not in stop_words()).strip()


@lru_cache(maxsize=1)
def load_pipeline() -> tuple:
    """Load (vectorizer, model, {class_no -> emotion_name}) from the pickled artifacts."""
    path = MODEL_DIR / "emotion_pipeline.pkl"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found - run notebooks/nlp.ipynb (Run All) first, it saves the model."
        )
    with open(path, "rb") as fh:
        artifacts = pickle.load(fh)

    vectorizer = artifacts["vectorizer"]
    model = artifacts["model"]
    name_by_no = {no: name for name, no in artifacts["emotion_names"].items()}
    return vectorizer, model, name_by_no


def predict_mood(text: str) -> dict[str, object]:
    """Predict the mood of `text`; returns verdict + probability of every emotion."""
    vectorizer, model, name_by_no = load_pipeline()

    cleaned = preprocess(text)
    vectors = vectorizer.transform([cleaned])
    probabilities: list[float] = list(model.predict_proba(vectors)[0])
    classes = [int(c) for c in model.classes_]

    ranked = sorted(
        ((name_by_no.get(no, "unknown"), prob) for no, prob in zip(classes, probabilities)),
        key=lambda pair: -pair[1],
    )
    top_name, top_prob = ranked[0]
    advice = MOOD_ADVICE.get(top_name, NEUTRAL_ADVICE)
    return {
        "emotion": top_name,
        "confidence": top_prob,
        "probabilities": ranked,          # [(name, prob), ...] best first
        "emoji": advice["emoji"],
        "status": advice["status"],
        "tip": advice["tip"],
        "processed": cleaned,
    }


if __name__ == "__main__":
    for sample in ("i am fine.", "watch out that dog might bite", "i baked your favorite cookies"):
        result = predict_mood(sample)
        print(f"{sample!r:38s} -> {result['emoji']} {result['emotion']} ({result['confidence']:.0%})")
