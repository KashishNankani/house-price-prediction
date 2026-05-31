# House Price Predictor

## Problem
Predict sale price of houses in Ames, Iowa using 80 features.

## Data
1460 houses, 80 columns — messy, missing values, skewed distributions, redundant features.

## What I Did

**Data Cleaning:**
- Dropped columns with 90%+ same value — no variation means nothing to learn
- Filled missing values with logic — neighbourhood median for LotFrontage, None for features that don't exist, median for unknowns
- Removed 54 luxury outliers above $350k — only 3.6% of data, too few for model to learn from

**Feature Engineering:**
- Combined 4 porch columns into TotalPorchSF — total area matters more than type
- Combined bathrooms into TotalBath — buyers think in total bathrooms not separate counts
- Removed redundant area columns — GrLivArea already captures 1stFlrSF + 2ndFlrSF

**Preprocessing:**
- Fixed skewed features with log transformation — LotArea had 11.18 skewness
- Standard scaling over Min-Max — more robust to remaining outliers
- One hot encoding for nominal categories, ordinal encoding for ranked ones

## Models Tested

| Model              | RMSE   |    MAE | MAPE  | R2   |
|--------------------|--------|--------|-------|------|
| Linear Regression  | 20,508 | 15,563 | 10.3% | 0.87 |
| Decision Tree      | 29,745 | 22,892 | 15.2% | 0.73 |
| Random Forest      | 21,153 | 15,393 | 10.2% | 0.87 |
| XGBoost            | 19,677 | 14,181 | 9.4%  | 0.88 |

## Why Each Model Behaved This Way

**Linear Regression** — heavy data cleaning made relationships linear. LR thrives on linear data. Preprocessing shaped which model would win.

**Decision Tree** — overfitted badly on default settings. Train RMSE was 163, Test RMSE was 32,000. Limiting depth helped but couldn't beat LR.

**Random Forest** — higher R2 but worse RMSE than LR. Tree based model didn't benefit from scaling. Outliers caused large individual mistakes that averaging couldn't fix.

**XGBoost** — best overall. Builds trees sequentially, each one fixing mistakes of the previous. Hunted down difficult houses RF averaged over. Edges LR by correcting the few remaining mistakes on unusual houses.

## Final Result
**XGBoost — RMSE 19,677 | MAE 14,181 | MAPE 9.4% | R2 0.88**

On average the model predicts house prices within 9.4% of actual value — comparable to real estate agent estimation accuracy.

## Biggest Insight
First baseline gave R2 0.86. After all data work, final R2 is 0.88. But RMSE dropped from 31,237 to 19,677 — a $11,560 improvement in actual dollar accuracy. Data quality mattered more than model choice.

## What I'd Do Differently
- Build baseline first before any cleaning — understand the data before fixing it
- Test models on both raw and cleaned data from the start
- Spend less time on individual column decisions, more on overall patterns