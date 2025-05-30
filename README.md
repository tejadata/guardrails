# Guardrails

Guardrails are safety mechanisms and quality controls that help ensure Large Language Models (LLMs) behave in a predictable, secure, and responsible manner. They are essential for deploying LLM-powered applications in production, especially when dealing with sensitive data, user interactions, or regulatory compliance.

### 🛡️ Common Types of Guardrails

1. **Content Safety Filters**  
   Monitor and restrict LLM responses containing offensive, harmful, or unsafe language to maintain ethical and secure outputs.

2. **PII Detection & Redaction**  
   Automatically detect and mask sensitive personal information such as names, email addresses, phone numbers, and financial identifiers to ensure privacy and compliance.

3. **Custom Validation Rules**  
   Enforce domain-specific business logic by validating outputs against custom-defined rules, patterns, or formats.

4. **Topic Restrictions**  
   Block or flag content related to sensitive or restricted topics (e.g., politics, legal, health) using topic classification techniques.

5. **Structured Output Enforcement**  
   Ensure the LLM’s response adheres to required output formats such as JSON, XML, or predefined schema structures.

6. **Prompt Validation & Rate Control**  
   Safeguard the system from misuse by validating inputs and limiting the frequency or volume of requests from users.

# PII/PHI detection

A Python project for detecting and anonymizing Personally Identifiable Information (PII) in text using [Presidio](https://microsoft.github.io/presidio/). This project provides an API for analyzing and masking PII, with support for custom entity recognizers.

## Features

- Detects and anonymizes PII entities in text (e.g., names, credit cards, SSNs).
- Supports adding custom entity recognizers via regex.
- REST API built with FastAPI.

### Sample request

POST call to `localhost:8000/api/v1/mask_pii`

In the following request, the `custom_entities` field is optional. Users can include it to define their own custom regex patterns for entity detection if needed.

```json
{
  "content": "Hello this is viswateja from v@v.com and LC-123456 with 1234-5678-9012",
  "guardrails": ["EMAIL_ADDRESS"],
  "custom_entities": [
    {
      "entity_name": "CUSTOM_ACCOUNT_NUMBER",
      "regex": "\\b\\d{4}-\\d{4}-\\d{4}\\b",
      "score": 0.9
    },
    {
      "entity_name": "LOYALTY_CARD",
      "regex": "LC-\\d{6}"
    }
  ]
}
```

```json
{
  "pii_found": true,
  "masked_text": "Hello this is viswateja from <EMAIL_ADDRESS> and <LOYALTY_CARD> with <CUSTOM_ACCOUNT_NUMBER>"
}
```

# Toxicity Detection

This module provides an API and utility functions for detecting toxic language in text using the [unitary/toxic-bert](https://huggingface.co/unitary/toxic-bert) model from HuggingFace Transformers.

## Features

- Detects multiple types of toxicity, including:
  - General toxicity
  - Severe toxicity
  - Obscene language
  - Identity attacks
  - Insults
  - Threats
- Handles long texts by splitting into overlapping chunks.
- Returns both overall toxicity flag and per-label scores.

## Usage

**Sample Input**

```json
{
  "content": "Just checking toxicity, I am going to insult you and slap you",
  "treshold": 0.5
}
```

**Sample output:**

```json
{
  "is_toxic": true,
  "flagged_labels": {
    "toxicity": 0.8888218998908997,
    "identity_attack": 0.5717701315879822
  },
  "all_scores": {
    "toxicity": 0.8888218998908997,
    "severe_toxicity": 0.02928190864622593,
    "obscene": 0.07397100329399109,
    "identity_attack": 0.5717701315879822,
    "insult": 0.05923270061612129,
    "threat": 0.016223613172769547
  }
}
```

## API

- `detect_toxicity(text: str, threshold: float = 0.5) -> dict`
  - Returns a dictionary with:
    - `is_toxic`: `True` if any label exceeds the threshold.
    - `flagged_labels`: Labels and scores above the threshold.
    - `all_scores`: All toxicity scores.

---

## How to run in local

install all the requirements using requirement.txt file and run `uvicorn src.app:app --reload`
