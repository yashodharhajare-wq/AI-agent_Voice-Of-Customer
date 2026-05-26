import pandas as pd

grouped = pd.read_pickle(
    r"C:\Users\yasho\Desktop\Mechanical Keyboard AI agent\outputs\discussions.pkl"
)

keywords = [
    "problem",
    "issue",
    "broken",
    "disconnect",
    "battery",
    "firmware",
    "recommend",
    "buy",
    "worth",
    "help",
    "fix"
]

for idx, row in grouped.iterrows():

    text = (
        str(row["Title"]) +
        " " +
        " ".join(row["Comment"])
    ).lower()

    if any(k in text for k in keywords):

        print("=" * 80)
        print("INDEX:", idx)
        print("TITLE:", row["Title"])
        print()