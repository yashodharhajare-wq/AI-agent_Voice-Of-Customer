from collections import Counter
import pandas as pd

df = pd.read_pickle(
    r"C:\Users\yasho\Desktop\Mechanical Keyboard AI agent\outputs\normalized_insights.pkl"
)

pain_point_counter = Counter()
gain_counter = Counter()
personas_counter = Counter()
must_have_features_counter = Counter()
nice_to_have_features_counter = Counter()
feature_requests_counter = Counter()

for _, row in df.iterrows():

    for item in row.get("pain_points", []) or []:
        pain_point_counter[item] += 1

    for item in row.get("gains", []) or []:
        gain_counter[item] += 1

    for item in row.get("personas", []) or []:
        personas_counter[item] += 1

    for item in row.get("must_have_features", []) or []:
        must_have_features_counter[item] += 1

    for item in row.get("nice_to_have_features", []) or []:
        nice_to_have_features_counter[item] += 1

    for item in row.get("feature_requests", []) or []:
        feature_requests_counter[item] += 1

print("Total discussions:", len(df))

print(
    "Discussions with pain points:",
    (df["pain_points"].apply(len) > 0).sum()
)

print(
    "Discussions with gains:",
    (df["gains"].apply(len) > 0).sum()
)

print(
    "Discussions with feature requests:",
    (df["feature_requests"].apply(len) > 0).sum()
)

print("\nTOP PAIN POINTS\n")

for item, count in pain_point_counter.most_common(20):
    print(count, "-", item)

print("\nTOP GAINS\n")

for item, count in gain_counter.most_common(20):
    print(count, "-", item)

print("\nTOP FEATURE REQUESTS\n")

for item, count in feature_requests_counter.most_common(20):
    print(count, "-", item)

print("\nTOP PERSONAS\n")

for item, count in personas_counter.most_common(20):
    print(count, "-", item)

print("\nTOP MUST-HAVE FEATURES\n")

for item, count in must_have_features_counter.most_common(20):
    print(count, "-", item)

print("\nTOP NICE-TO-HAVE FEATURES\n")

for item, count in nice_to_have_features_counter.most_common(20):
    print(count, "-", item)