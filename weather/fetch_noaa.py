import requests
from datetime import datetime

class NOAAHistoricalFetcher:

    def __init__(self):
        # Central Park NYC Official Station
        self.station_id = "USW00094728"
        self.base_url = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"
        self.token = "mVSjiXoEDhVINmPqWgVEiHqnzBWoJXxb"

    def fetch_feb_26_history(self, start_year=2010, end_year=2024):

        historical_temps = []

        for year in range(start_year, end_year + 1):

            date_str = f"{year}-02-26"

            params = {
                "datasetid": "GHCND",
                "stationid": f"GHCND:{self.station_id}",
                "startdate": date_str,
                "enddate": date_str,
                "datatypeid": "TMAX",
                "units": "standard",
                "limit": 1000
            }

            headers = {
                "token": self.token
            }

            try:
                response = requests.get(self.base_url, params=params, headers=headers, timeout=10)

                if response.status_code != 200:
                    print(f"No data available for {year}")
                    continue

                data = response.json()

                if "results" not in data:
                    print(f"No results for {year}")
                    continue

                temp = data["results"][0]["value"]
                historical_temps.append(temp)

            except Exception as e:
                print(f"Error fetching {year}: {e}")
                continue

        return historical_temps


# ---- Test Block ----
if __name__ == "__main__":

    fetcher = NOAAHistoricalFetcher()

    temps = fetcher.fetch_feb_26_history()

    print("\nFeb 26 Historical TMAX (°F):")
    print(temps)
