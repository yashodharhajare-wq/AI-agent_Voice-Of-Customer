import streamlit as st
import pandas as pd
from collections import Counter
import plotly.express as px
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_pickle(
    BASE_DIR / "outputs" / "normalized_insights.pkl"
)

st.title("🎯 Voice of Customer - AI Intelligence Platform")

# Load data
df = pd.read_pickle(
    r"C:\Users\yasho\Desktop\Mechanical Keyboard AI agent\outputs\normalized_insights.pkl"
)

# ------------------------
# SIDEBAR
# ------------------------

st.sidebar.header("Filters")

discussion_types = sorted(
    df["discussion_type"]
    .dropna()
    .unique()
)

selected_type = st.sidebar.selectbox(
    "Discussion Type",
    ["All"] + list(discussion_types)
)

minimum_comments = st.sidebar.slider(
    "Minimum Comments",
    0,
    int(df["comment_count"].max()),
    0
)

minimum_confidence = st.sidebar.slider(
    "Minimum Confidence",
    0,
    10,
    0
)

minimum_mentions = st.sidebar.slider(
    "Minimum Theme Mentions",
    1,
    20,
    1
)

search_term = st.sidebar.text_input(
    "Search Theme"
)

filtered_df = df.copy()

if selected_type != "All":

    filtered_df = filtered_df[
        filtered_df["discussion_type"] == selected_type
    ]

filtered_df = filtered_df[
    filtered_df["comment_count"] >= minimum_comments
]

filtered_df = filtered_df[
    filtered_df["confidence"] >= minimum_confidence
]

# ------------------------
# KPI SECTION
# ------------------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Analyzed Discussions",
    len(filtered_df)
)

col2.metric(
    "Pain Point Discussions",
    sum(len(x) > 0 for x in filtered_df["pain_points"])
)

col3.metric(
    "Gains Discussions",
    sum(len(x) > 0 for x in filtered_df["gains"])
)

col4.metric(
    "Personas",
    sum(len(x) > 0 for x in filtered_df["personas"])
)

col5.metric(
    "Feature Request Discussions",
    sum(len(x) > 0 for x in filtered_df["feature_requests"])
)

col6 = st.columns(1)[0]

col6.metric(
    "Avg Confidence",
    round(
        filtered_df["confidence"].mean(),
        1
    )
)

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Pain Points",
        "Gains",
        "Personas",
        "Feature Requests",
        "Discussion Explorer"
    ]
)

# ------------------------
# COUNTER FUNCTION
# ------------------------

def count_items(column_name):

    counter = Counter()

    for row in filtered_df[column_name]:

        for item in row:

            counter[item] += 1

    return counter


# ------------------------
# PAIN POINTS
# ------------------------

