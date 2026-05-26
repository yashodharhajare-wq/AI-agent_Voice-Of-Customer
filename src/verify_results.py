import pandas as pd

df = pd.read_pickle(
    r"C:\Users\yasho\Desktop\Mechanical Keyboard AI agent\outputs\classified_discussions.pkl"
)

print(df["discussion_type"].value_counts())
print(
    df[
        ["Title", "discussion_type", "contains_product_insights"]
    ].head(50)
)
