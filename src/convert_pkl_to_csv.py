import pandas as pd

grouped = pd.read_pickle(
     "C:\\Users\\yasho\\Desktop\\Mechanical Keyboard AI agent\\outputs\\classified_discussions.pkl"
)


# Save as CSV
grouped.to_csv("C:\\Users\\yasho\\Desktop\\Mechanical Keyboard AI agent\\outputs\\output.csv", index=False)

print("Conversion completed!")
