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
* LotFrontage → filled using **neighborhood-wise median values** instead of global median, because LotFrontage follows a conditional distribution — P(LotFrontage | Neighborhood) — meaning houses in the same neighborhood tend to have similar lot sizes. Using a global median would ignore this subgroup structure and introduce bias. This is a case of Missing At Random (MAR), where missingness is related to another observed variable (Neighborhood), making conditional imputation the statistically correct approach.
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

### 4. Outlier Treatment — Intentionally Preserved

Outliers in SalePrice were **deliberately kept in the training data.**

While removing outliers improved evaluation metrics on paper, it created a more serious problem: a truncated training distribution. A model trained without expensive houses has never learned patterns for that price range. In production, when a high-value property is submitted for prediction, the model would silently underpredict — returning a plausible-looking but completely wrong number with no error thrown.

This is called **silent failure** and is one of the most dangerous issues in deployed ML systems.

By keeping outliers and instead applying log transformation to SalePrice, the model compresses extreme values without discarding them. The model learns from the full price spectrum and generalizes correctly to luxury properties — which is what a real estate company would require.

**Lesson: A model that looks slightly worse on metrics but handles real-world edge cases correctly is more valuable than one optimized purely for benchmark numbers.**

---

### 5. Skewness Reduction

Several highly skewed numerical features were transformed using logarithms.

Examples:

* LotArea
* MasVnrArea
* Other positively skewed numerical variables

The target variable (`SalePrice`) was also log-transformed before training. This compressed the right-skewed tail of house prices, brought residuals closer to a normal distribution (which Linear Regression assumes), and reduced the disproportionate influence of extreme values on model weights.

---

### 6. Encoding & Scaling

* One-Hot Encoding for nominal categorical features
* Ordinal Encoding for ordered categorical features
* StandardScaler applied before Linear Regression

---

## Models Evaluated

| Model             | RMSE       | MAE        | MAPE      | R²        |
| ----------------- | ---------- | ---------- | --------- | --------- |
| Linear Regression | **27,192** | **16,616** | **9.59%** | **0.894** |
| Decision Tree     | 29,745     | 22,892     | 15.2%     | 0.73      |
| Random Forest     | 21,153     | 15,393     | 10.2%     | 0.87      |
| XGBoost           | 19,677     | 14,181     | 9.4%      | 0.88      |

---

## Model Analysis

### Linear Regression

Performed best after preprocessing and target transformation.

The combination of feature engineering, skewness reduction, encoding, and log-transforming `SalePrice` helped linear relationships become more apparent. Importantly, StandardScaler significantly improved Linear Regression performance because the model relies on weight multiplication — scale directly affects predictions. Tree-based models like XGBoost are scale invariant (they split on thresholds, not magnitudes), so the same standardization had no effect on them.

This is why a heavily preprocessed dataset favored a linear model over more complex ensemble methods.

### Decision Tree

Overfitted heavily on training data and generalized poorly to unseen houses.

### Random Forest

Reduced overfitting compared to a single decision tree but could not outperform the fully optimized Linear Regression pipeline.

### XGBoost

Captured additional nonlinear relationships and improved upon Random Forest, but could not overcome the advantage Linear Regression gained from data that was engineered toward linearity.

---

## Final Result

### Linear Regression (trained on full price range including outliers)

* RMSE: **27,192**
* MAE: **16,616**
* MAPE: **9.59%**
* R²: **0.894**

On average, predictions are within approximately **9.6%** of the actual house price — across the full price spectrum including luxury properties.

---

## Performance Progression

| Stage                                  | RMSE       | R²        |
| -------------------------------------- | ---------- | --------- |
| Initial Baseline                       | 31,237     | 0.86      |
| After Cleaning & Feature Engineering   | ~20,500    | ~0.87     |
| After Skewness Reduction & Log(Target) | **27,192** | **0.894** |

---

## Key Learnings

The biggest improvement came from understanding and preparing the data rather than simply switching to more complex models.

A critical production insight emerged during this project: **optimizing for metrics is not the same as optimizing for real-world reliability.**

Removing outliers reduced RMSE from ~27k to ~17k — but created a model that would fail silently on luxury properties in production. Keeping the full training distribution and relying on log transformation instead is the correct production-grade decision, even at the cost of slightly worse benchmark numbers.

This project reinforced two important machine learning lessons:

> Better data preparation often contributes more to model performance than choosing a more complex algorithm.

> A model that generalizes correctly to the real world is more valuable than one that scores well on a filtered dataset.

---

## Future Improvements

* Build an end-to-end Sklearn Pipeline to chain preprocessing and prediction into a single deployable object
* Add input validation layer — check for missing fields, unseen categories, and out-of-range values before prediction reaches the model
* Deploy as a FastAPI endpoint so frontend applications can submit house features and receive price estimates
* Implement cross-validation for more robust evaluation across data splits
* Monitor for data drift over time and schedule periodic retraining
* Analyze residuals to identify remaining systematic prediction errors
* Experiment with advanced feature interactions and hyperparameter tuning for XGBoost and Random Forest