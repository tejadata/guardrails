# Guardrails

# PII/PHI detection

A Python project for detecting and anonymizing Personally Identifiable Information (PII) in text using [Presidio](https://microsoft.github.io/presidio/). This project provides an API for analyzing and masking PII, with support for custom entity recognizers.

## Features

- Detects and anonymizes PII entities in text (e.g., names, credit cards, SSNs).
- Supports adding custom entity recognizers via regex.
- REST API built with FastAPI.

### Sample request

POST call to `localhost:8000/api/v1/transform`

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

## How to run in local

install all the requirements using requirement.txt file and run `uvicorn src.app:app --reload`
