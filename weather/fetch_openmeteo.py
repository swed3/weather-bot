import requests
from datetime import datetime


class OpenMeteoFetcher:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def fetch_current_temperature(self):
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current_weather": True
        }

        response = requests.get(self.BASE_URL, params=params, timeout=10)

        if response.status_code != 200:
            raise Exception(f"OpenMeteo API error: {response.status_code}")

        data = response.json()

        if "current_weather" not in data:
            raise Exception("Invalid API response structure")

        temperature = data["current_weather"]["temperature"]
        windspeed = data["current_weather"]["windspeed"]
        timestamp = data["current_weather"]["time"]

        return {
            "temperature": temperature,
            "windspeed": windspeed,
            "timestamp": timestamp,
            "fetched_at": datetime.utcnow().isoformat()
        }


if __name__ == "__main__":
    # Example test: Dallas
    dallas = OpenMeteoFetcher(32.7767, -96.7970)
    result = dallas.fetch_current_temperature()
    print(result)
