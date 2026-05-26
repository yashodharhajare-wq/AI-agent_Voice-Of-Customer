import pandas as pd

df = pd.read_csv(r"C:\Users\yasho\Desktop\Mechanical Keyboard AI agent\data\MechanicalKeyboards_Comments.csv")

print("Rows:", len(df))

print("\nHighest upvoted comments:")
print(
    df[["Score", "Comment"]]
    .sort_values("Score", ascending=False)
    .head(10)
)