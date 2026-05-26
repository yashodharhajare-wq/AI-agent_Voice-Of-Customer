import json
import pandas as pd
import requests

print("Loading classified discussions...")

df = pd.read_pickle(
    r"C:\Users\yasho\Desktop\Mechanical Keyboard AI agent\outputs\classified_discussions.pkl"
)

# Only keep useful discussions
df = df[
    df["contains_product_insights"] == True
].copy()

print(f"Discussions to analyze: {len(df)}")

MODEL = "qwen2.5:7b"

results = []

for idx, row in df.iterrows():

    print(f"Processing {idx}")

    comments = row["Comment"]

    if len(comments) > 50:

        comments = (
            comments[:25]
            + comments[-25:]
        )

    discussion_text = f"""
TITLE:
{row['Title']}

COMMENTS:

{chr(10).join(comments)}
"""

    prompt = f"""
You are a Product Insights Extractor.

Return ONLY valid JSON.

Extract ONLY information explicitly discussed.

Do not invent information.
Do not infer information.

Definitions:

Pain Point:
A frustration, problem, complaint, limitation, or difficulty.

Gain:
A positive outcome, benefit, or thing users appreciate.

Persona:
A user type that is explicitly mentioned or clearly evidenced by discussion behavior.

Examples:
- Network Engineers
- Programmers
- Gamers
- Keyboard Enthusiasts
- Office Workers

Do not invent personas.
Must Have Feature:
A capability users consider essential.

Nice To Have Feature:
A capability users would like but do not consider essential.

Feature Request:
A requested feature, enhancement, or improvement.

Rules:

1. Use only information explicitly discussed.
2. Ignore jokes and memes.
3. Ignore off-topic conversations.
4. Merge similar ideas.
5. If none exist, return empty arrays.
6. Return valid JSON only.

Schema:

{{
  "pain_points": [],
  "gains": [],
  "personas": [],
  "must_have_features": [],
  "nice_to_have_features": [],
  "feature_requests": []
}}

DISCUSSION:

{discussion_text}
"""

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0
                }
            }
        )

        result = response.json()["response"]

        result = result.strip()

        if result.startswith("```json"):
            result = result.replace("```json", "", 1)

        if result.endswith("```"):
            result = result[:-3]

        result = result.strip()

        extracted = json.loads(result)

        results.append({
            # Core identifiers
            "ID": row["ID"],
            "Title": row["Title"],

            # Discussion metadata
            "Post URL": row["Post URL"],
            "discussion_type": row["discussion_type"],
            "confidence": row["confidence"],
            "reason": row["reason"],

            # Engagement metadata
            "comment_count": row["comment_count"],
            "avg_score": row["avg_score"],
            "max_score": row["max_score"],

            # Extracted insights
            "pain_points": extracted.get("pain_points", []),
            "gains": extracted.get("gains", []),
            "personas": extracted.get("personas", []),
            "must_have_features": extracted.get("must_have_features", []),
            "nice_to_have_features": extracted.get("nice_to_have_features", []),
            "feature_requests": extracted.get("feature_requests", [])
        })

    except Exception as e:

        print("ERROR:", e)

        results.append({
            # Core identifiers
            "ID": row["ID"],
            "Title": row["Title"],

            # Discussion metadata
            "Post URL": row["Post URL"],
            "discussion_type": row["discussion_type"],
            "confidence": row["confidence"],
            "reason": row["reason"],

            # Engagement metadata
            "comment_count": row["comment_count"],
            "avg_score": row["avg_score"],
            "max_score": row["max_score"],

            # Empty insights
            "pain_points": [],
            "gains": [],
            "personas": [],
            "must_have_features": [],
            "nice_to_have_features": [],
            "feature_requests": [],

            "error": str(e)
        })

insights_df = pd.DataFrame(results)

insights_df.to_pickle(
    r"C:\Users\yasho\Desktop\Mechanical Keyboard AI agent\outputs\discussion_insights.pkl"
)

print("\nSaved discussion_insights.pkl")