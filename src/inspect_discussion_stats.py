import pandas as pd

df = pd.read_csv(r"C:\Users\yasho\Desktop\Mechanical Keyboard AI agent\data\MechanicalKeyboards_Comments.csv")

print("Comments:", len(df))
print("Unique discussions:", df["ID"].nunique())

discussion_sizes = (
    df.groupby("ID")
      .size()
      .sort_values(ascending=False)
)

print("\nLargest discussions:")
print(discussion_sizes.head(10))