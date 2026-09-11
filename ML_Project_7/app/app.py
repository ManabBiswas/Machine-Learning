import json
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "logistic_regression_model.pkl"
PREPROCESSOR_PATH = BASE_DIR / "data" / "processed" / "preprocessor.joblib"
REPORTS_DIR = BASE_DIR / "reports"
LOG_FILE = REPORTS_DIR / "prediction_logs.csv"
METRICS_FILE = REPORTS_DIR / "metrics.json"
STYLES_PATH = Path(__file__).resolve().parent / "styles.css"
FAVICON_PATH = Path(__file__).resolve().parent / "heart.png"

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

CP_LABELS = {"0": "0 — Typical Angina", "1": "1 — Atypical Angina",
             "2": "2 — Non-anginal Pain", "3": "3 — Asymptomatic"}
RESTEcg_LABELS = {"0": "0 — Normal", "1": "1 — ST-T Abnormality", "2": "2 — LV Hypertrophy"}
SLOPE_LABELS = {"0": "0 — Upsloping", "1": "1 — Flat", "2": "2 — Downsloping"}
THAL_LABELS = {"0": "0 — None", "1": "1 — Fixed Defect", "2": "2 — Normal", "3": "3 — Reversible Defect"}


def _binary(x, no: str, yes: str) -> str:
    s = str(x)
    if s in (no, yes):
        return s
    return yes if s == "1" else no


def _label(x, table: dict) -> str:
    s = str(x)
    return table.get(s, s if s in table.values() else s)

st.set_page_config(page_title="CardioLens — Heart Disease Predictor",
                  page_icon=str(FAVICON_PATH), layout="wide")


# ---------------- THEME ----------------
def theme_vars() -> str:
    if st.session_state.get("theme") == "light":
        return """
        :root {
            --bg1: #eef3fa;
            --panel: rgba(255,255,255,0.72);
            --panel-strong: rgba(255,255,255,0.9);
            --field: #ffffff;
            --field-text: #0f172a;
            --popover: #ffffff;
            --line: rgba(148,163,184,0.25);
            --line-strong: rgba(148,163,184,0.45);
            --track: rgba(148,163,184,0.25);
            --zero-line: rgba(148,163,184,0.6);
            --text: #0f172a;
            --muted: #5b6b83;
            --chip: rgba(255,255,255,0.65);
            --chip-accent: rgba(37,99,235,0.1);
            --accent: #2563eb; --accent2: #7c3aed;
            --grad-a: #1d4ed8; --grad-b: #4f46e5; --grad-c: #0ea5e9;
            --accent-line: rgba(37,99,235,0.6);
            --accent-glow: rgba(37,99,235,0.2);
            --focus-glow: rgba(59,130,246,0.15);
            --success: #16a34a; --success-soft: #dcfce7; --success-line: #bbf7d0;
            --danger: #dc2626; --danger-soft: #fee2e2; --danger-line: #fecaca;
            --warning: #b45309; --warning-soft: #fef3c7; --warning-line: #fde68a;
            --bar-pos-a: #f87171; --bar-pos-b: #dc2626;
            --bar-neg-a: #4ade80; --bar-neg-b: #16a34a;
            --orb1: rgba(125,211,252,0.5); --orb2: rgba(196,181,253,0.5);
            --orb3: rgba(147,197,253,0.45); --orb1-pos: 6% 8%;
            --pulse: rgba(22,163,74,0.5);
            --shadow: 0 18px 42px rgba(15,23,42,0.09);
            --shadow-hover: 0 24px 48px rgba(15,23,42,0.14);
        }
        """
    return """
    :root {
        --bg1: #0B1220;
        --panel: rgba(17,27,45,0.66);
        --panel-strong: rgba(15,23,42,0.86);
        --field: #0d1628;
        --field-text: #e6edf7;
        --popover: #101c30;
        --line: rgba(99,128,180,0.22);
        --line-strong: rgba(99,128,180,0.4);
        --track: rgba(99,128,180,0.22);
        --zero-line: rgba(99,128,180,0.5);
        --text: #eef3fa;
        --muted: #94a8c4;
        --chip: rgba(23,37,58,0.7);
        --chip-accent: rgba(96,165,250,0.14);
        --accent: #3b82f6; --accent2: #8b5cf6;
        --grad-a: #60a5fa; --grad-b: #a78bfa; --grad-c: #22d3ee;
        --accent-line: rgba(96,165,250,0.5);
        --accent-glow: rgba(59,130,246,0.28);
        --focus-glow: rgba(59,130,246,0.2);
        --success: #34d399; --success-soft: rgba(52,211,153,0.12); --success-line: rgba(52,211,153,0.35);
        --danger: #f87171; --danger-soft: rgba(248,113,113,0.12); --danger-line: rgba(248,113,113,0.35);
        --warning: #fbbf24; --warning-soft: rgba(251,191,36,0.12); --warning-line: rgba(251,191,36,0.35);
        --bar-pos-a: #fb923c; --bar-pos-b: #ef4444;
        --bar-neg-a: #22d3ee; --bar-neg-b: #10b981;
        --orb1: rgba(59,130,246,0.5); --orb2: rgba(139,92,246,0.45);
        --orb3: rgba(34,211,238,0.32); --orb1-pos: 8% 10%;
        --pulse: rgba(52,211,153,0.55);
        --shadow: 0 20px 48px rgba(2,6,17,0.5);
        --shadow-hover: 0 26px 54px rgba(2,6,17,0.62);
    }
    """


