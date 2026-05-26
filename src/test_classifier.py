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

TEST_INDEX = 251

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

# --------------------------------------------------
# PROMPT
# --------------------------------------------------

PROMPT = f"""
You are a Product Insights Classifier.

Your task is ONLY to classify the discussion.

You are NOT extracting pain points.
You are NOT generating recommendations.
You are NOT summarizing the discussion.

Always classify the ORIGINAL discussion.

Ignore side conversations, jokes, arguments,
and unrelated comment chains.

If the discussion contains multiple topics,
classify according to the dominant topic.

Examples:

A keyboard photo post with 100 comments discussing random things:
-> Showcase

A build photo post with some buying advice:
-> Showcase

A complaint post with jokes in the comments:
-> Complaint

Return ONLY valid JSON.

No markdown.

No explanations outside JSON.

Possible discussion types:

- Complaint
- Praise
- Feature Request
- Buying Advice
- Technical Support
- Showcase
- Humor/Meme
- Community Discussion

Definitions:

Complaint:
Users describing problems or frustrations.

Praise:
Users describing positive experiences.

Feature Request:
Users asking for features or improvements.

Buying Advice:
Users asking what product to buy.

Technical Support:
Users asking for help solving an issue.

Showcase:
Users showing a setup, keyboard, build, desk, photo, etc.

Humor/Meme:
Primarily jokes, sarcasm, memes, entertainment.

Community Discussion:
General discussion with little product feedback.

Rules:

1. Determine the primary discussion type.
2. Determine whether actionable product feedback exists.
3. If no actionable product feedback exists:
   contains_product_insights = false
4. Do not infer product issues.
5. Use only information explicitly present.
6. Return exactly one JSON object.
7. Do not create additional fields.

Confidence Rules:

Return confidence from 1 to 10.

1 = very uncertain classification
5 = somewhat confident
10 = extremely confident

Reason Rules:

Reason is required.

Reason must contain 1-2 sentences explaining:

- why the discussion was assigned this type
- why contains_product_insights is true or false

Output Requirements:

- confidence must be an integer from 1-10
- reason must never be empty
- all fields are required

Reason cannot be empty.

Schema:

{{
  "discussion_type": "Showcase",
  "contains_product_insights": false,
  "confidence": 8,
  "reason": "The discussion focuses on users sharing and discussing a keyboard setup rather than reporting product problems or requesting features."
}}

Your response MUST be parseable by:

json.loads(response)

Invalid responses are failures.

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