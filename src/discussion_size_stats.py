import pandas as pd

grouped = pd.read_pickle(
    r"C:\Users\yasho\Desktop\Mechanical Keyboard AI agent\outputs\discussions.pkl"
)

print(grouped["comment_count"].describe())

print("\nLargest discussions:\n")

print(
    grouped[
        ["Title", "comment_count"]
    ]
    .sort_values(
        "comment_count",
        ascending=False
    )
    .head(20)
)