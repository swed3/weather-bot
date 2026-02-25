from engine.auto_trade import AutoTradeDecision
from engine.kelly_engine import KellyEngine
from execution.paper_trader import PaperTrader
from engine.settlement_engine import SettlementEngine
from performance.metrics import PerformanceTracker


class TradingSystem:

    def __init__(self):

        self.auto = AutoTradeDecision(station_id="NYC")
        self.kelly = KellyEngine()
        self.paper = PaperTrader()
        self.settlement = SettlementEngine()
        self.performance = PerformanceTracker()

    def run(self, market_prices, actual_temp):

        print("=== Running Trading System ===")

        signal = self.auto.generate_signal(market_prices)
        print("Signal:", signal)

        if not signal.get("trade"):
            print("No trade.")
            return

        price = market_prices[signal["bucket"]]

        stake = self.kelly.calculate_stake(
            edge=signal["edge"],
            bankroll=self.paper.bankroll,
            price=price
        )

        print("Recommended Stake:", round(stake, 2))

        trade_result = self.paper.execute_trade(
            side=signal["side"],
            price=price,
            stake=stake
        )

        print("\nPaper Trade Result:")
        print(trade_result)

        settlement_result = self.settlement.settle_trade(
            trade={
                "side": signal["side"],
                "bucket": signal["bucket"],
                "price": price,
                "stake": stake
            },
            actual_temp=actual_temp
        )

        print("\nSettlement Result:")
        print(settlement_result)

        self.paper.bankroll += settlement_result["profit"]

        self.performance.record_trade(settlement_result["profit"])

        print("\nUpdated Bankroll:", round(self.paper.bankroll, 2))

        print("\n===== PERFORMANCE SUMMARY =====")
        print(self.performance.summary())


if __name__ == "__main__":

    market_prices = {
        "≥48": 0.22
    }

    system = TradingSystem()

    system.run(market_prices, actual_temp=52)
