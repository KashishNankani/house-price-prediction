**House Price Predictor — README**

**Problem:** Predict sale price of houses in Ames, Iowa using 80 features.

**Data:** 1460 houses, 80 columns — messy, missing values, skewed distributions, redundant features.

**What I did:**
- Dropped columns with 90%+ same value — no variation means nothing to learn
- Filled missing values with logic — neighbourhood median for LotFrontage, None for features that don't exist, median for unknowns
- Removed 54 luxury outliers above $350k — too few examples for model to learn from
- Combined redundant columns — 4 porch columns into TotalPorchSF, bathrooms into TotalBath
- Fixed skewed features with log transformation — LotArea had 11.18 skewness
- Standard scaling — ensured no feature dominated due to scale difference
- One hot encoding for categorical columns

**Models tested:** Linear Regression, Decision Tree, Random Forest

**Results:** Linear Regression won — RMSE 20,508, R2 0.87

**Biggest surprise:** 86% R2 on first baseline. All the data work only moved it to 87%. The data decisions reduced dollar error by $10,000 — from 31k to 20k RMSE. Model choice mattered less than data quality.

---
