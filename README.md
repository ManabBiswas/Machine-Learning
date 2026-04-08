# ML Projects Repository

This repository contains two machine learning projects focused on predictive modeling using data analysis, preprocessing, and feature engineering.

---

## Project Structure

```
ML/
├── ML_Project_2/
│   ├── Heart.ipynb
│   ├── heart.csv
│
├── ML_project_1/
│   ├── insurance.ipynb
│   ├── insurance.csv
│
└── README.md
```

---

## Project 1: Insurance Prediction

**File:** `ML_project_1/insurance.ipynb`

### Overview
Predicts insurance charges based on customer demographic and health information.

### Key Steps

#### 1. **Data Import & Exploration**
- Load CSV file and explore structure
- Check data shape, columns, and data types
- View summary statistics

#### 2. **Data Cleaning**
- Remove duplicate records
- Check for missing values
- Encode categorical variables (`sex`, `smoker` → 0/1)
- One-hot encode region categories
- Rename columns for clarity

#### 3. **Feature Engineering**
- Create BMI categories (Underweight, Normal, Overweight, Obese)
- Perform correlation analysis using Pearson correlation
- Chi-square test for categorical feature importance
- Feature scaling using StandardScaler

#### 4. **Final Dataset**
Selected features based on statistical significance:
- `age`, `is_female`, `bmi`, `children`, `is_smoker`, `region_southeast`, `bmi_category_Obese`
- Target: `charges`

### Visualizations
- Distribution plots for numeric features
- Count plots for categorical variables
- Box plots for outlier detection
- Correlation heatmap

---

## Project 2: Heart Disease Prediction

**File:** `ML_Project_2/Heart.ipynb`

### Overview
Predicts heart disease presence based on clinical and physical measurements.

### Key Steps

#### 1. **Data Load & Exploration**
- Import heart disease dataset
- Display basic information (shape, columns, dtypes)
- Generate summary statistics

#### 2. **Data Cleaning**
- Handle zero values in `Cholesterol` (replace with mean)
- Handle zero values in `RestingBP` (replace with mean)
- Round values for consistency

#### 3. **Exploratory Data Analysis**
- Distribution plots for numeric features:
  - Age
  - Resting Blood Pressure
  - Cholesterol
  - Maximum Heart Rate

#### 4. **Categorical Analysis**
- Count plots for categorical variables
- Relationship between chest pain type and age
- Heart disease distribution across features

#### 5. **Feature Encoding**
- One-hot encode categorical features using `pd.get_dummies()`
- Convert all columns to integer type

#### 6. **Feature Scaling**
- Standardize numeric columns using StandardScaler:
  - Age, RestingBP, Cholesterol, MaxHR, Oldpeak

### Visualizations
- Histograms with KDE for distributions
- Category count plots
- Box plots for numeric relationships
- Violin plots for distribution shape
- Correlation heatmap

---

## 🛠️ Technologies Used

```python
# Data Processing
pandas          # Data manipulation
numpy           # Numerical operations

# Visualization
matplotlib      # Plotting
seaborn         # Statistical visualizations

# Machine Learning
sklearn         # Preprocessing and modeling
scipy.stats     # Statistical analysis
```

---

## Common Preprocessing Steps

### Data Cleaning
```python
# Remove duplicates
df.drop_duplicates(inplace=True)

# Check missing values
df.isnull().sum()

# Replace zero values with mean
df['column'] = df['column'].replace(0, df[df['column'] != 0]['column'].mean())
```

### Feature Encoding
```python
# Map categorical to numerical
df['column'] = df['column'].map({'category1': 0, 'category2': 1})

# One-hot encoding
df = pd.get_dummies(df, columns=['category_column'], drop_first=True)
```

### Feature Scaling
```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
numeric_cols = ['col1', 'col2', 'col3']
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
```

---

## 📈 Exploratory Data Analysis Methods

| Visualization | Purpose |
|--------------|---------|
| **Histogram** | Distribution of numeric features |
| **KDE Plot** | Density estimation |
| **Count Plot** | Frequency of categorical values |
| **Box Plot** | Identify outliers and quartiles |
| **Violin Plot** | Distribution shape comparison |
| **Heatmap** | Correlation between features |

---
<!--
## Next Steps

- Train classification models (Logistic Regression, Random Forest, etc.)
- Grid search for hyperparameter tuning
- Cross-validation for model evaluation
- Generate predictions on test data

---
-->

## Notes

- Both projects use pandas for data manipulation
- Seaborn and matplotlib for comprehensive visualizations
- StandardScaler ensures features are on similar scales for ML models
- One-hot encoding converts categorical variables to numerical format

---

**Author:** Manab Biswas  
**Date:** 2026
