import asyncio
import os
from dotenv import load_dotenv
from main import real_physics_result

load_dotenv()

async def test():
    # Make sure we have a key
    if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY").startswith("sk-your-key"):
        print("Missing or invalid OPENAI_API_KEY. Skipping actual API call, but code loaded successfully.")
        return
        
    print("Testing OpenAI integration...")
    result = await real_physics_result("The earth is flat and rests on a giant turtle.")
    print("Result:")
    print(result.model_dump_json(indent=2))

if __name__ == "__main__":
    asyncio.run(test())