def inject_base_style():
    """Inject theme variables + stylesheet via st.html (CSS-only content is
    routed to the event container by Streamlit, so it takes no layout space
    and <style> tags are preserved)."""
    css = theme_vars() + "\n" + STYLES_PATH.read_text(encoding="utf-8")
    st.html(f"<style>{css}</style>")


# ---------------- MODEL ----------------
@st.cache_resource(show_spinner=False)
def load_model_and_preprocessor():
    if not MODEL_PATH.exists() or not PREPROCESSOR_PATH.exists():
        return None, None
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    return model, preprocessor


def load_metrics() -> dict:
    defaults = {"model": "Logistic Regression", "model_version": "1.0",
                "accuracy": 0.836, "f1": 0.848}
    if METRICS_FILE.exists():
        try:
            return {**defaults, **json.loads(METRICS_FILE.read_text())}
        except (json.JSONDecodeError, OSError):
            return defaults
    return defaults


def log_prediction(patient_data: dict, prediction: int, probability: float):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    record = {**{k: patient_data[k] for k in FEATURE_COLUMNS},
              "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              "prediction": prediction,
              "probability": round(probability, 4),
              "risk_label": "High Risk" if prediction == 1 else "Low Risk"}
    if LOG_FILE.exists():
        df = pd.read_csv(LOG_FILE)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    else:
        df = pd.DataFrame([record])
    df.to_csv(LOG_FILE, index=False)


def predict_heart_disease(patient_data: dict):
    model, preprocessor = load_model_and_preprocessor()
    input_df = pd.DataFrame([patient_data], columns=FEATURE_COLUMNS)
    transformed = preprocessor.transform(input_df)
    prediction = int(model.predict(transformed)[0])
    probability = float(model.predict_proba(transformed)[0][1])
    return prediction, probability, transformed


def feature_contributions(patient: dict, transformed) -> list[tuple[str, float]]:
    """Per-patient signed LogReg contributions grouped back to 13 parent features."""
    model, preprocessor = load_model_and_preprocessor()
    try:
        names = [n.split("__", 1)[1] for n in preprocessor.get_feature_names_out()]
    except Exception:
        names = [f"f{i}" for i in range(transformed.shape[1])]
    if len(names) != transformed.shape[1]:
        names = names[: transformed.shape[1]]
    coefs = model.coef_[0]
    contrib = pd.Series(transformed[0] * coefs, index=names)
    grouped = {}
    for name, value in contrib.items():
        parent = name.split("_")[0]
        grouped[parent] = grouped.get(parent, 0.0) + float(value)
    ranked = sorted(grouped.items(), key=lambda kv: abs(kv[1]), reverse=True)
    return ranked


