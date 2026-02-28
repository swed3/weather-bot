import random
from weather.fetch_noaa import fetch_historical_tmax
from engine.range_model import RangeProbabilityModel
from engine.auto_trade import AutoTradeDecision


class WeatherBacktester:

    def __init__(self, station="USW00094728"):
        self.station = station
        self.balance = 1000
        self.trade_size = 50
        self.history = []

    def simulate_market_prices(self):
        """
        Fake historical polymarket prices
        (later real data replace hoga)
        """

        buckets = [
            "34-35",
            "36-37",
            "38-39",
            "40-41",
            "42-43",
            "44-45",
            "46-47",
            ">=48",
        ]

        prices = {}

        for b in buckets:
            prices[b] = round(random.uniform(0.05, 0.60), 2)

        return prices

    def run_day(self):

        temps = fetch_historical_tmax()

        if not temps:
            print("No NOAA data")
            return

        model = RangeProbabilityModel(temps)
        probs = model.calculate_probabilities()

        market_prices = self.simulate_market_prices()

        trader = AutoTradeDecision("NYC")
        signal = trader.generate_signal(market_prices)

        if not signal["trade"]:
            return

        bucket = signal["bucket"]

        model_prob = probs.get(bucket, 0)
        market_price = market_prices.get(bucket, 0)

        edge = model_prob - market_price

        pnl = edge * self.trade_size * 100

        self.balance += pnl

        self.history.append(pnl)

    def run_backtest(self, days=100):

        print("=== STARTING BACKTEST ===")

        for _ in range(days):
            self.run_day()

        total_pnl = sum(self.history)

        win_rate = len(
            [p for p in self.history if p > 0]
        ) / max(len(self.history), 1)

        print("\n=== RESULTS ===")
        print("Final Balance:", round(self.balance, 2))
        print("Total PnL:", round(total_pnl, 2))
        print("Trades:", len(self.history))
        print("Win Rate:", round(win_rate * 100, 2), "%")


if __name__ == "__main__":
    bt = WeatherBacktester()
    bt.run_backtest(days=200)
