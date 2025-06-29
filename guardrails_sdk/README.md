# README for Guardrails SDK

# Guardrails SDK

The Guardrails SDK is a Python library designed to facilitate interaction with the Guardrails API. It provides a simple and intuitive interface for developers to integrate safety mechanisms and quality controls into their applications powered by Large Language Models (LLMs).

## Features

- **Content Validation**: Validate user-generated content against specified guardrails to ensure safety and compliance.
- **PII Detection & Masking**: Automatically detect and mask Personally Identifiable Information (PII) in text to protect user privacy.
- **Toxicity Detection**: Identify and flag toxic language in user inputs to maintain a safe environment.
- **Compitator mention**: Detects user-specified competitor-related words or phrases in the text.
- **Anomoly logging**: anomoly detected by SDK can be logged to postgress or MySQL for further analysis

## Installation

You can install the Guardrails SDK using pip. Run the following command:

```bash
pip install guardrails-sdk
```

# Sample request

### 🧾 Field Descriptions

| Field             | Type           | Description                                                                                                                                    |
| ----------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `content`         | `string`       | The raw input text that you want to send to LLM.                                                                                               |
| `guardrails`      | `List[string]` | List of **built-in or custom entity types** to apply masking on. Examples: `"EMAIL_ADDRESS"`, `"PHONE_NUMBER"`, `"CUSTOM_ACCOUNT_NUMBER"` etc. |
| `treshold`        | `float`        | The minimum confidence score (0.0 - 1.0) to consider a match valid. Defaults to `0.5`.                                                         |
| `custom_entities` | `List[Dict]`   | A list of **custom entity matchers** defined using regular expressions. Each entry describes a user-defined entity.                            |

---

### 🔧 `custom_entities` Object Fields

| Subfield      | Required | Description                                                                                                 |
| ------------- | -------- | ----------------------------------------------------------------------------------------------------------- |
| `entity_name` | ✅ Yes   | A unique name/label for your custom entity. Should also be listed in the `guardrails` array to take effect. |
| `regex`       | ✅ Yes   | The regular expression pattern used to detect the custom entity in the input text.                          |
| `score`       | ❌ No    | Optional confidence score (between 0.0 and 1.0). If not provided, default logic will be used.               |

### Sample request

```json
{
  "content": "Hello this is viswateja from v@v.com and LC-123456 with 1234-5678-9012",
  "guardrails": ["EMAIL_ADDRESS", "CUSTOM_ACCOUNT_NUMBER", "LOYALTY_CARD"],
  "treshold": 0.5,
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

## Usage

Here’s a quick example of how to use the Guardrails SDK: The below code snippet helps to run all the guard rails provided by SDK

```python
from guardrails_sdk import GuardrailsClient, TransformRequest
import asyncio

req = {
    "content": "Hello this is viswateja from v@v.com and LC-123456 with 1234-5678-9012",
    "guardrails": [
        "EMAIL_ADDRESS","CUSTOM_ACCOUNT_NUMBER","LOYALTY_CARD"
    ],
    "treshold": 0.5,
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


async def main():
    client = GuardrailsClient()
    request = TransformRequest(**req)
    res = await client.run_all_guardrails(request)
    print(res)

if __name__ == "__main__":
    asyncio.run(main())
```

## 📘 API Reference

working examples can be found here https://github.com/tejadata/guardrails/tree/main/examples

### `GuardrailsClient`

A class to run various content safety guardrails such as PII masking, toxicity detection, and prompt injection classification.

---

#### `validate_content(request: ToxiRequest) -> Dict`

Detects **toxic content** in the input text based on the given threshold.

##### 🔸 Parameters:

- `request: ToxiRequest`
  - `content` (str): Input text to analyze.
  - `treshold` (float, optional): Confidence threshold for toxicity detection. Default is `0.5`.

##### 🔸 Returns:

- `Dict`: Result of toxicity analysis (e.g., toxicity score and classification).

---

#### `transform_content(request: TransformRequest) -> Dict`

Analyzes and masks **PII or other custom entities** in the text based on the specified guardrails.

##### 🔸 Parameters:

- `request: TransformRequest`
  - `content` (str): Input text to scan and mask.
  - `guardrails` (List[str]): List of built-in or custom entity types to mask (e.g., `"EMAIL_ADDRESS"`, `"PHONE_NUMBER"`).
  - `treshold` (float, optional): Confidence threshold for entity detection. Default is `0.5`.
  - `custom_entities` (List[Dict], optional): Custom entity definitions using regex patterns.

##### 🔸 Returns:

- `Dict`: Original and masked text, along with metadata for detected entities.

---

#### `prompt_injection(request: Prompt) -> Dict`

Classifies the input text to detect **prompt injection attacks** in LLM interactions.

##### 🔸 Parameters:

- `request: Prompt`
  - `content` (str): Prompt input to classify.

##### 🔸 Returns:

- `Dict`: Classification label and confidence score for whether the prompt is a potential injection.

---

#### `run_all_guardrails(request: TransformRequest) -> Dict`

Executes **all guardrails** (`PII masking`, `toxicity detection`, and `prompt injection detection`) in parallel.

##### 🔸 Parameters:

- `request: TransformRequest` (same as above)

##### 🔸 Returns:

- `Dict`: Combined output for:
  - `"pii"`: Masked content and entity info
  - `"toxicity"`: Toxicity classification
  - `"prompt_injection"`: Prompt injection status

# Anomaly Logging

This SDK uses SQLAlchemy and logs in to DB in async fashion to avoid adding latency for response. It supports both **PostgreSQL** and **MySQL**.

## 🔧 Database Configuration

To store anomalies, configure the **DSN (Database Source Name)** using the appropriate format depending on your database system.

### How to enable DB logging

when initilizing guardrails client

```python
client = GuardrailsClient(enable_logging=True, dsn=<DSN>)
```

### 🔧 PostgreSQL Configuration

Make sure you install the required driver

```bash
pip install psycopg2-binary
```

### ✅ DSN Format

```
postgresql+psycopg2://<username>:<password>@<host>:<port>/<database_name>
```

## 🔧 MySQL Configuration

Make sure you install the required driver:

```bash
pip install pymysql
```

### ✅ DSN Format

```
mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the terms of the Apache License 2.0. See the LICENSE file for details.
