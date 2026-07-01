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

* Low-variance columns (e.g. `Id` — row number with no predictive meaning)
* Redundant features identified during EDA
* Features with excessive missingness and limited usefulness

#### Multicollinearity Check

Beyond removing irrelevant features, a correlation analysis was performed between all feature pairs to detect multicollinearity — where two input features are highly correlated with each other, causing model coefficients to become unstable and unreliable.

Two problematic pairs were identified:

| Feature Pair | Correlation | Decision |
|---|---|---|
| GarageCars vs GarageArea | 0.88 | Dropped GarageArea (lower correlation with SalePrice: 0.62 vs 0.64) |
| GrLivArea vs TotRmsAbvGrd | 0.83 | Dropped TotRmsAbvGrd (lower correlation with SalePrice: 0.53 vs 0.69) |

**Decision rule:** When two features are highly correlated with each other, keep the one with higher correlation to SalePrice. Let data decide, not intuition.

Dropping these features did not dramatically change metrics but made coefficients significantly more stable and trustworthy — which matters more for a production model than a small metric gain.

---

### 4. Outlier Treatment — Intentionally Preserved

Outliers in SalePrice were **deliberately kept in the training data.**

While removing outliers improved evaluation metrics on paper, it created a more serious problem: a truncated training distribution. A model trained without expensive houses has never learned patterns for that price range. In production, when a high-value property is submitted for prediction, the model would silently underpredict — returning a plausible-looking but completely wrong number with no error thrown.

This is called **silent failure** and is one of the most dangerous issues in deployed ML systems.

By keeping outliers and instead applying log transformation to SalePrice, the model compresses extreme values without discarding them. The model learns from the full price spectrum and generalizes correctly to luxury properties — which is what a real estate company would require.

**Lesson: A model that looks slightly worse on metrics but handles real-world edge cases correctly is more valuable than one optimized purely for benchmark numbers.**

---

### 5. Skewness Reduction & Log Transformation

Several highly skewed numerical features were transformed using logarithms.

Examples:

* LotArea
* MasVnrArea
* Other positively skewed numerical variables

The target variable (`SalePrice`) was also log-transformed before training for two reasons:

**Reason 1 — Exponential relationships become linear**
House prices follow exponential growth patterns. The jump from Overall Quality 9 to 10 is worth far more than the jump from 1 to 2. This is a non-linear relationship that Linear Regression cannot fit directly. Log transformation converts the exponential relationship to linear — P(log(SalePrice) | features) — which the model can learn effectively.

**Reason 2 — Normality of residuals**
Raw SalePrice is right-skewed, which violates the normality of residuals assumption in Linear Regression. Log transformation compresses the tail and brings residuals closer to a normal distribution, making coefficients more reliable.

---

### 6. Encoding & Scaling

* One-Hot Encoding for nominal categorical features
* Ordinal Encoding for ordered categorical features
* StandardScaler applied before Linear Regression

StandardScaler significantly improved Linear Regression performance because the model relies on weight multiplication — scale directly affects predictions and coefficient comparability. Tree-based models like XGBoost are scale invariant (they split on thresholds, not magnitudes), so standardization had no effect on them.

---

## Models Evaluated

| Model             | RMSE       | MAE        | MAPE      | R²        |
| ----------------- | ---------- | ---------- | --------- | --------- |
| Linear Regression | **27,040** | **16,626** | **9.56%** | **0.896** |
| Decision Tree     | 29,745     | 22,892     | 15.2%     | 0.73      |
| Random Forest     | 21,153     | 15,393     | 10.2%     | 0.87      |
| XGBoost           | 19,677     | 14,181     | 9.4%      | 0.88      |

**Note on metrics:** MAPE (Mean Absolute Percentage Error) was used as the primary evaluation metric rather than RMSE, because house prices span a wide range. A 20k error on a 50k house is catastrophic; the same error on a 500k house is acceptable. MAPE captures this proportional difference — RMSE treats both identically.

