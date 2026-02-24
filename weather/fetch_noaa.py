import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("NOAA_TOKEN")
BASE_URL = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"


class NOAAHistoricalFetcher:

    def __init__(self, station_id):
        self.station_id = station_id

    def fetch_feb26_history(self, start_year=2011, end_year=2025):
        headers = {"token": TOKEN}
        temps = []

        for year in range(start_year, end_year + 1):

            date_str = f"{year}-02-26"

            params = {
                "datasetid": "GHCND",
                "datatypeid": "TMAX",
                "stationid": self.station_id,
                "startdate": date_str,
                "enddate": date_str,
                "units": "standard",
                "limit": 1000
            }

            response = requests.get(BASE_URL, headers=headers, params=params)

            if response.status_code != 200:
                print("Error:", response.status_code, response.text)
                continue

            data = response.json()

            if "results" in data and len(data["results"]) > 0:
                temps.append(data["results"][0]["value"])

        return temps


if __name__ == "__main__":

    station = "GHCND:USW00094728"  # NYC Central Park

    fetcher = NOAAHistoricalFetcher(station)
    temps = fetcher.fetch_feb26_history()

    print("Feb 26 Historical TMAX (°F):")
    print(temps)
