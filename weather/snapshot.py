from weather.fetch_openmeteo import OpenMeteoFetcher
from config import CITIES


class WeatherSnapshotEngine:

    def fetch_all_cities(self):
        snapshot = {}

        for city_name, coords in CITIES.items():
            fetcher = OpenMeteoFetcher(coords["lat"], coords["lon"])
            data = fetcher.fetch_current_temperature()

            snapshot[city_name] = {
                "temperature": data["temperature"],
                "windspeed": data["windspeed"],
                "timestamp": data["timestamp"]
            }

        return snapshot


if __name__ == "__main__":
    engine = WeatherSnapshotEngine()
    data = engine.fetch_all_cities()
    print(data)
