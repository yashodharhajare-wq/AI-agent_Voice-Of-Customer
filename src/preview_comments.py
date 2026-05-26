import pandas as pd

df = pd.read_csv(r"C:\Users\yasho\Desktop\Mechanical Keyboard AI agent\data\MechanicalKeyboards_Comments.csv")

print("Rows:", len(df))
print("Columns:", list(df.columns))

print("\nTop 5 comments:")
print(df["Comment"].head())