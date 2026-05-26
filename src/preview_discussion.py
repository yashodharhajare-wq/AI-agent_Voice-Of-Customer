import pandas as pd

grouped = pd.read_pickle(
     "C:\\Users\\yasho\\Desktop\\Mechanical Keyboard AI agent\\outputs\\discussions.pkl"
)

sample = grouped.iloc[0]

print("TITLE:")
print(sample["Title"])

print("\nCOMMENTS:\n")

for comment in sample["Comment"][:10]:
    print(comment)
    print()