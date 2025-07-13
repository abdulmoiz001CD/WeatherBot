from agents import Agent, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel 
import requests
from dotenv import find_dotenv, get_key

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

# Rename this function to avoid confusion
def run_agent(message: str) -> str:
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful weather agent.",
        tools=[weather_tool],
        model=LitellmModel(
            model="gemini/gemini-2.0-flash",
            api_key=GEMINI_API_KEY
        )
    )

    result_agent = Runner.run_sync(agent, message)
    return result_agent.final_output
