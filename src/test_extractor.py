import json
import pandas as pd
import requests

print("Starting classifier test...")

# Load grouped discussions
grouped = pd.read_pickle(
    r"C:\Users\yasho\Desktop\Mechanical Keyboard AI agent\outputs\discussions.pkl"
)

# --------------------------------------------------
# SELECT DISCUSSION TO TEST
# --------------------------------------------------

TEST_INDEX = 383

sample = grouped.iloc[TEST_INDEX]

print("=" * 80)
print("INDEX:", TEST_INDEX)
print("TITLE:", sample["Title"])
print("COMMENT COUNT:", sample["comment_count"])
print("=" * 80)
print()

# --------------------------------------------------
# LIMIT VERY LARGE DISCUSSIONS
# --------------------------------------------------

MAX_COMMENTS = 50

comments = sample["Comment"]

if len(comments) > MAX_COMMENTS:
    comments = (
        comments[:MAX_COMMENTS // 2]
        + comments[-MAX_COMMENTS // 2:]
    )

discussion_text = f"""
TITLE:
{sample['Title']}

COMMENT COUNT:
{sample['comment_count']}

COMMENTS:

{chr(10).join(comments)}
"""

PROMPT = f"""
You are a Product Insights Extractor.

Your task is to extract ONLY information that is explicitly discussed.

Do not invent information.

Do not infer product problems.

Do not create recommendations.

Return ONLY valid JSON.

No markdown.

Focus only on:

1. Pain Points
2. Gains
3. Feature Requests

Definitions:

Pain Point:
A problem, frustration, complaint, limitation, or issue.

Gain:
Something users explicitly like, appreciate, enjoy, or praise.

Feature Request:
A requested feature, enhancement, or improvement.

Rules:

1. Use only information explicitly mentioned.
2. Ignore jokes and memes.
3. Ignore off-topic conversations.
4. Merge similar ideas.
5. If none exist, return empty arrays.
6. Return valid JSON only.

Schema:

{{
  "pain_points": [],
  "gains": [],
  "feature_requests": []
}}

DISCUSSION:

{discussion_text}
"""

# --------------------------------------------------
# MODEL
# --------------------------------------------------

models = [
    "qwen2.5:7b"
]

# --------------------------------------------------
# RUN
# --------------------------------------------------

for model in models:

    print("\n" + "=" * 80)
    print("MODEL:", model)
    print("=" * 80)

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": PROMPT,
            "stream": False,
            "options": {
                "temperature": 0
            }
        }
    )

    result = response.json()["response"]

    try:

        parsed = json.loads(result)

        print("VALID JSON\n")
        print(json.dumps(parsed, indent=2))

    except Exception as e:

        print("INVALID JSON")
        print("ERROR:", e)
        print()
        print(result)