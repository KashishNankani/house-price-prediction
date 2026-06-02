# House Price Prediction

## Problem

Predict residential sale prices in Ames, Iowa using housing characteristics such as lot size, living area, quality ratings, basement features, garage information, and neighborhood data.

---

## Dataset

* 1460 houses
* 80 features
* Mix of numerical and categorical variables
* Contains missing values, skewed distributions, redundant features, and outliers

---

## Project Workflow

### 1. Missing Value Handling

Missing values were filled based on feature meaning rather than applying a single strategy to all columns.

Examples:

* Garage-related features → filled with **"No Garage"** when the property had no garage
* Basement-related features → filled with **"No Basement"** when the property had no basement
* LotFrontage → filled using neighborhood-wise median values
* Electrical → filled using mode (only one missing value)
* Masonry veneer features were handled using both `MasVnrType` and `MasVnrArea` together

---

### 2. Feature Engineering

Created new features that better represent how buyers perceive houses:

* Combined porch-related features into **TotalPorchSF**
* Combined bathroom counts into **TotalBath**
* Removed redundant area-related columns where information was already captured by broader features

---

### 3. Feature Selection

Removed features with little predictive value:

* Low-variance columns
* Redundant features identified during EDA
* Features with excessive missingness and limited usefulness

---

### 4. Outlier Treatment

Outliers were identified using distribution analysis and boxplots.

Approximately 3.6% of observations were removed to reduce the influence of extreme values and improve model stability.

---

### 5. Skewness Reduction

Several highly skewed numerical features were transformed using logarithms.

Examples:

* LotArea
* MasVnrArea
* Other positively skewed numerical variables

The target variable (`SalePrice`) was also log-transformed before training.

---

### 6. Encoding & Scaling

* One-Hot Encoding for nominal categorical features
* Ordinal Encoding for ordered categorical features
* StandardScaler applied before Linear Regression

---

## Models Evaluated

| Model             | RMSE       | MAE        | MAPE      | R²        |
| ----------------- | ---------- | ---------- | --------- | --------- |
| Linear Regression | **17,871** | **13,485** | **8.73%** | **0.904** |
| Decision Tree     | 29,745     | 22,892     | 15.2%     | 0.73      |
| Random Forest     | 21,153     | 15,393     | 10.2%     | 0.87      |
| XGBoost           | 19,677     | 14,181     | 9.4%      | 0.88      |

---

## Model Analysis

### Linear Regression

Performed best after preprocessing and target transformation.

The combination of feature engineering, skewness reduction, encoding, and log-transforming `SalePrice` helped linear relationships become more apparent, allowing Linear Regression to achieve the best overall performance.

### Decision Tree

Overfitted heavily on training data and generalized poorly to unseen houses.

### Random Forest

Reduced overfitting compared to a single decision tree but could not outperform the fully optimized Linear Regression pipeline.

### XGBoost

Captured additional nonlinear relationships and improved upon Random Forest, but the improvement over Linear Regression was relatively small.

---

## Final Result

### Linear Regression

* RMSE: **17,871**
* MAE: **13,485**
* MAPE: **8.73%**
* R²: **0.904**

On average, predictions are within approximately **8.7%** of the actual house price.

---

## Performance Progression

| Stage                                  | RMSE       | R²        |
| -------------------------------------- | ---------- | --------- |
| Initial Baseline                       | 31,237     | 0.86      |
| After Cleaning & Feature Engineering   | ~20,500    | ~0.87     |
| After Skewness Reduction & Log(Target) | **17,871** | **0.904** |

---

## Key Learning

The biggest improvement came from understanding and preparing the data rather than simply switching to more complex models.

RMSE improved from:

**31,237 → 17,871**

while R² improved from:

**0.86 → 0.904**

This project reinforced an important machine learning lesson:

> Better data preparation often contributes more to model performance than choosing a more complex algorithm.

---

## Future Improvements

* Perform cross-validation for more robust evaluation
* Experiment with advanced feature interactions
* Tune XGBoost and Random Forest using systematic hyperparameter search
* Analyze residuals to understand where prediction errors are still occurring
* Build an end-to-end prediction pipeline for deployment
