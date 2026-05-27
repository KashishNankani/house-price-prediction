# House Price Prediction

## Project Overview

This project focuses on predicting house prices using the Ames Housing dataset with Machine Learning techniques.  
The main objective of this project was not only to train a model, but also to understand real-world preprocessing, feature analysis, missing value handling, and model evaluation workflows used in ML projects.

The project was developed using a reasoning-first approach instead of blindly following tutorials. Every preprocessing decision was analyzed using feature meaning, distributions, relationships, and dataset documentation.

---

## Workflow

The complete workflow followed in this project:

- Exploratory Data Analysis (EDA)
- Feature understanding using dataset documentation
- Missing value analysis and semantic imputation
- Distribution analysis using histograms and boxplots
- Redundancy analysis between related features
- Handling categorical and numerical features separately
- Feature encoding
- Linear Regression model training
- Model evaluation using RMSE and R² Score

---

## Missing Value Handling

Different missing value strategies were used depending on feature semantics and dataset behavior.

### Electrical
- Used mode imputation because it is a categorical feature and the missing proportion was negligible.

### Masonry Veneer Features
- `MasVnrType` missing values were filled with `None` where veneer was absent (`MasVnrArea = 0`).
- Inconsistent rows with existing veneer area but missing type were filled using mode.
- `MasVnrArea` missing values were filled with `0.0` for houses without masonry veneer.

### FireplaceQu
- Missing values represented absence of fireplace, therefore filled with `NoFireplace`.

### LotFrontage
- Numerical feature with skewed distribution and outliers.
- Median-based reasoning was preferred over mean imputation.

### Garage Features
Features:
- GarageType
- GarageYrBlt
- GarageFinish
- GarageQual

Reason:
- Missing values represented houses without garages.
- Categorical garage features were filled with `NoGarage`.
- `GarageYrBlt` was filled with `0`.

### Basement Features
Features:
- BsmtQual
- BsmtFinType1
- BsmtCond

Reason:
- Missing values represented houses without basements.
- Filled with `NoBasement`.

### BsmtExposure
- One inconsistent missing value where basement existed was filled with `No`.
- Remaining missing values were filled with `NoBasement`.

---

## Feature Analysis

Several feature-level investigations were performed during preprocessing:

- Compared basement quality and condition features for redundancy analysis
- Investigated missing-value patterns using related columns
- Analyzed feature distributions using histograms and boxplots
- Checked skewness and outlier behavior
- Verified assumptions using cross-feature validation instead of blind imputation

---

## Model Used

- Linear Regression

Linear Regression was used as the baseline model to better understand:
- feature relationships
- preprocessing impact
- overfitting behavior
- linear assumptions

---

## Model Performance

### Evaluation Metrics

- Train R² Score: 0.903
- Test R² Score: 0.861
- RMSE: 31,237

These results indicate good baseline generalization performance for a Linear Regression model.

---

## Libraries Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn

---

## Future Improvements

Possible future improvements for this project:

- Log transformation of target variable
- Feature engineering
- Ordinal encoding for ranked categorical features
- Outlier treatment
- Hyperparameter tuning
- Trying advanced models:
  - Ridge Regression
  - Lasso Regression
  - Random Forest
  - XGBoost

---

## Key Learning Outcomes

This project helped in understanding:

- Real-world preprocessing workflows
- Semantic missing value handling
- Feature relationship analysis
- Distribution and outlier analysis
- Baseline ML pipeline creation
- Git and GitHub workflow management
- Model evaluation and interpretation

---