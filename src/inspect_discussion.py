import pandas as pd

grouped = pd.read_pickle(
    r"C:\Users\yasho\Desktop\Mechanical Keyboard AI agent\outputs\discussions.pkl"
)

sample = grouped.iloc[0]

print("=" * 80)
print("DISCUSSION DETAILS")
print("=" * 80)

print(f"\nID:\n{sample['ID']}")

print(f"\nTITLE:\n{sample['Title']}")

print(f"\nPOST URL:\n{sample['Post URL']}")

print(f"\nCOMMENT COUNT:\n{sample['comment_count']}")

print(f"\nAVERAGE SCORE:\n{sample['avg_score']:.2f}")

print(f"\nMAX SCORE:\n{sample['max_score']}")

print("\nFIRST 10 COMMENTS:\n")

for i, comment in enumerate(sample["Comment"][:10], start=1):
    print("-" * 80)
    print(f"Comment {i}")
    print(comment)
    print()