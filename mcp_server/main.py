from fastapi import FastAPI, HTTPException, Query
from typing import Any, Dict

from weather_service import fetch_current_weather

app = FastAPI()


@app.get("/weather/current")
def get_current_weather(city: str = Query(..., description="City name, e.g. London")) -> Dict[str, Any]:
    """
    Get current weather for a given city.

    Query params:
    - city: name of the city (required)
    """
    try:
        weather = fetch_current_weather(city=city)
        return weather
    except RuntimeError as exc:
        # Raised when OPENWEATHER_API_KEY is missing
        raise HTTPException(status_code=500, detail=str(exc)) from exc

