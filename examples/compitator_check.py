from guardrails_sdk import GuardrailsClient, Compitator
import asyncio

req = {
    "content": "Hello this is viswateja from v@v.com and LC-123456 with 1234-5678-9012",
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
request = Compitator(**req)


async def main():
    result = await client.compitator_banned(request)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
