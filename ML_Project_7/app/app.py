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

FEATURE_COLUMNS = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal",
]

st.set_page_config(page_title="Heart Disease Predictor", page_icon="🫀", layout="wide")


def inject_dashboard_style():
    st.markdown(
        """
        <style>
        :root {
            --bg: #f4f7fb;
            --panel: rgba(255,255,255,0.82);
            --card: #ffffff;
            --line: #dfe7f3;
            --text: #0f172a;
            --muted: #475569;
            --primary: #2563eb;
            --primary-strong: #1d4ed8;
            --secondary: #8b5cf6;
            --success: #16a34a;
            --success-soft: #dcfce7;
            --danger: #dc2626;
            --danger-soft: #fee2e2;
            --warning: #f59e0b;
            --warning-soft: #fef3c7;
            --shadow: 0 22px 50px rgba(15, 23, 42, 0.12);
        }

        html, body, [class*="css"] {
            color: var(--text) !important;
        }

        .stApp {
            background: radial-gradient(circle at top left, #e0f2fe 0%, #f8fafc 28%, #eef2ff 60%, #fdf2f8 100%);
            color: var(--text);
        }

        div[data-testid="stMainBlockContainer"] {
            padding-top: 0.9rem;
            padding-bottom: 1.5rem;
        }

        .dashboard-shell {
            background: rgba(255,255,255,0.42);
            border: 1px solid rgba(148,163,184,0.22);
            border-radius: 30px;
            padding: 1.4rem 1.5rem 1.1rem;
            box-shadow: 0 22px 60px rgba(15, 23, 42, 0.10);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
        }

        .hero {
            background: linear-gradient(135deg, rgba(191,219,254,0.72), rgba(239,246,255,0.82), rgba(245,243,255,0.75), rgba(252,231,243,0.72));
            border: 1px solid rgba(148,163,184,0.18);
            border-radius: 24px;
            padding: 1.6rem 1.5rem;
            margin-bottom: 1.1rem;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.65), 0 16px 36px rgba(37, 99, 235, 0.06);
        }

        .hero-title {
            font-size: 2.55rem;
            line-height: 1.08;
            font-weight: 800;
            letter-spacing: -0.05em;
            color: #0f172a;
            margin: 0;
        }

        .hero-subtitle {
            color: #475569;
            font-size: 1rem;
            margin-top: 0.45rem;
            margin-bottom: 0;
        }

        .stat-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
            border: 1px solid rgba(148,163,184,0.28);
            border-radius: 20px;
            padding: 1.05rem 1.15rem;
            box-shadow: 0 12px 24px rgba(37, 99, 235, 0.08);
            height: 100%;
        }

        .stat-label {
            color: var(--muted);
            font-size: 0.7rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.3rem;
        }

        .stat-value {
            color: var(--primary-strong);
            font-weight: 800;
            font-size: 1.8rem;
            margin: 0;
        }

        .section-card {
            background: rgba(255,255,255,0.42);
            border: 1px solid rgba(148,163,184,0.18);
            border-radius: 22px;
            padding: 1.05rem 1.1rem;
            box-shadow: 0 14px 30px rgba(15, 23, 42, 0.05), inset 0 1px 0 rgba(255,255,255,0.42);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            height: 100%;
        }

        .section-title {
            font-weight: 700;
            font-size: 1.08rem;
            color: var(--text);
            margin-bottom: 0.8rem;
        }

        .result-panel {
            border-radius: 20px;
            padding: 1.1rem 1.15rem;
            border: 1px solid var(--line);
            box-shadow: 0 10px 18px rgba(15, 23, 42, 0.04);
            margin-top: 0.25rem;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 0.38rem;
            padding: 0.42rem 0.7rem;
            border-radius: 999px;
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            border: 1px solid transparent;
        }

        .badge-high {
            background: var(--danger-soft);
            color: #991b1b;
            border-color: #fecaca;
        }

        .badge-low {
            background: var(--success-soft);
            color: #166534;
            border-color: #bbf7d0;
        }

        .risk-ring-wrap {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-top: 0.6rem;
            margin-bottom: 0.6rem;
        }

        .risk-ring {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: conic-gradient(#dc2626 0deg, #dc2626 var(--angle), #e2e8f0 var(--angle), #e2e8f0 360deg);
            display: grid;
            place-items: center;
            box-shadow: inset 0 0 0 1px rgba(148,163,184,0.15);
        }

        .risk-ring-inner {
            width: 102px;
            height: 102px;
            background: white;
            border-radius: 50%;
            display: grid;
            place-items: center;
            text-align: center;
            box-shadow: inset 0 0 0 1px rgba(148,163,184,0.18);
        }

        .risk-ring-inner strong {
            display: block;
            font-size: 1.4rem;
            color: var(--text);
            line-height: 1.2;
        }

        .risk-ring-inner span {
            color: var(--muted);
            font-size: 0.7rem;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .mini-chart {
            margin-top: 0.9rem;
            border-radius: 14px;
            background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
            border: 1px solid rgba(148,163,184,0.18);
            padding: 0.5rem 0.7rem 0.2rem;
        }

        div[data-testid="stFormSubmitButton"] > button,
        button[kind="primary"],
        .stButton > button,
        div[data-testid="stBaseButton-primary"],
        div[data-testid="baseButton-primary"] {
            width: 100% !important;
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            background-color: #2563eb !important;
            color: #ffffff !important;
            border: 1px solid rgba(37, 99, 235, 0.8) !important;
            border-radius: 14px !important;
            padding: 0.9rem 1.2rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.02em;
            transition: all 0.22s ease;
            box-shadow: 0 12px 24px rgba(37, 99, 235, 0.18);
            appearance: none !important;
            -webkit-appearance: none !important;
        }

        div[data-testid="stFormSubmitButton"] > button:hover,
        button[kind="primary"]:hover,
        .stButton > button:hover,
        div[data-testid="stBaseButton-primary"]:hover,
        div[data-testid="baseButton-primary"]:hover {
            background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
            background-color: #1d4ed8 !important;
            box-shadow: 0 16px 28px rgba(37, 99, 235, 0.24);
            transform: translateY(-1px);
            color: #ffffff !important;
        }

        div[data-testid="stFormSubmitButton"] > button:focus,
        button[kind="primary"]:focus,
        .stButton > button:focus,
        div[data-testid="stBaseButton-primary"]:focus,
        div[data-testid="baseButton-primary"]:focus {
            box-shadow: 0 0 0 4px rgba(59,130,246,0.18) !important;
            outline: none !important;
            color: #ffffff !important;
            background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
        }

        div[data-testid="stFormSubmitButton"] > button * {
            color: #ffffff !important;
        }

        .stNumberInput label,
        .stSelectbox label,
        .stTextInput label,
        .stMarkdown,
        .stDataFrame,
        .stDataFrame div,
        .stCaption,
        .stSuccess,
        .stError,
        .stInfo {
            color: #0f172a !important;
        }

        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select,
        .stTextInput > div > div > input {
            border-radius: 12px !important;
            border: 1px solid #cbd5e1 !important;
            background: white !important;
            color: #0f172a !important;
            padding: 0.78rem 0.9rem !important;
            min-height: 48px;
            box-shadow: inset 0 1px 2px rgba(15, 23, 42, 0.04);
        }

        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus,
        .stTextInput > div > div > input:focus {
            border-color: #60a5fa !important;
            box-shadow: 0 0 0 4px rgba(96,165,250,0.15) !important;
        }

        .stDataFrame {
            border-radius: 14px;
            overflow: hidden;
        }

        .footer {
            margin-top: 1.4rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(148,163,184,0.22);
            color: #475569;
            font-size: 0.82rem;
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 0.6rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource
def load_model_and_preprocessor():
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    return model, preprocessor


def log_prediction(patient_data: dict, prediction: int, probability: float):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "age": patient_data["age"],
        "sex": patient_data["sex"],
        "cp": patient_data["cp"],
        "trestbps": patient_data["trestbps"],
        "chol": patient_data["chol"],
        "fbs": patient_data["fbs"],
        "restecg": patient_data["restecg"],
        "thalach": patient_data["thalach"],
        "exang": patient_data["exang"],
        "oldpeak": patient_data["oldpeak"],
        "slope": patient_data["slope"],
        "ca": patient_data["ca"],
        "thal": patient_data["thal"],
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


def predict_heart_disease(patient_data: dict):
    model, preprocessor = load_model_and_preprocessor()
    input_df = pd.DataFrame([patient_data], columns=FEATURE_COLUMNS)
    transformed = preprocessor.transform(input_df)
    prediction = int(model.predict(transformed)[0])
    probability = float(model.predict_proba(transformed)[0][1])
    return prediction, probability


def render_risk_ring(probability: float):
    angle = min(max(probability, 0.0), 1.0) * 360
    risk_label = "High" if probability >= 0.5 else "Low"
    badge_class = "badge-high" if probability >= 0.5 else "badge-low"
    color = "#dc2626" if probability >= 0.5 else "#16a34a"

    st.markdown(
        f"""
        <div class="risk-ring-wrap">
            <div class="risk-ring" style="background: conic-gradient({color} 0deg, {color} {angle}deg, #e2e8f0 {angle}deg, #e2e8f0 360deg);">
                <div class="risk-ring-inner">
                    <div>
                        <strong>{probability * 100:.1f}%</strong>
                        <span>Risk</span>
                    </div>
                </div>
            </div>
        </div>
        <div style="text-align:center; margin-top:0.5rem;">
            <span class="badge {badge_class}">{risk_label} Risk</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_result(prediction: int, probability: float):
    is_high_risk = prediction == 1
    result_bg = "#fff1f2" if is_high_risk else "#f0fdf4"
    hairline = "#fecaca" if is_high_risk else "#bbf7d0"
    heading = "High Risk" if is_high_risk else "Low Risk"
    text_color = "#991b1b" if is_high_risk else "#166534"
    intro = "The model predicts a significant heart disease risk." if is_high_risk else "The model predicts no major risk detected."

    st.markdown(
        f"""
        <div class="result-panel" style="background:{result_bg};border-color:{hairline};">
            <div style="display:flex; align-items:center; justify-content:space-between; gap:0.75rem; flex-wrap:wrap;">
                <h3 style="margin:0; color:{text_color};">{heading}</h3>
                <span class="badge {'badge-high' if is_high_risk else 'badge-low'}">{'High' if is_high_risk else 'Low'} Risk</span>
            </div>
            <p style="margin:10px 0 0; color:{text_color};">{intro}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_risk_ring(probability)

    chart_df = pd.DataFrame({
        "Category": ["Current Risk", "Remaining Safe"],
        "Probability": [probability, 1 - probability],
    })
    st.markdown('<div class="mini-chart">', unsafe_allow_html=True)
    st.bar_chart(chart_df.set_index("Category"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.progress(min_value=0.0, max_value=1.0, value=probability)
    st.caption("Educational use only — not a medical diagnosis.")


def build_patient_form():
    with st.form("heart_form"):
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Patient Information</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age *", min_value=18, max_value=100, value=52)
            sex = st.selectbox("Sex *", [0, 1], format_func=lambda x: "Female" if x == 0 else "Male")
            cp = st.selectbox("Chest Pain Type *", [0, 1, 2, 3])
            trestbps = st.number_input("Resting Blood Pressure *", min_value=80, max_value=220, value=125)
            chol = st.number_input("Cholesterol *", min_value=100, max_value=600, value=212)
            fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl *", [0, 1])
            restecg = st.selectbox("Resting ECG *", [0, 1, 2])

        with col2:
            thalach = st.number_input("Maximum Heart Rate *", min_value=60, max_value=220, value=168)
            exang = st.selectbox("Exercise-Induced Angina *", [0, 1])
            oldpeak = st.number_input("Oldpeak *", min_value=0.0, max_value=7.0, value=1.0, step=0.1)
            slope = st.selectbox("Slope *", [0, 1, 2])
            ca = st.selectbox("Number of Major Vessels *", [0, 1, 2, 3])
            thal = st.selectbox("Thalassemia *", [0, 1, 2, 3])

        st.markdown('</div>', unsafe_allow_html=True)
        submit = st.form_submit_button("Predict Risk", use_container_width=True)

    patient = {
        "age": int(age),
        "sex": int(sex),
        "cp": int(cp),
        "trestbps": int(trestbps),
        "chol": int(chol),
        "fbs": int(fbs),
        "restecg": int(restecg),
        "thalach": int(thalach),
        "exang": int(exang),
        "oldpeak": float(oldpeak),
        "slope": int(slope),
        "ca": int(ca),
        "thal": int(thal),
    }

    return patient, submit


def show_recent_logs():
    if LOG_FILE.exists():
        logs = pd.read_csv(LOG_FILE)
        if not logs.empty:
            st.markdown('<div class="section-title" style="margin-top:1.5rem;">Recent Predictions</div>', unsafe_allow_html=True)
            st.dataframe(logs.tail(5), use_container_width=True)


def main():
    inject_dashboard_style()

    st.markdown('<div class="dashboard-shell">', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero"><p class="hero-title">Heart Disease Predictor</p><p class="hero-subtitle">Clinical risk assessment powered by a trained machine learning model.</p></div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="stat-card"><div class="stat-label">Model</div><p class="stat-value">LogReg</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-card"><div class="stat-label">Accuracy</div><p class="stat-value">83.6%</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-card"><div class="stat-label">F1 Score</div><p class="stat-value">84.9%</p></div>', unsafe_allow_html=True)

    form_col, result_col = st.columns([1.45, 0.9])
    with form_col:
        patient, submitted = build_patient_form()
    with result_col:
        st.markdown('<div class="section-card"><div class="section-title">Prediction Output</div>', unsafe_allow_html=True)
        if submitted:
            required_values = [
                patient["age"],
                patient["sex"],
                patient["cp"],
                patient["trestbps"],
                patient["chol"],
                patient["fbs"],
                patient["restecg"],
                patient["thalach"],
                patient["exang"],
                patient["oldpeak"],
                patient["slope"],
                patient["ca"],
                patient["thal"],
            ]
            if any(v is None or v == "" for v in required_values):
                st.warning("Please fill all required fields before predicting.")
            elif any(v <= 0 for v in [patient["age"], patient["trestbps"], patient["chol"], patient["thalach"]]):
                st.warning("Age, blood pressure, cholesterol, and heart rate must be greater than zero.")
            else:
                prediction, probability = predict_heart_disease(patient)
                log_prediction(patient, prediction, probability)
                display_result(prediction, probability)
        else:
            st.info("Enter patient details and click Predict Risk.")
            st.caption("Model output appears here after you submit the form.")
        st.markdown('</div>', unsafe_allow_html=True)

    show_recent_logs()

    st.markdown(
        """
        <div class="footer">
            <div>Heart disease risk demo • Built for educational use</div>
            <div>Updated with modern dashboard styling</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
