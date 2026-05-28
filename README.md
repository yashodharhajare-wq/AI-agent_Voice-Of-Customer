# Voice of Customer AI Intelligence Platform

### Transforming reddit Community Discussions into Actionable Product Intelligence using Local LLM model

🚀 **Live Demo:** https://voice-of-customer-ai-agent.streamlit.app/

📂 **GitHub Repository:** https://github.com/yashodharhajare-wq/voice-of-customer-ai-agent

---

## Overview

This project is an end-to-end Voice of Customer (VoC) Intelligence Platform that analyzes Reddit community discussions and converts unstructured conversations into structured product insights.

The system processes thousands of discussions, identifies conversations containing product feedback, extracts actionable insights using a local Large Language Model (LLM), normalizes recurring themes, and visualizes results through an interactive analytics dashboard.

The project demonstrates:

* LLM Engineering
* Prompt Engineering
* Data Processing Pipelines
* NLP-based Insight Extraction
* Product Analytics
* Dashboard Development
* Local AI Deployment using Ollama

---

## Problem Statement

Online communities contain valuable customer feedback, but extracting meaningful insights manually is time-consuming and difficult.

Product teams need answers to questions such as:

* What problems are users experiencing?
* What features do customers want?
* What benefits do users appreciate?
* Which user personas are most active?
* Which issues occur most frequently?

This project automates the process of converting community discussions into structured product intelligence.

---

## Dataset

### Source

Mechanical Keyboards Reddit Community

### Dataset Size

* 9,042 Reddit comments
* Multiple discussion threads
* User-generated product feedback

### Data Fields

* Discussion Title
* Comment Text
* Comment Score
* Post URL
* Discussion Metadata

---

## Architecture

```text
Reddit Discussions
        │
        ▼
Discussion Grouping
        │
        ▼
LLM Classification
        │
        ▼
Insight Extraction
        │
        ▼
Theme Normalization
        │
        ▼
Insight Aggregation
        │
        ▼
Interactive Dashboard
```

---

## Technology Stack

### AI / LLM

* Ollama
* Qwen 2.5 7B
* Prompt Engineering
* Structured JSON Extraction

### Data Processing

* Python
* Pandas
* NumPy

### Visualization

* Streamlit
* Plotly

### Development

* Git
* GitHub

---

## Pipeline

### 1. Discussion Grouping

Raw Reddit comments are grouped into discussion-level records.

Generated Metrics:

* Comment Count
* Average Score
* Maximum Score
* Discussion Metadata

Output:

```text
discussions.pkl
```

---

### 2. Discussion Classification

A local LLM classifies each discussion into categories:

* Complaint
* Praise
* Feature Request
* Buying Advice
* Technical Support
* Showcase
* Humor / Meme
* Community Discussion

Additional outputs:

* Contains Product Insights
* Confidence Score
* Classification Reason

Output:

```text
classified_discussions.pkl
```

---

### 3. Product Insight Extraction

The LLM extracts only explicitly discussed information.

Extracted Categories:

* Pain Points
* Gains
* Personas
* Must-Have Features
* Nice-To-Have Features
* Feature Requests

Design Goals:

* No hallucinations
* JSON-only responses
* Explicit evidence extraction
* Conservative output generation

Output:

```text
discussion_insights.pkl
```

---

### 4. Theme Normalization

Similar insights are merged into standardized themes.

Example:

```text
Bluetooth Issues
Bluetooth Connectivity Problems
Bluetooth Reliability Problems

↓
Bluetooth Reliability
```

Output:

```text
normalized_insights.pkl
```

---

### 5. Insight Aggregation

Normalized insights are aggregated to identify:

* Most Common Pain Points
* Most Requested Features
* Top User Personas
* Most Appreciated Benefits

---

## LLM Evaluation

Multiple local models were evaluated before selecting the final production model.

| Model       | Result   |
| ----------- | -------- |
| Gemma 3 4B  | Rejected |
| Qwen 3 8B   | Rejected |
| Qwen 2.5 7B | Selected |

### Selection Criteria

* JSON Reliability
* Schema Compliance
* Hallucination Rate
* Prompt Controllability
* Extraction Accuracy

### Final Choice

**Qwen 2.5 7B via Ollama**

Reasons:

* Consistent structured outputs
* Strong schema adherence
* Lower hallucination rate
* Reliable extraction behavior

---

## Dashboard Features

### KPI Overview

Displays:

* Total Discussions Analyzed
* Pain Point Discussions
* Gains Discussions
* Feature Request Discussions
* Persona Coverage
* Average Confidence Score

---

### Interactive Filters

Users can filter by:

* Discussion Type
* Minimum Confidence
* Minimum Comment Count
* Theme Frequency
* Keyword Search

---

### Analytics Tabs

#### Pain Points

Visualizes the most frequently mentioned customer problems.

#### Gains

Highlights benefits users appreciate.

#### Personas

Identifies recurring user segments.

#### Feature Requests

Displays the most requested product improvements.

#### Discussion Explorer

Allows exploration of individual discussions including:

* Title
* Discussion Type
* Engagement Metrics
* Confidence Score
* Reddit Link
* Extracted Insights

---

## Key Skills Demonstrated

### AI Engineering

* Local LLM Deployment
* Structured Prompt Engineering
* Hallucination Reduction
* JSON Schema Enforcement

### Data Engineering

* Pipeline Design
* Data Transformation
* Data Aggregation
* Feature Engineering

### Analytics

* Customer Insight Discovery
* Product Intelligence
* Trend Analysis

### Software Engineering

* Modular Architecture
* Reproducible Workflows
* Dashboard Development

---

## Repository Structure

```text
voice-of-customer-ai-agent/

├── dashboard/
│   └── app.py
│
├── src/
│   ├── run_classifier.py
│   ├── run_extractor.py
│   ├── normalize_themes.py
│   ├── analyze_insights.py
│
├── outputs/
│   └── normalized_insights.pkl
│
├── screenshots/
│
├── requirements.txt
│
└── README.md
```

---

## Results

The platform successfully transformed over 9,000 Reddit comments into structured product intelligence.

Generated insights include:

* Customer pain points
* Product strengths
* User personas
* Must-have features
* Feature requests

The resulting dashboard enables rapid exploration of community feedback and product opportunities.

---

## Future Improvements

### Recommendation Engine

Automatically generate product recommendations based on recurring customer issues.

Example:

```text
Pain Point:
Bluetooth Reliability

Mentions:
43 Discussions

Recommendation:
Improve reconnect speed and connection stability.
```

### Additional Data Sources

* Discord Communities
* Product Reviews
* Support Tickets
* Survey Responses

### Advanced Analytics

* Sentiment Analysis
* Trend Detection
* Topic Evolution Tracking
* Multi-community Comparison

---

## Running Locally

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/voice-of-customer-ai-agent.git
cd voice-of-customer-ai-agent
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Launch Dashboard

```bash
streamlit run dashboard/app.py
```

---

## Author

**Yashodhar Hajare**
