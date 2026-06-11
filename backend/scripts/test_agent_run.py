import asyncio
from app.agent import root_agent
from google.adk.runners import InMemoryRunner
from google.genai import types

async def main():
    runner = InMemoryRunner(root_agent, app_name="scout")
    runner.auto_create_session = True
    
    # create new message
    content = types.Content(
        parts=[types.Part.from_text(text="What matches are Egypt playing?")]
    )
    
    print("Running agent...")
    async for event in runner.run_async(
        user_id="test-user",
        session_id="test-session",
        new_message=content
    ):
        print(f"Event: {event}")

if __name__ == "__main__":
    asyncio.run(main())
