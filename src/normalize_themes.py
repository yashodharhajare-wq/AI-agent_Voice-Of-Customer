import json
import pandas as pd
import requests

print("Loading discussion insights...")

df = pd.read_pickle(
    r"C:\Users\yasho\Desktop\Mechanical Keyboard AI agent\outputs\discussion_insights.pkl"
)

MODEL = "qwen2.5:7b"

results = []

for idx, row in df.iterrows():

    print(f"Processing {idx}")

    prompt = f"""
You are a Theme Normalizer.

Convert extracted insights into short standardized themes.

Examples:

"Loud switches"
"Switches are too loud"
"Switch noise is annoying"

becomes

"Switch Noise"

---

"Typing IP addresses is difficult"
"Entering numbers on TKL is frustrating"

becomes

"Number Entry Difficulty"

Rules:

- Return concise themes
- Maximum 4 words per theme
- Merge duplicates
- Return valid JSON only

Schema:

{{
  "pain_points": [],
  "gains": [],
  "personas": [],
  "must_have_features": [],
  "nice_to_have_features": [],
  "feature_requests": []
}}

INPUT:

{json.dumps({
    "pain_points": row["pain_points"],
    "gains": row["gains"],
    "personas": row["personas"],
    "must_have_features": row["must_have_features"],
    "nice_to_have_features": row["nice_to_have_features"],
    "feature_requests": row["feature_requests"]
}, indent=2)}
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

        normalized = json.loads(result)

        results.append({
            "ID": row["ID"],
            "Title": row["Title"],

            # Discussion metadata
            "Post URL": row.get("Post URL"),
            "discussion_type": row.get("discussion_type"),
            "confidence": row.get("confidence"),
            "reason": row.get("reason"),

            # Engagement metadata
            "comment_count": row.get("comment_count"),
            "avg_score": row.get("avg_score"),
            "max_score": row.get("max_score"),

            "pain_points": normalized.get(
                "pain_points", []
            ),

            "gains": normalized.get(
                "gains", []
            ),

            "personas": normalized.get(
                "personas", []
            ),

            "must_have_features": normalized.get(
                "must_have_features", []
            ),

            "nice_to_have_features": normalized.get(
                "nice_to_have_features", []
            ),

            "feature_requests": normalized.get(
                "feature_requests", []
            )
        })

    except Exception as e:

        print("ERROR:", e)

        results.append({
            "ID": row["ID"],
            "Title": row["Title"],

            "Post URL": row.get("Post URL"),
            "discussion_type": row.get("discussion_type"),
            "confidence": row.get("confidence"),
            "reason": row.get("reason"),

            "comment_count": row.get("comment_count"),
            "avg_score": row.get("avg_score"),
            "max_score": row.get("max_score"),

            # fallback to original values
            "pain_points": row["pain_points"],
            "gains": row["gains"],
            "personas": row["personas"],
            "must_have_features": row["must_have_features"],
            "nice_to_have_features": row["nice_to_have_features"],
            "feature_requests": row["feature_requests"],

            "error": str(e)
        })

normalized_df = pd.DataFrame(results)

normalized_df.to_pickle(
    r"C:\Users\yasho\Desktop\Mechanical Keyboard AI agent\outputs\normalized_insights.pkl"
)

print("\nSaved normalized_insights.pkl")