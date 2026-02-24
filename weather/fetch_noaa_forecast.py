import requests


class NOAAForecastFetcher:

    def __init__(self):
        self.base_url = "https://api.weather.gov"

    def get_forecast(self, lat, lon):

        # Step 1: Get grid endpoint
        point_url = f"{self.base_url}/points/{lat},{lon}"
        point_resp = requests.get(point_url, headers={"User-Agent": "weather-bot"})
        point_data = point_resp.json()

        forecast_url = point_data["properties"]["forecast"]

        # Step 2: Get forecast
        forecast_resp = requests.get(forecast_url, headers={"User-Agent": "weather-bot"})
        forecast_data = forecast_resp.json()

        periods = forecast_data["properties"]["periods"]

        # Extract daily highs only
        daily_highs = []

        for period in periods:
            if period["isDaytime"]:
                daily_highs.append({
                    "name": period["name"],
                    "temperature": period["temperature"]
                })

        return daily_highs


if __name__ == "__main__":

    # NYC coordinates
    LAT = 40.7128
    LON = -74.0060

    fetcher = NOAAForecastFetcher()
    data = fetcher.get_forecast(LAT, LON)

    for day in data:
        print(day)