def group_scale(contribs: list[tuple[str, float]]) -> dict[str, float]:
    """Scale each driver to a 0-100 width for bars, preserving sign."""
    max_abs = max((abs(v) for _, v in contribs), default=1.0) or 1.0
    return {k: abs(v) / max_abs * 100 for k, v in contribs}


# ---------------- HERO ----------------
HEART_SVG = """<svg viewBox="0 0 24 24" fill="none" stroke="url(#heroHeartGrad)" stroke-width="1.8"
     stroke-linecap="round" stroke-linejoin="round" class="hero-heart-svg">
  <path d="M19.5 12.57l-7.5 7.428-7.5-7.428a5 5 0 1 1 7.5-6.566a5 5 0 1 1 7.5 6.566z"/>
</svg>"""


def render_hero(metrics: dict):
    ver = metrics.get("model_version", "1.0")
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-orb o1"></div>
            <div class="hero-orb o2"></div>
            <div class="hero-brand">
                <span class="hero-icon">{HEART_SVG}</span>
                <h1 class="hero-title">CardioLens</h1>
            </div>
            <p class="hero-subtitle">Clinical-grade heart disease risk assessment, powered by an
            explainable logistic regression model — instant, transparent, patient-specific.</p>
            <span class="hero-status">
                <span class="status-dot"></span>
                Model loaded · v{ver} · {metrics.get('feature_count', 13)} clinical features
            </span>
            <svg class="hero-ecg" viewBox="0 0 800 60" preserveAspectRatio="none" aria-hidden="true">
                <path class="ecg-line" stroke="url(#ecgGrad)"
                      d="M0,30 L80,30 L100,18 L120,42 L140,30 L200,30 L215,26 L230,30
                         L300,30 L320,10 L335,52 L350,30 L430,30 L450,20 L470,40 L490,30
                         L560,30 L580,14 L595,48 L610,30 L700,30 L720,24 L740,32 L800,30"/>
                <defs>
                    <linearGradient id="ecgGrad" x1="0" x2="1">
                        <stop offset="0" stop-color="var(--grad-a)"/>
                        <stop offset="0.5" stop-color="var(--grad-b)"/>
                        <stop offset="1" stop-color="var(--grad-c)"/>
                    </linearGradient>
                    <linearGradient id="heroHeartGrad" x1="0" y1="0" x2="1" y2="1">
                        <stop offset="0" stop-color="var(--grad-a)"/>
                        <stop offset="1" stop-color="var(--grad-c)"/>
                    </linearGradient>
                </defs>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )


def stat_card(delay: str, icon: str, label: str, value: str, hint: str) -> str:
    return f"""
    <div class="stat-card {delay}">
        <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="url(#g-{label})" stroke-width="2"
                 stroke-linecap="round" stroke-linejoin="round">{icon}</svg>
        </div>
        <div class="stat-label">{label}</div>
        <p class="stat-value">{value}</p>
        <div class="stat-hint">{hint}</div>
    </div>
    """


