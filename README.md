# 🤖 Machine Learning Portfolio

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-orange.svg)](https://pandas.pydata.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-green.svg)](https://scikit-learn.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-Visualization-blue.svg)](https://seaborn.pydata.org/)

A collection of machine learning projects covering healthcare, insurance, automotive, passenger survival, and flower classification datasets. The notebooks demonstrate an end-to-end workflow from data exploration and preprocessing to model training and evaluation.

---

## 🚀 Projects

### 🫀 CardioLens — Heart Disease Risk App (Deployed)
**Path:** `ML_Project_7_A/cardiolens/`
**Live:** [cardiolens365.vercel.app](https://cardiolens365.vercel.app) ·
API: [cardiolens-api-r1q7.onrender.com](https://cardiolens-api-r1q7.onrender.com)

Full-stack interpretable heart-disease risk prediction: FastAPI + scikit-learn backend, React 19 + TypeScript + Tailwind frontend.
- **Key Highlights:**
  - Logistic regression served as a JSON API (Dockerized, deployed on Render).
  - Risk tier + top feature contributions for every prediction (SHAP-style drivers).
  - Multi-page React SPA (Home / Assess / Insights / About) with dark/light themes.
  - CI via GitHub Actions; CORS locked to the deployed origin via env var.

---

### 🧬 Iris Classification with KNN
**Path:** `ML_Project_5/KNN-2.ipynb`

Classifies Iris flowers with a K-Nearest Neighbors model.
- **Key Highlights:**
  - Loaded and explored the Iris dataset from scikit-learn.
  - Standardized features with `StandardScaler` before distance-based modeling.
  - Trained a 5-neighbor KNN classifier.
  - Evaluated accuracy, classification metrics, and a confusion matrix.
  - Predicted the class of a new flower sample.

### 🚗 Ford Vehicle Analysis
**Path:** `ML_Project_3/notebook687e6ed2f6.ipynb`

Explores Ford vehicle data and applies machine learning techniques to an automotive dataset.

### 🚢 Titanic Survival Prediction
**Path:** `ML_Project_4/Titanic.ipynb`

Analyzes passenger data to investigate the factors associated with Titanic survival.

### 🏥 Heart Disease Prediction
**Path:** `ML_Project_2/Heart.ipynb`

Predicts the presence of heart disease based on clinical and physical measurements.
- **Key Highlights:**
  - Handled missing/zero values in `Cholesterol` and `RestingBP` using mean imputation.
  - Performed comprehensive EDA with KDE plots and Violin plots.
  - Implemented one-hot encoding for categorical clinical data.
  - Standardized features using `StandardScaler`.

### 💰 Insurance Charge Prediction
**Path:** `ML_Project_1/insurance.ipynb`

Predicts healthcare insurance costs based on customer demographics and health metrics.
- **Key Highlights:**
  - Engineered `BMI` categories (Underweight, Normal, Overweight, Obese).
  - Used **Pearson Correlation** and **Chi-Square tests** for feature selection.
  - Optimized dataset by selecting only statistically significant features.
  - Applied one-hot encoding for regional and demographic data.

---

## 🛠️ Tech Stack

| Category | Tools |
| :--- | :--- |
| **Language** | Python |
| **Data Manipulation** | `pandas`, `numpy` |
| **Visualization** | `matplotlib`, `seaborn` |
| **Machine Learning** | `scikit-learn`, `scipy.stats` |

---

## 📖 Core ML Workflow

The projects use a practical machine learning workflow:

### 1. Data Cleaning & Engineering
- **Duplicate Removal:** `df.drop_duplicates()`
- **Imputation:** Replacing invalid zeros with column means.
- **Encoding:** 
  - Binary mapping for simple categories.
  - One-hot encoding via `pd.get_dummies()` for multi-class categories.
- **Scaling:** Normalizing numeric ranges using `StandardScaler`, especially before distance-based models such as KNN.

### 2. Exploratory Data Analysis (EDA)
| Plot Type | Purpose |
| :--- | :--- |
| **Histogram/KDE** | Analyzing feature distributions |
| **Box/Violin Plots** | Outlier detection & distribution shape |
| **Count Plots** | Frequency analysis of categories |
| **Heatmaps** | Identifying multi-collinearity between features |

---

## 🏁 Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/ML.git
   cd ML
   ```
2. **Install dependencies:**
   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn scipy
   ```
3. **Run Notebooks:**
   Open `.ipynb` files using Jupyter Notebook or VS Code.

---

**Author:** Manab Biswas  
**Year:** 2026
