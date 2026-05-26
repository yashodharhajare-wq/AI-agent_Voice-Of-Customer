import json
import pandas as pd
import requests

print("Starting classifier run...")

# --------------------------------------------------
# LOAD DISCUSSIONS
# --------------------------------------------------

grouped = pd.read_pickle(
    r"C:\Users\yasho\Desktop\Mechanical Keyboard AI agent\outputs\discussions.pkl"
)

# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

MODEL = "qwen2.5:7b"
MAX_COMMENTS = 50

results = []

# --------------------------------------------------
# PROCESS DISCUSSIONS
# --------------------------------------------------

for idx, sample in grouped.head(25).iterrows():

    print(f"Processing {idx + 1}/{len(grouped)}")

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

    prompt = f"""
You are a Product Insights Classifier.

Your task is ONLY to classify the discussion.

Always classify the ORIGINAL discussion.

Important:

Most discussions in this dataset are keyboard photos,
keyboard builds, desk setups, or hobby discussions.

If a user is showing a keyboard, setup, desk,
build, collection, or photo:

discussion_type = Showcase

Even if comments contain advice, opinions,
or side conversations.

Only use Technical Support if the original post
is asking for help solving a problem.

Only use Complaint if the original post
describes a problem or frustration.

Only use Buying Advice if the original post
asks what product to purchase.

Ignore side conversations, jokes, arguments,
and unrelated comment chains.

Possible discussion types:

- Complaint
- Praise
- Feature Request
- Buying Advice
- Technical Support
- Showcase
- Humor/Meme
- Community Discussion

Confidence Rules:

Return confidence from 1 to 10.

1 = very uncertain
10 = very certain

Reason Rules:

Reason is required.

Schema:

{{
  "discussion_type": "",
  "contains_product_insights": false,
  "confidence": 8,
  "reason": ""
}}

Return ONLY valid JSON.

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

        parsed = json.loads(result)

        results.append({
            "ID": sample["ID"],
            "Title": sample["Title"],

            # KEEP ORIGINAL DATA
            "Comment": sample["Comment"],
            "Score": sample["Score"],
            "Post URL": sample["Post URL"],

            "comment_count": sample["comment_count"],
            "avg_score": sample["avg_score"],
            "max_score": sample["max_score"],

            # CLASSIFIER OUTPUT
            "discussion_type": parsed.get("discussion_type"),
            "contains_product_insights": parsed.get("contains_product_insights"),
            "confidence": parsed.get("confidence"),
            "reason": parsed.get("reason")
        })

    except Exception as e:

        print("\n" + "=" * 80)
        print(f"ERROR ON DISCUSSION {idx}")
        print("=" * 80)

        print("TITLE:")
        print(sample["Title"])

        print("\nRAW MODEL RESPONSE:")
        print(result)

        print("\nERROR:")
        print(e)

        results.append({
            "ID": sample["ID"],
            "Title": sample["Title"],

            "Comment": sample["Comment"],
            "Score": sample["Score"],
            "Post URL": sample["Post URL"],

            "comment_count": sample["comment_count"],
            "avg_score": sample["avg_score"],
            "max_score": sample["max_score"],

            "discussion_type": "ERROR",
            "contains_product_insights": False,
            "confidence": 0,
            "reason": str(e)
        })

# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

classified_df = pd.DataFrame(results)

classified_df.to_pickle(
    r"C:\Users\yasho\Desktop\Mechanical Keyboard AI agent\outputs\classified_discussions.pkl"
)

print()
print("=" * 80)
print("CLASSIFICATION COMPLETE")
print("=" * 80)

print(f"Total discussions: {len(classified_df)}")

print(
    f"Contains product insights: "
    f"{classified_df['contains_product_insights'].sum()}"
)

print(
    f"No product insights: "
    f"{len(classified_df) - classified_df['contains_product_insights'].sum()}"
)

print("\nSaved classified_discussions.pkl")