from datetime import datetime
from typing import List, Dict

from requests import get as requests_get
from miru import init, start, listen


WEATHERAPI_KEY = "YOUR_API_KEY"

@listen
def get_weather_forecast(city: str) -> List[Dict]:
    """
    Returns weather forecast for given city.

    Parameters:
    - city: City name.

    Returns:
    - List: List of weather forecast.
    """
    response = requests_get(
        f"https://api.weatherapi.com/v1/forecast.json?key={WEATHERAPI_KEY}&q={city}&days=6&aqi=no&alerts=no",
        timeout=5
    )

    data = response.json()

    if "error" in data:
        raise Exception(data["error"]["message"])

    forecast = []

    for day in data["forecast"]["forecastday"]:
        date = datetime.strptime(day["date"], "%Y-%m-%d").strftime("%A")
        temp = round(day["day"]["maxtemp_c"])
        condition = day["day"]["condition"]["text"]
        wind = day["day"]["maxwind_mph"]
        humidity = day["day"]["avghumidity"]

        forecast.append({
            "date": date,
            "temp": temp,
            "condition": condition,
            "wind": wind,
            "humidity": humidity,
        })

    return forecast

if __name__ == "__main__":
    init(
        size=(1050, 750),
        port=8585,
    )

    start()
