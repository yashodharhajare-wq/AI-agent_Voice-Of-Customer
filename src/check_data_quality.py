import pandas as pd

df = pd.read_csv(r"C:\Users\yasho\Desktop\Mechanical Keyboard AI agent\data\MechanicalKeyboards_Comments.csv")

print("Total comments:", len(df))

print("\nMissing comments:")
print(df["Comment"].isna().sum())

print("\nTop scored comments:")
print(
    df[["Score", "Comment"]]
    .sort_values(by="Score", ascending=False)
    .head(20)
)