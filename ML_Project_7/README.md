# Heart Disease Prediction — CardioLens

A machine learning project that predicts whether a patient is at risk of heart disease using 13 clinical features such as age, cholesterol, blood pressure, chest pain type, and exercise-related indicators. The final model is served through **CardioLens**, a fully themed Streamlit web app with dark/light modes, an animated risk gauge, and per-patient explainability.

## Project Objective

This project demonstrates a complete machine learning workflow:

1. Data cleaning and exploration
2. Feature preprocessing
3. Model training and comparison
4. Model evaluation
5. Deployment as an interactive Streamlit web app

## Project Structure

```text
ML_Project_7/
|-- data/
|   |-- raw/
|   |   `-- heart.csv
|   `-- processed/
|       |-- heart_clean.csv
|       |-- x_train_processed.csv
|       |-- x_test_processed.csv
|       |-- y_train.csv
|       |-- y_test.csv
|       `-- preprocessor.joblib
|-- models/
|   |-- logistic_regression_model.pkl
|   `-- feature_columns.pkl
|-- notebooks/
|   |-- 01_eda_preprocessing.ipynb
|   |-- 02_model_training.ipynb
|   `-- 03_model_evaluation.ipynb
|-- app/
|   |-- app.py              # CardioLens Streamlit app
|   |-- styles.css           # Dual-theme glassmorphism stylesheet
|   |-- heart.png            # Favicon / page icon
|   `-- requirements.txt
|-- reports/
|   |-- metrics.json         # Accuracy / F1 metrics for the app header
|   `-- prediction_logs.csv  # History of app predictions
|-- .streamlit/
|   `-- config.toml          # Native Streamlit theme (dark, blue accent)
|-- README.md
`-- .gitignore
```

## Models Used

The project compares several classification models:

- Logistic Regression
- Naive Bayes
- Decision Tree
- SVM
- KNN

The final selected model is **Logistic Regression** because it gives the best balance of accuracy and F1-score on the test set, and its coefficients allow per-patient risk explanation.

## Evaluation Result

The chosen model achieved:

- Accuracy: 83.6%
- F1 Score: 84.8%

This is a strong result for a beginner-friendly healthcare prediction task and shows the model can classify both healthy and at-risk patients reasonably well.

## Workflow

1. Load raw heart disease dataset from `data/raw/heart.csv`
2. Clean and preprocess the data in `notebooks/01_eda_preprocessing.ipynb`
3. Train and compare models in `notebooks/02_model_training.ipynb`
4. Evaluate the best model in `notebooks/03_model_evaluation.ipynb`
5. Save the model and preprocessing pipeline in `models/`
6. Use the Streamlit app in `app/app.py` to make predictions from patient data
7. Store prediction attempts in `reports/prediction_logs.csv`

## CardioLens — Streamlit Frontend

To run the app locally:

```bash
cd ML_Project_7
pip install -r app/requirements.txt
streamlit run app/app.py
```

### Features

- **Assessment form** — 13 clinical inputs grouped into Demographics, Vitals & Labs, and ECG & Exercise sections, with reference ranges and tooltips on every field
- **Example patient** — one-click prefill of a known high-risk sample
- **Animated risk gauge** — predicted probability with a smooth sweep animation and risk tier (Low / Moderate / High)
- **Top Risk Drivers** — signed per-feature log-odds contributions from the logistic regression coefficients, grouped and ranked per patient
- **Input Summary** — friendly labels with units (e.g. `Resting BP · 125 mm Hg`) for exactly what was scored
- **Prediction history** — recent predictions table with summary chips and full CSV download
- **Dark / light theme** — live toggle; the entire UI, gauge, and charts adapt instantly
- **Design** — glassmorphism panels, gradient accents, ECG-line hero animation, and responsive layout for mobile

### Configuration

- `app/styles.css` holds the full dual-theme design system (CSS variables per theme)
- `.streamlit/config.toml` aligns Streamlit's native widgets with the dark theme
- `reports/metrics.json` feeds the accuracy / F1 stat cards in the app header

## Notes

- This project is for educational and demonstration purposes.
- It should not be used as a medical diagnosis.
- Prediction logs are stored in the `reports` folder for demo/testing purposes.

## Future Improvements

- Add more models and hyperparameter tuning
- Add confusion matrix and ROC chart visualization
- Deploy the app on Streamlit Cloud or Render
- Patient-level SHAP values for richer explanations
