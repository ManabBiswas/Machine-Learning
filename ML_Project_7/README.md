# Heart Disease Prediction Project

A machine learning project that predicts whether a patient is at risk of heart disease using clinical features such as age, cholesterol, blood pressure, chest pain, and exercise-related symptoms.

## Project Objective

This project demonstrates a complete machine learning workflow:

1. Data cleaning and exploration
2. Feature preprocessing
3. Model training and comparison
4. Model evaluation
5. Deployment as a simple Streamlit web app

## Current Project Structure

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
|       |-- preprocessor.joblib
|-- models/
|   |-- logistic_regression_model.pkl
|   `-- feature_columns.pkl
|-- notebooks/
|   |-- 01_eda_preprocessing.ipynb
|   |-- 02_model_training.ipynb
|   `-- 03_model_evaluation.ipynb
|-- app/
|   |-- app.py
|   `-- requirements.txt
|-- reports/
|   |-- prediction_logs.csv
|-- README.md
`-- .gitignore
```

## Models Used

The project compares several classification models, including:

- Logistic Regression
- Naive Bayes
- Decision Tree
- SVM
- KNN

The final selected model is the Logistic Regression model because it gives the best balance of accuracy and F1-score on the test set.

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

## Streamlit Frontend

To run the app locally:

```bash
cd "C:\Users\Manab Biswas\codes\codeSpace5\ML\ML_Project_7"
pip install -r app/requirements.txt
streamlit run app/app.py
```

The app provides a form where the user enters clinical values and receives a heart disease risk prediction.

## Notes

- This project is for educational and demonstration purposes.
- It should not be used as a medical diagnosis.
- Prediction logs are stored in the `reports` folder for demo/testing purposes.

## Future Improvements

- Add more models and hyperparameter tuning
- Add confusion matrix and ROC chart visualization
- Improve the frontend styling and layout
- Deploy the app on Streamlit Cloud or Render
