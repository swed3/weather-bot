from engine.auto_trade import AutoTradeDecision
from engine.kelly_engine import KellyEngine
from execution.paper_trader import PaperTrader
from performance.metrics import PerformanceTracker


class TradingSystem:

    def __init__(self, station_id, bankroll=1000):
        self.station_id = station_id
        self.bankroll = bankroll

        self.edge_threshold = 0.05
        self.kelly_fraction = 0.5

        self.trader = AutoTradeDecision(station_id, self.edge_threshold)
        self.kelly = KellyEngine(self.kelly_fraction)
        self.paper = PaperTrader(bankroll)
        self.performance = PerformanceTracker(bankroll)

    def run(self, market_prices):

        print("\n=== Running Trading System ===")

        signal = self.trader.generate_signal(market_prices)
        print("Signal:", signal)

        if not signal["trade"]:
            print("No trade executed.")
            return

        bucket = signal["bucket"]
        edge = signal["edge"]
        market_price = market_prices[bucket]

        model_prob = market_price + edge

        stake = self.kelly.calculate_bet_size(
            model_prob=model_prob,
            market_price=market_price,
            bankroll=self.paper.bankroll
        )

        print("Recommended Stake:", stake)

        if stake <= 0:
            print("Stake is zero. No trade.")
            return

        result = self.paper.place_trade(
            side="BUY",
            price=market_price,
            stake=stake
        )

        pnl = result["pnl"]
        new_bankroll = result["new_bankroll"]

        self.performance.record_trade(stake, pnl, new_bankroll)

        print("\nPaper Trade Result:")
        print(result)

        self.performance.summary()


if __name__ == "__main__":

    station = "GHCND:USW00094728"

    market_prices = {
        "≤33": 0.20,
        "34-35": 0.05,
        "36-37": 0.10,
        "38-39": 0.08,
        "40-41": 0.04,
        "42-43": 0.06,
        "44-45": 0.25,
        "46-47": 0.05,
        "≥48": 0.22,
    }

    system = TradingSystem(station, bankroll=1000)

    # Run multiple times to simulate multiple trades
    for _ in range(5):
        system.run(market_prices)
