import statistics
from weather.fetch_noaa import NOAAHistoricalFetcher
from engine.trade_decision import TradeDecision


class Backtester:

    def __init__(self, threshold=33, initial_bankroll=1000):
        self.threshold = threshold
        self.bankroll = initial_bankroll
        self.history = []

    def probability(self, data):
        count = sum(1 for x in data if x >= self.threshold)
        return count / len(data)

    def run(self):

        station = "GHCND:USW00094728"  # NYC Central Park
        fetcher = NOAAHistoricalFetcher(station)

        data = fetcher.fetch_feb26_history()

        print("Historical Data:", data)
        print("Total Years:", len(data))
        print("-------------")

        for i in range(10, len(data)):

            training_data = data[:i]
            test_value = data[i]

            prob = self.probability(training_data)

            market_price = 0.80  # simulated market price

            decision = TradeDecision.evaluate(prob, market_price)

            if decision["trade"]:

                stake = self.bankroll * 0.1
                self.bankroll -= stake

                if test_value >= self.threshold:
                    payout = stake
                else:
                    payout = 0

                pnl = payout - stake
                self.bankroll += payout

                self.history.append(pnl)

                print(
                    f"Year Index {i} | "
                    f"Prob={round(prob,3)} | "
                    f"Actual={test_value} | "
                    f"PnL={round(pnl,2)} | "
                    f"Bankroll={round(self.bankroll,2)}"
                )

            else:
                print(f"Year Index {i}: No trade")

        print("\nFinal Bankroll:", round(self.bankroll, 2))


if __name__ == "__main__":
    bt = Backtester()
    bt.run()
