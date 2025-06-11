from guardrails_sdk import GuardrailsClient, ToxiRequest
import asyncio

req = {
    "content": "Hello this is viswateja from v@v.com and LC-123456 with 1234-5678-9012 and I am going to find you and kill you",
    
    "treshold": 0.5
}

#Creating a object for Guard rails SDK
client = GuardrailsClient()
#Request validation
request = ToxiRequest(**req)

async def main():
    result = await client.validate_content(request)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())