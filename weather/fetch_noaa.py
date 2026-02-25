import requests
import os

BASE_URL = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"

# Put your NOAA API token here or use environment variable
TOKEN = os.getenv("NOAA_TOKEN", "mVSjiXoEDhVINmPqWgVEiHqnzBWoJXxb")


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

            try:
                response = requests.get(
                    BASE_URL,
                    headers=headers,
                    params=params,
                    timeout=10
                )

                if response.status_code != 200:
                    print(f"NOAA API unavailable for {year}")
                    print("Status Code:", response.status_code)
                    continue

                data = response.json()

                if "results" in data and len(data["results"]) > 0:
                    temps.append(data["results"][0]["value"])
                else:
                    print(f"No data available for {year}")

            except requests.exceptions.Timeout:
                print(f"Timeout fetching data for {year}")
                continue

            except requests.exceptions.RequestException as e:
                print(f"Network error for {year}: {e}")
                continue

        if len(temps) == 0:
            print("WARNING: No historical data fetched.")
            return []

        return temps


if __name__ == "__main__":

    station = "GHCND:USW00094728"  # NYC Central Park

    fetcher = NOAAHistoricalFetcher(station)
    temps = fetcher.fetch_feb26_history()

    print("\nFeb 26 Historical TMAX (°F):")
    print(temps)