def render_stat_cards(metrics: dict):
    acc = metrics.get("accuracy", 0.836)
    f1 = metrics.get("f1", 0.848)
    cards = "".join([
        stat_card("d1",
                  '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
                  "Accuracy", f"{acc * 100:.1f}%", "Holdout test set"),
        stat_card("d2",
                  '<path d="M12 2a10 10 0 1 0 10 10"/><path d="M12 12l6-6"/>',
                  "F1 Score", f"{f1 * 100:.1f}%", "Balanced precision / recall"),
        stat_card("d3",
                  '<path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/>',
                  "Model", metrics.get("model", "Logistic Regression"), "Fully interpretable"),
    ])
    gradients = """
    <svg width="0" height="0" style="position:absolute">
        <defs>
            <linearGradient id="g-Accuracy" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0" stop-color="var(--accent)"/><stop offset="1" stop-color="var(--accent2)"/>
            </linearGradient>
            <linearGradient id="g-F1 Score" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0" stop-color="var(--accent2)"/><stop offset="1" stop-color="var(--grad-c)"/>
            </linearGradient>
            <linearGradient id="g-Model" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0" stop-color="var(--grad-c)"/><stop offset="1" stop-color="var(--accent)"/>
            </linearGradient>
        </defs>
    </svg>
    """
    st.markdown(gradients + f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.9rem;">{cards}</div>', unsafe_allow_html=True)


# ---------------- FORM ----------------
def build_patient_form(example: bool):
    st.markdown('<div class="section-title"><span class="bar"></span>Patient Information</div>', unsafe_allow_html=True)

    defaults = EXAMPLE_PATIENT if example else {
        "age": 52, "sex": 0, "cp": 0, "trestbps": 125, "chol": 212, "fbs": 0,
        "restecg": 0, "thalach": 168, "exang": 0, "oldpeak": 1.0, "slope": 0,
        "ca": 0, "thal": 0,
    }

    st.markdown("**Demographics**", help="Core patient profile")
    c1, c2 = st.columns(2)
    with c1:
        age = st.number_input("Age *", min_value=18, max_value=100, value=defaults["age"], help="Years (18–100)")
        sex = st.selectbox("Sex *", [0, 1], index=defaults["sex"],
                           format_func=lambda x: _binary(x, "Female", "Male"))
    with c2:
        cp = st.selectbox("Chest Pain Type *", [0, 1, 2, 3], index=defaults["cp"], format_func=lambda x: _label(x, CP_LABELS),
            help="Category 3 (asymptomatic) carries the highest risk weight")
        trestbps = st.number_input("Resting Blood Pressure *", min_value=80, max_value=220, value=defaults["trestbps"], help="mm Hg — normal < 120")

    st.markdown("**Vitals & Labs**")
    c3, c4 = st.columns(2)
    with c3:
        chol = st.number_input("Cholesterol *", min_value=100, max_value=600, value=defaults["chol"], help="mg/dl — desirable < 200")
        fbs = st.selectbox("Fasting Blood Sugar *", [0, 1], index=defaults["fbs"], format_func=lambda x: _binary(x, "≤ 120 mg/dl", "> 120 mg/dl"))
    with c4:
        restecg = st.selectbox("Resting ECG *", [0, 1, 2], index=defaults["restecg"], format_func=lambda x: _label(x, RESTEcg_LABELS))
        thalach = st.number_input("Maximum Heart Rate *", min_value=60, max_value=220, value=defaults["thalach"], help="bpm achieved during exercise")

    st.markdown("**ECG & Exercise**")
    c5, c6 = st.columns(2)
    with c5:
        exang = st.selectbox("Exercise-Induced Angina *", [0, 1], index=defaults["exang"], format_func=lambda x: _binary(x, "No", "Yes"))
        oldpeak = st.number_input("Oldpeak (ST Depression) *", min_value=0.0, max_value=7.0, value=defaults["oldpeak"], step=0.1, help="mm — induced by exercise relative to rest")
        slope = st.selectbox("ST Slope *", [0, 1, 2], index=defaults["slope"], format_func=lambda x: _label(x, SLOPE_LABELS))
    with c6:
        ca = st.selectbox("Number of Major Vessels *", [0, 1, 2, 3], index=defaults["ca"], help="Fluoroscopy-colored vessels (0–3)")
        thal = st.selectbox("Thalassemia *", [0, 1, 2, 3], index=defaults["thal"], format_func=lambda x: _label(x, THAL_LABELS),
            help="3 (reversible defect) is a strong risk marker")

    submit = st.form_submit_button("Predict Risk", use_container_width=True, type="primary")

    patient = {k: int(v) if k != "oldpeak" else float(v) for k, v in {
        "age": age, "sex": sex, "cp": cp, "trestbps": trestbps, "chol": chol,
        "fbs": fbs, "restecg": restecg, "thalach": thalach, "exang": exang,
        "oldpeak": oldpeak, "slope": slope, "ca": ca, "thal": thal}.items()}
    return patient, submit


def form_section(example: bool):
    with st.form("heart_form", border=False):
        return build_patient_form(example)


# ---------------- GAUGE (animated HTML component) ----------------
def current_theme() -> str:
    try:
        return st.session_state.get("theme", "dark")
    except Exception:
        return "dark"


def render_gauge(probability: float, tier: str) -> str:
    pct = min(max(probability, 0.0), 1.0)
    light = current_theme() == "light"
    text_col = "#0f172a" if light else "#eef3fa"
    muted_col = "#5b6b83" if light else "#94a8c4"
    color = {"high": "#ef4444", "moderate": "#f59e0b", "low": "#10b981"}[tier]
    glow = {"high": "rgba(239,68,68,0.5)", "moderate": "rgba(245,158,11,0.45)", "low": "rgba(16,185,129,0.45)"}[tier]
    label = {"high": "HIGH RISK", "moderate": "MODERATE", "low": "LOW RISK"}[tier]
    return f"""
    <style>html,body{{margin:0;background:transparent;}}</style>
    <div style="display:flex;flex-direction:column;align-items:center;font-family:'Plus Jakarta Sans',Inter,sans-serif;padding:0.4rem 0 0;">
      <div style="position:relative;width:190px;height:190px;">
        <svg width="190" height="190" viewBox="0 0 190 190">
          <circle cx="95" cy="95" r="84" fill="none" stroke="rgba(148,163,184,0.18)" stroke-width="13"/>
          <circle id="gaugeArc" cx="95" cy="95" r="84" fill="none" stroke="{color}" stroke-width="13"
                  stroke-linecap="round" transform="rotate(-90 95 95)"
                  stroke-dasharray="527.8" stroke-dashoffset="527.8"
                  style="filter:drop-shadow(0 0 10px {glow});"/>
        </svg>
        <div style="position:absolute;inset:0;display:grid;place-items:center;text-align:center;">
          <div>
            <div id="gaugeNum" style="font-size:2.5rem;font-weight:800;color:{text_col};line-height:1;font-variant-numeric:tabular-nums;">0.0%</div>
            <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.14em;color:{muted_col};margin-top:0.3rem;">PREDICTED RISK</div>
            <div style="margin-top:0.4rem;font-size:0.72rem;font-weight:800;color:{color};">{label}</div>
          </div>
        </div>
      </div>
      <script>
        (() => {{
          const arc = document.getElementById('gaugeArc');
          const num = document.getElementById('gaugeNum');
          const target = {pct * 100:.1f};
          const dur = 1400, start = performance.now();
          const ease = t => 1 - Math.pow(1 - t, 3);
          const step = now => {{
            const p = Math.min((now - start) / dur, 1);
            const eased = ease(p);
            if (arc) arc.setAttribute('stroke-dashoffset', 527.8 * (1 - {pct} * eased));
            if (num) num.textContent = (target * eased).toFixed(1) + '%';
            if (p < 1) requestAnimationFrame(step);
          }};
          requestAnimationFrame(step);
        }})();
      </script>
    </div>
    """


def tier_of(probability: float) -> str:
    if probability >= 0.65:
        return "high"
    if probability >= 0.35:
        return "moderate"
    return "low"


def render_drivers(contribs: list[tuple[str, float]]) -> str:
    if not contribs:
        return ""
    scale = group_scale(contribs)
    rows = []
    for i, (name, val) in enumerate(contribs[:6]):
        w = scale.get(name, 0)
        sign = "pos" if val > 0 else ("neg" if val < 0 else "")
        value_txt = f"+{val:.2f}" if val > 0 else f"{val:.2f}"
        rows.append(f"""
        <div class="driver" style="animation-delay:{0.1 + i * 0.08}s">
          <div class="driver-top">
            <span class="driver-name">{FRIENDLY.get(name, name)}</span>
            <span class="driver-val {sign}">{value_txt}</span>
          </div>
          <div class="driver-track">
            <div class="driver-zero"></div>
            <div class="driver-fill {sign}" style="--w:{w:.1f}%"></div>
          </div>
        </div>""")
    return f"""
    <div class="panel-head" style="margin-top:1.2rem;">
        <span class="section-title" style="font-size:0.92rem;"><span class="bar"></span>Top Risk Drivers</span>
    </div>
    <div class="drivers">{''.join(rows)}</div>
    <div class="driver-legend">
        <span><span class="dot up"></span>Increases risk</span>
        <span><span class="dot down"></span>Protective</span>
    </div>
    <div class="stat-hint" style="margin-top:0.5rem;">Signed model contribution per feature (log-odds), grouped for readability.</div>
    """


SUMMARY_FORMATS = {
    "sex": lambda v: "Male" if v == 1 else "Female",
    "cp": lambda v: CP_LABELS[str(v)].split(" — ")[1],
    "fbs": lambda v: "> 120 mg/dl" if v == 1 else "≤ 120 mg/dl",
    "restecg": lambda v: RESTEcg_LABELS[str(v)].split(" — ")[1],
    "exang": lambda v: "Yes" if v == 1 else "No",
    "slope": lambda v: SLOPE_LABELS[str(v)].split(" — ")[1],
    "thal": lambda v: THAL_LABELS[str(v)].split(" — ")[1],
    "trestbps": lambda v: f"{v} mm Hg",
    "chol": lambda v: f"{v} mg/dl",
    "thalach": lambda v: f"{v} bpm",
    "oldpeak": lambda v: f"{v} mm",
    "ca": lambda v: str(v),
    "age": lambda v: f"{v} yrs",
}


def render_summary(patient: dict) -> str:
    cells = "".join(
        f'<div class="sum-row"><span class="k">{FRIENDLY.get(k, k)}</span>'
        f'<span class="v">{SUMMARY_FORMATS.get(k, str)(v)}</span></div>'
        for k, v in patient.items())
    return f"""
    <div class="panel-head" style="margin-top:1.2rem;">
        <span class="section-title" style="font-size:0.92rem;"><span class="bar"></span>Input Summary</span>
    </div>
    <div class="summary-grid">{cells}</div>
    """


def display_result(prediction: int, probability: float, contribs: list[tuple[str, float]], patient: dict):
    tier = tier_of(probability)
    heading = {"high": "High Risk", "moderate": "Moderate Risk", "low": "Low Risk"}[tier]
    intro = {
        "high": "The model predicts significant heart disease risk. Clinical follow-up is advised.",
        "moderate": "The model predicts an intermediate risk profile worth monitoring.",
        "low": "The model predicts no major risk indicators detected.",
    }[tier]

    st.markdown(
        f"""
        <div class="result-panel">
            <div class="result-head">
                <h3 class="result-title">{heading}</h3>
                <span class="badge badge-{tier}">{probability * 100:.1f}% probability</span>
            </div>
            <p class="result-intro">{intro}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.iframe(
        render_gauge(probability, tier),
        height=260,
    )
    st.markdown(render_drivers(contribs), unsafe_allow_html=True)
    st.markdown(render_summary(patient), unsafe_allow_html=True)
    st.caption("Educational use only — not a medical diagnosis.")


EMPTY_HEART_SVG = """<svg viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="1.6"
     stroke-linecap="round" stroke-linejoin="round" style="width:64px;height:64px;">
  <path d="M19.5 12.57l-7.5 7.428-7.5-7.428a5 5 0 1 1 7.5-6.566a5 5 0 1 1 7.5 6.566z"/>
</svg>"""


def render_empty_state():
    st.markdown(
        f"""
        <div class="empty-state">
            <span class="glyph">{EMPTY_HEART_SVG}</span>
            <p><strong>Ready when you are.</strong></p>
            <p class="hint">Fill in the patient details on the left, then hit
            <strong>Predict Risk</strong> — results, gauge, and drivers appear here.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------- HISTORY ----------------
def render_history():
    if not LOG_FILE.exists():
        return
    logs = pd.read_csv(LOG_FILE)
    if logs.empty:
        return
    recent = logs.tail(8).iloc[::-1]

    total = len(logs)
    high = int((logs["prediction"] == 1).sum())
    avg = float(logs["probability"].mean())

    chips = f"""
    <div class="chips-row">
        <span class="chip"><span class="k">Predictions</span><span class="v">{total}</span></span>
        <span class="chip"><span class="k">High risk</span><span class="v">{high}</span></span>
        <span class="chip"><span class="k">Avg risk</span><span class="v">{avg * 100:.1f}%</span></span>
    </div>
    """
    rows = []
    for _, r in recent.iterrows():
        badge = "high" if r["prediction"] == 1 else "low"
        label = "High" if r["prediction"] == 1 else "Low"
        rows.append(f"""
        <tr>
            <td>{r['timestamp']}</td>
            <td>{int(r['age'])} / {'M' if r['sex'] == 1 else 'F'}</td>
            <td>{int(r['thalach'])} bpm</td>
            <td class="prob">{r['probability'] * 100:.1f}%</td>
            <td><span class="mini-badge {badge}">{label}</span></td>
        </tr>""")
    table = f"""
    <table class="log-table">
        <thead><tr><th>When</th><th>Age / Sex</th><th>Max HR</th><th>Probability</th><th>Risk</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
    </table>
    """
    st.markdown(chips + table, unsafe_allow_html=True)
    csv_bytes = logs.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download full history (CSV)",
        data=csv_bytes,
        file_name="prediction_history.csv",
        mime="text/csv",
        use_container_width=True,
    )


# ---------------- MAIN ----------------
def main():
    if "example" not in st.session_state:
        st.session_state.example = False

    model, preprocessor = load_model_and_preprocessor()
    if model is None:
        inject_base_style()
        st.markdown(
            """
            <div class="hero">
                <div class="hero-brand">
                    <h1 class="hero-title">Model artifacts missing</h1>
                </div>
                <p class="hero-subtitle">Expected <code>models/logistic_regression_model.pkl</code> and
                <code>data/processed/preprocessor.joblib</code>. Run the training notebooks first, then reload.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.stop()

    _, toggle_col = st.columns([7, 1], gap="small", vertical_alignment="center")
    with toggle_col:
        theme = st.toggle("Light mode", key="theme_toggle", label_visibility="collapsed",
                          help="Switch between dark and light themes")
    st.session_state.theme = "light" if theme else "dark"
    inject_base_style()

    metrics = load_metrics()
    render_hero(metrics)
    st.markdown('<div style="height:0.9rem;"></div>', unsafe_allow_html=True)
    render_stat_cards(metrics)
    st.markdown('<div style="height:1.1rem;"></div>', unsafe_allow_html=True)

    left, right = st.columns([1.5, 1], gap="medium")
    with left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="panel-head"><span class="section-title"><span class="bar"></span>Assessment Input</span></div>',
            unsafe_allow_html=True,
        )
        ex_btn = st.button("Load example patient", key="load_example",
                           help="Pre-fill with a known high-risk sample")
        if ex_btn:
            st.session_state.example = True
        patient, submitted = form_section(st.session_state.example)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="panel-head"><span class="section-title"><span class="bar"></span>Prediction Output</span></div>',
            unsafe_allow_html=True,
        )
        if submitted:
            if any(patient[k] <= 0 for k in ("age", "trestbps", "chol", "thalach")):
                st.warning("Age, blood pressure, cholesterol, and heart rate must be positive.")
            else:
                prediction, probability, transformed = predict_heart_disease(patient)
                log_prediction(patient, prediction, probability)
                contribs = feature_contributions(patient, transformed)
                display_result(prediction, probability, contribs, patient)
        else:
            render_empty_state()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:1.4rem;"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="panel-head"><span class="section-title"><span class="bar"></span>Recent Predictions</span></div>',
        unsafe_allow_html=True,
    )
    render_history()

    st.markdown(
        f"""
        <div class="footer">
            <div>CardioLens · Heart disease risk demo · Built for educational use</div>
            <div>Model v{metrics.get('model_version', '1.0')} · Not a medical diagnosis</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
