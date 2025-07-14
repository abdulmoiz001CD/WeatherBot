from agents import Agent, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel 
import requests
from dotenv import find_dotenv, get_key
import json

# Load Gemini API key from .env file
GEMINI_API_KEY = get_key(find_dotenv(), "GEMINI_API_KEY")

@function_tool
def weather_tool(city: str) -> str:
    """Weather Identifier"""
    result = requests.get(
        f"http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}"
    )

    if result.status_code == 200:
        data = result.json()
        return f"The weather in {city} is {data['current']['temp_c']}°C and {data['current']['condition']['text']}."
    else:
        return "The request could not be fulfilled."

async def run_agent(message: str) -> str:
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful weather agent. When a user asks about the weather, use the weather_tool and return ONLY the tool's output string (e.g., 'The weather in <city> is <temp>°C and <condition>.') without any JSON wrapping, metadata, or additional text.",
        tools=[weather_tool],
        model=LitellmModel(
            model="gemini/gemini-2.0-flash",
            api_key=GEMINI_API_KEY
        )
    )

    result_agent = Runner.run_streamed(agent, message)
    accumulated_tokens = ""  # To accumulate tokens for JSON parsing
    async for event in result_agent.stream_events():
        if event.type == "raw_response_event" and hasattr(event.data, 'delta'):
            token = event.data.delta
            # Skip tokens that are part of unwanted metadata (e.g., "OK")
            if token == "OK":
                continue
            accumulated_tokens += token
            # Try to parse accumulated tokens as JSON to extract the content
            try:
                parsed = json.loads(accumulated_tokens)
                if isinstance(parsed, dict) and "weather_tool_response" in parsed and "content" in parsed["weather_tool_response"]:
                    yield parsed["weather_tool_response"]["content"]
                    accumulated_tokens = ""  # Reset after yielding content
            except json.JSONDecodeError:
                # If not valid JSON yet, continue accumulating
                # Yield tokens that are part of the weather response (heuristic)
                if "weather in" in token.lower() or "°C" in token or any(cond in token.lower() for cond in ["clear", "cloudy", "rain", "thunder", "sunny", "overcast"]):
                    yield token