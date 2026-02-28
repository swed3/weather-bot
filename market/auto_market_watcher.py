import time
from market.fetch_polymarket import PolymarketFetcher
from engine.trading_system import TradingSystem


class AutoMarketWatcher:

    def __init__(self, check_interval=300):
        """
        check_interval = seconds between scans
        default = 5 minutes
        """
        self.fetcher = PolymarketFetcher()
        self.system = TradingSystem()
        self.check_interval = check_interval

    def run(self):

        print("=== AUTO MARKET WATCHER STARTED ===")

        while True:
            try:
                print("\nScanning Polymarket weather markets...")

                market = self.fetcher.fetch_weather_markets()

                if market:
                    print("✅ Active market detected!")
                    print(market)

                    prices = market.get("prices", {})
                    actual_temp = None

                    self.system.run(
                        market_prices=prices,
                        actual_temp=actual_temp
                    )

                else:
                    print("⏳ No active NYC weather market yet.")

            except Exception as e:
                print("Watcher Error:", e)

            print(f"Sleeping {self.check_interval} seconds...\n")
            time.sleep(self.check_interval)


if __name__ == "__main__":
    watcher = AutoMarketWatcher()
    watcher.run()
