from langchain.tools import tool
import requests

@tool
def get_current_weather(city: str) -> str:
    """
    Get the current weather for a given city.
    """
    response = requests.get(
        "http://localhost:8000/weather/current",
        params={"city": city}
    )
    return response.text