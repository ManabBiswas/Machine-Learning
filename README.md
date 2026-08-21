# 🤖 Machine Learning Portfolio

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-orange.svg)](https://pandas.pydata.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-green.svg)](https://scikit-learn.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-Visualization-blue.svg)](https://seaborn.pydata.org/)

A collection of predictive modeling projects focused on healthcare and insurance data. This repository demonstrates the end-to-end ML pipeline: from raw data exploration and rigorous preprocessing to statistical feature engineering.

---

## 🚀 Projects

### 🏥 Heart Disease Prediction
**Path:** `ML_Project_2/Heart.ipynb`

Predicts the presence of heart disease based on clinical and physical measurements.
- **Key Highlights:**
  - Handled missing/zero values in `Cholesterol` and `RestingBP` using mean imputation.
  - Performed comprehensive EDA with KDE plots and Violin plots.
  - Implemented one-hot encoding for categorical clinical data.
  - Standardized features using `StandardScaler`.

### 💰 Insurance Charge Prediction
**Path:** `ML_project_1/insurance.ipynb`

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

This repository follows a standardized preprocessing pipeline:

### 1. Data Cleaning & Engineering
- **Duplicate Removal:** `df.drop_duplicates()`
- **Imputation:** Replacing invalid zeros with column means.
- **Encoding:** 
  - Binary mapping for simple categories.
  - One-hot encoding via `pd.get_dummies()` for multi-class categories.
- **Scaling:** Normalizing numeric ranges using `StandardScaler`.

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
