import os
import requests
from dotenv import load_dotenv
load_dotenv()

def fetch_current_weather(city: str, country_code: str | None = None, units: str = "metric") -> dict:
    """
    Fetch current weather for a city from OpenWeather API.

    :param city: City name (e.g. "London")
    :param country_code: Optional country code (e.g. "GB")
    :param units: "metric", "imperial", or "standard"
    :return: Parsed JSON response as a dict
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENWEATHER_API_KEY environment variable is not set")

    query = f"{city},{country_code}" if country_code else city

    params = {
        "q": query,
        "appid": api_key,
        "units": units,
    }

    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params=params,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()