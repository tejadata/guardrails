from guardrails_sdk import GuardrailsClient, TransformRequest
import asyncio

req = {
    "content": "Hello this is viswateja from v@v.com and LC-123456 with 1234-5678-9012",
    "guardrails": [
        "EMAIL_ADDRESS"
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
    ],
    "action": "mask",
    "compitator_loc": "competitors.txt",
    "block_loc": "banned_words.txt"
}

# Creating a object for Guard rails SDK
client = GuardrailsClient()
# If you want to enable logging, you can pass the DSN for the database
# Enable logging by passing a DSN
# Replace <DSN> with your actual database connection string
"""client = GuardrailsClient(enable_logging=True, dsn=<DSN>)"""
# Request validation
request = TransformRequest(**req)


async def main():
    result = await client.run_all_guardrails(request)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
