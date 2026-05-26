import json
import pandas as pd
import requests

print("Starting script...")
# Load grouped discussions
grouped = pd.read_pickle(
    r"C:\Users\yasho\Desktop\Mechanical Keyboard AI agent\outputs\discussions.pkl"
)

# Select one discussion
sample = grouped.iloc[0]

discussion_text = f"""
TITLE:
{sample['Title']}

COMMENTS:

{chr(10).join(sample['Comment'])}
"""

PROMPT = f"""
You are a Product Insights Analyst.

IMPORTANT:

Return ONLY valid JSON.

Do not return markdown.
Do not return explanations.
Do not return text before or after the JSON.

Use ONLY the fields defined in the schema.

Do not create additional fields.

If a field has no information, return an empty list.

If the discussion is mainly humor, memes, social interaction,
or hobby culture with no actionable product feedback:

- set contains_product_insights to false
- leave all insight lists empty

Do not infer product issues that are not explicitly discussed.

Rules:

1. Ignore jokes and memes.
2. Focus on product insights.
3. Merge similar ideas into themes.
4. Rate importance from 1-10.
5. Return JSON only.
6. Do not use markdown.

7. First determine whether the discussion contains
   meaningful product feedback.

8. If the discussion is mainly jokes, memes, social interaction,
hobby culture, or unrelated conversation, set:

"contains_product_insights": false

9. Provide a confidence score from 1-10.

10. Explain your reasoning briefly.

11. If contains_product_insights is false,
    leave all insight lists empty.
  
12. Do not invent pain points, gains, or feature requests
if they are not explicitly discussed.


Schema:

{{
  "contains_product_insights": true,
  "confidence": 1,
  "reason": "",

  "pain_points": [
    {{
      "theme": "",
      "importance": 1
    }}
  ],

  "gains": [
    {{
      "theme": "",
      "importance": 1
    }}
  ],

  "personas": [],

  "must_haves": [],

  "nice_to_haves": [],

  "feature_requests": [],

  "summary": ""
}}

DISCUSSION:

{discussion_text}
"""
models = [
    "qwen2.5:7b",
    "qwen3:8b"
]

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

    print(result)