---

## Model Analysis

### Linear Regression

Performed best after preprocessing and target transformation.

Linear Regression outperforming XGBoost is unusual and worth explaining. The answer lies in how the data was prepared:

* Skewness was reduced across numerical features
* SalePrice was log-transformed, converting exponential relationships to linear ones
* Multicollinearity was removed, stabilizing coefficients
* StandardScaler was applied, making feature weights directly comparable

These steps satisfied every assumption of Linear Regression — linearity, normality of residuals, homoscedasticity, no multicollinearity. The data was engineered toward linearity, so naturally a linear model thrived.

XGBoost is scale invariant — standardization that significantly helped Linear Regression had zero effect on it. On a small, clean, well-prepared dataset of 1460 houses, the additional complexity of XGBoost found no advantage to exploit.

### Decision Tree

Overfitted heavily on training data and generalized poorly to unseen houses. Memorized training patterns instead of learning generalizable rules.

### Random Forest

Reduced overfitting compared to a single decision tree by averaging multiple trees. Still could not outperform the fully optimized Linear Regression pipeline on this dataset.

### XGBoost

Captured additional nonlinear relationships and improved upon Random Forest, but could not overcome the advantage Linear Regression gained from data engineered toward linearity.

---

## Final Result

### Linear Regression — trained on full price range including outliers

* RMSE: **27,040**
* MAE: **16,626**
* MAPE: **9.56%**
* R²: **0.896**

On average, predictions are within approximately **9.6%** of the actual house price — across the full price spectrum including luxury properties.

R² of 0.896 means the model explains 89.6% of why house prices differ from each other. The remaining 10.4% is noise the model could not capture.

---

## Performance Progression

| Stage | RMSE | R² |
| --- | --- | --- |
| Initial Baseline | 31,237 | 0.860 |
| After Cleaning & Feature Engineering | ~20,500 | ~0.870 |
| After Skewness Reduction & Log(Target) | 27,192 | 0.894 |
| After Multicollinearity Removal | **27,040** | **0.896** |

---

## Key Learnings

**1. Data preparation matters more than model complexity**
The biggest performance jump came from log transforming SalePrice and reducing skewness — not from switching to XGBoost or Random Forest. A well-prepared dataset in a simple model outperformed a complex model on raw data.

**2. Optimizing for metrics is not the same as optimizing for real-world reliability**
Removing outliers reduced RMSE from ~27k to ~17k — impressive on paper. But it created a model that would fail silently on luxury properties in production. Keeping the full training distribution and relying on log transformation is the correct production-grade decision, even at the cost of slightly worse benchmark numbers.

**3. Multicollinearity is a coefficient problem, not just a metric problem**
Dropping GarageArea and TotRmsAbvGrd barely changed R² but made coefficients significantly more stable and trustworthy. Metrics measure accuracy. Coefficient stability determines whether you can trust and interpret the model.

**4. Understand why, not just what**
Log transformation did not just reduce outlier influence — it converted exponential house price relationships into linear ones that Linear Regression could actually learn. Standardization did not just normalize scale — it made coefficients directly comparable so the model could correctly weight feature importance.

---

## Future Improvements

* Build an end-to-end Sklearn Pipeline to chain preprocessing and prediction into a single deployable object — saving scaler, encoder, and imputation values together
* Add input validation layer — check for missing fields, unseen categories, and out-of-range values before prediction reaches the model, preventing silent failure
* Deploy as a FastAPI endpoint so frontend applications can submit house features and receive price estimates
* Implement cross-validation for more robust evaluation across data splits instead of single train-test split
* Monitor for data drift over time and schedule periodic retraining as housing market conditions change
* Analyze residuals systematically to identify remaining patterns in prediction errors
* Run VIF analysis to formally confirm multicollinearity removal beyond correlation checks
* Experiment with advanced feature interactions and hyperparameter tuning for XGBoost and Random Forest