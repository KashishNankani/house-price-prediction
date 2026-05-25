import pandas as pd

# Load the dataset
df = pd.read_csv("test.csv")
print(df.shape)

# missing = df.isnull().sum()
# missing = missing[missing > 0].sort_values(ascending=False)
# print(missing)

# percent_missing = (df.isnull().sum() / len(df)) * 100
# percent_missing = percent_missing[percent_missing > 0].sort_values(ascending=False)
# print(percent_missing)

# See all columns with very low variation
# for col in df.columns:
#     top_value_percent = df[col].value_counts(normalize=True).iloc[0] * 100
#     if top_value_percent > 90:
#         print(f"{col}: {top_value_percent:.1f}% same value")


print(df["SaleType"].value_counts())

print(df[df['SaleType'].isna()])

print("only the missing value in that row")
print(df[df['SaleType'].isna()]['SaleType'].value_counts())

print(df.loc[234])