## WeatherBot

## Description
WeatherBot is a Python-based chatbot that provides real-time weather updates for any city using the WeatherAPI. Powered by the Gemini language model and the agents library, it offers a simple, extensible way to query weather data conversationally.

## Features
- Fetch current weather (temperature and conditions) by city.
- Natural language processing via Gemini API.
- Secure API key management with .env.
- Easy-to-extend tool-based architecture.
- **Streaming support**: Weather responses are now streamed in real time for a more responsive user experience.

## Tech Stack
Python 3.8+

Libraries: agents, litellm, requests, python-dotenv

APIs: WeatherAPI, Gemini

## Installation
Clone the repository:
git clone https://github.com/abdulmoiz001CD/weatherbot.git
cd weatherbot

## Set up a virtual environment (optional):
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

## Install dependencies:
pip install requests python-dotenv agents litellm
Create a .env file with API keys:

GEMINI_API_KEY=your_gemini_api_key
WEATHER_API_KEY=your_weather_api_key

## Usage
Run the chatbot:

python main.py
Query the weather (basic call):
python

from chatbot import run_agent
print(run_agent("Weather in Paris"))
# Output: The weather in Paris is 20°C and Sunny.

Streamed weather updates (using Chainlit):
WeatherBot now supports real-time streaming using Chainlit. To run with streaming:

chainlit run main.py
This launches a web interface where messages are streamed as they are generated, providing a smoother interaction.

## License
MIT License. See LICENSE for details.

