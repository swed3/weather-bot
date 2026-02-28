import requests
import time


class PolymarketFetcher:

    def __init__(self):
        self.base_url = "https://gamma-api.polymarket.com/markets"

    def safe_request(self, url, retries=3):

        for attempt in range(retries):
            try:
                response = requests.get(url, timeout=20)
                if response.status_code == 200:
                    return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt+1} failed:", e)
                time.sleep(2)

        return []

    def fetch_weather_markets(self):

        url = f"{self.base_url}?limit=50&active=true"

        markets = self.safe_request(url)

        weather_markets = []

        for market in markets:
            question = market.get("question", "").lower()

            if "temperature" in question:
                weather_markets.append(market)

        return weather_markets

    def fetch_nyc_market(self):

        weather_markets = self.fetch_weather_markets()

        for market in weather_markets:

            question = market.get("question", "").lower()

            if "new york" in question or "nyc" in question:

                outcomes = market.get("outcomes", [])

                parsed = []

                for o in outcomes:
                    try:
                        parsed.append({
                            "name": o["name"],
                            "price": float(o["price"])
                        })
                    except:
                        continue

                return {
                    "question": market["question"],
                    "outcomes": parsed
                }

        return None


if __name__ == "__main__":

    fetcher = PolymarketFetcher()

    print("\nScanning weather markets...\n")

    weather = fetcher.fetch_weather_markets()

    print(f"Weather markets found: {len(weather)}")

    for m in weather:
        print(m.get("question"))

    print("\nNYC Market:")
    print(fetcher.fetch_nyc_market())