with tab1:
    st.header("🔥 Top Pain Points")

    pain_counter = count_items("pain_points")

    pain_df = pd.DataFrame(
        pain_counter.most_common(10),
        columns=["Pain Point", "Count"]
    )

    pain_df.index = range(1, len(pain_df) + 1)
    pain_df.index.name = "Ranking"

    pain_df = pain_df[
        pain_df["Count"] >= minimum_mentions
    ]

    if search_term:
        pain_df = pain_df[
            pain_df["Pain Point"]
            .str.contains(
                search_term,
                case=False,
                na=False
            )
        ]

    fig = px.bar(
        pain_df,
        x="Count",
        y="Pain Point",
        orientation="h",
        title="Top Pain Points"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ------------------------
# GAINS
# ------------------------
with tab2:
    st.header("✅ Top Gains")

    gain_counter = count_items("gains")

    gain_df = pd.DataFrame(
        gain_counter.most_common(10),
        columns=["Gain", "Count"]
    )

    gain_df.index = range(1, len(gain_df) + 1)
    gain_df.index.name = "Ranking"

    gain_df = gain_df[
        gain_df["Count"] >= minimum_mentions
    ]

    if search_term:
        gain_df = gain_df[
            gain_df["Gain"]
            .str.contains(
                search_term,
                case=False,
                na=False
            )
        ]

    fig = px.bar(
        gain_df,
        x="Count",
        y="Gain",
        orientation="h",
        title="Top Gains"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ------------------------
# PERSONAS
# ------------------------
with tab3:

    st.header("👤 Top Personas")

    persona_counter = count_items("personas")

    persona_df = pd.DataFrame(
        persona_counter.most_common(10),
        columns=["Persona", "Count"]
    )

    persona_df.index = range(1, len(persona_df) + 1)
    persona_df.index.name = "Ranking"

    persona_df = persona_df[
        persona_df["Count"] >= minimum_mentions
    ]

    if search_term:
        persona_df = persona_df[
            persona_df["Persona"]
            .str.contains(
                search_term,
                case=False,
                na=False
            )
        ]

    fig = px.bar(
        persona_df,
        x="Count",
        y="Persona",
        orientation="h",
        title="Top Personas"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ------------------------
# FEATURE REQUESTS
# ------------------------
with tab4:

    st.header("🚀 Feature Requests")

    feature_counter = count_items(
        "feature_requests"
    )

    feature_df = pd.DataFrame(
        feature_counter.most_common(10),
        columns=["Feature Request", "Count"]
    )

    feature_df.index = range(1, len(feature_df) + 1)
    feature_df.index.name = "Ranking"

    feature_df = feature_df[
        feature_df["Count"] >= minimum_mentions
    ]

    if search_term:
        feature_df = feature_df[
            feature_df["Feature Request"]
            .str.contains(
                search_term,
                case=False,
                na=False
            )
        ]

    fig = px.bar(
        feature_df,
        x="Count",
        y="Feature Request",
        orientation="h",
        title="Top Feature Requests"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ------------------------
# Discussion Explorer
# ------------------------
with tab5:

    st.header("🔍 Discussion Explorer")

    selected_title = st.selectbox(
        "Choose Discussion",
        filtered_df["Title"].tolist()
    )

    selected_row = filtered_df[
        filtered_df["Title"] == selected_title
    ].iloc[0]

    # ------------------------
    # DISCUSSION TITLE
    # ------------------------

    st.subheader("Discussion Title")

    st.info(selected_row["Title"])
    st.subheader("Discussion Metadata")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Discussion Type",
        selected_row["discussion_type"]
    )

    col2.metric(
        "Comments",
        selected_row["comment_count"]
    )

    col3.metric(
        "Avg Score",
        round(selected_row["avg_score"], 1)
    )

    col4.metric(
        "Max Score",
        selected_row["max_score"]
    )

    st.subheader("Why This Discussion Was Selected")

    st.write(
        selected_row["reason"]
    )

    st.subheader("Original Discussion")

    st.link_button(
    "Open Reddit Discussion",
    selected_row["Post URL"])

    st.subheader("AI Confidence")

    confidence = float(selected_row["confidence"])

    st.progress(
        confidence / 10
    )

    st.write(
        f"Confidence Score: {confidence}/10"
    )
    # ------------------------
    # PAIN POINTS
    # ------------------------

    st.subheader("Pain Points")

    if selected_row["pain_points"]:
        for item in selected_row["pain_points"]:
            st.write(f"• {item}")
    else:
        st.write("No pain points identified")

    # ------------------------
    # GAINS
    # ------------------------

    st.subheader("Gains")

    if selected_row["gains"]:
        for item in selected_row["gains"]:
            st.write(f"• {item}")
    else:
        st.write("No gains identified")

    # ------------------------
    # PERSONAS
    # ------------------------

    st.subheader("Personas")

    if selected_row["personas"]:
        for item in selected_row["personas"]:
            st.write(f"• {item}")
    else:
        st.write("No personas identified")

    # ------------------------
    # FEATURE REQUESTS
    # ------------------------

    st.subheader("Feature Requests")

    if selected_row["feature_requests"]:
        for item in selected_row["feature_requests"]:
            st.write(f"• {item}")
    else:
        st.write("No feature requests identified")
