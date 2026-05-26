import pandas as pd

# Load dataset
df = pd.read_csv(
    r"C:\Users\yasho\Desktop\Mechanical Keyboard AI agent\data\MechanicalKeyboards_Comments.csv"
)

# Group discussions
grouped = (
    df.groupby("ID")
      .agg({
          "Title": "first",
          "Comment": list,
          "Score": list,
          "Post URL": "first"
      })
      .reset_index()
)

# Discussion statistics
grouped["comment_count"] = grouped["Comment"].apply(len)

grouped["avg_score"] = grouped["Score"].apply(
    lambda scores: sum(scores) / len(scores)
)

grouped["max_score"] = grouped["Score"].apply(max)

# Save output
grouped.to_pickle(
    r"C:\Users\yasho\Desktop\Mechanical Keyboard AI agent\outputs\discussions.pkl"
)

print(f"Comments: {len(df)}")
print(f"Discussions: {len(grouped)}")
print("\nSaved discussions.pkl")