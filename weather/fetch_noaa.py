import requests
from datetime import datetime

# ===============================
# CONFIG
# ===============================

STATION_ID = "USW00094728"   # NYC Central Park
BASE_URL = "https://www.ncei.noaa.gov/access/services/data/v1"


# ===============================
# INTERNAL NOAA FETCH
# ===============================

def fetch_noaa_history(month, day, start_year=2010, end_year=None):
    """
    Fetch historical Tmax for NYC for given month/day
    """

    if end_year is None:
        end_year = datetime.now().year - 1

    temps = []

    for year in range(start_year, end_year + 1):

        start_date = f"{year}-{month:02d}-{day:02d}"
        end_date = start_date

        params = {
            "dataset": "daily-summaries",
            "stations": STATION_ID,
            "startDate": start_date,
            "endDate": end_date,
            "dataTypes": "TMAX",
            "units": "standard",
            "format": "json"
        }

        try:
            response = requests.get(BASE_URL, params=params, timeout=15)

            if response.status_code != 200:
                continue

            data = response.json()

            if not data:
                continue

            value = data[0].get("TMAX")

            if value is not None:
                temps.append(value)

        except Exception:
            continue

    return temps


# ===============================
# ✅ SAFE EXPORT FUNCTION
# ===============================

def fetch_historical_tmax(month=2, day=26):
    """
    Cleaned historical Tmax values
    Used by:
    - Range Model
    - Backtester
    - Edge Engine
    """

    print("Fetching NOAA historical temperatures...")

    raw_data = fetch_noaa_history(month, day)

    cleaned = []

    for temp in raw_data:
        try:
            cleaned.append(float(temp))
        except:
            continue

    if not cleaned:
        print("WARNING: All historical values invalid.")

    return cleaned


# ===============================
# TEST RUN
# ===============================

if __name__ == "__main__":
    data = fetch_historical_tmax()
    print("\nHistorical Tmax:")
    print(data)
