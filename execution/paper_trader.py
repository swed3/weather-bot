from engine.trade_decision import TradeDecision


class PaperTrader:

    def __init__(self, bankroll=1000):
        self.bankroll = bankroll
        self.position = 0
        self.entry_price = None

    def execute(self, blended_prob, market_price):

        decision = TradeDecision.evaluate(
            blended_prob,
            market_price
        )

        if decision["trade"]:

            if decision["side"] == "BUY":

                stake = self.bankroll * 0.1  # 10% position sizing
                self.position += stake
                self.entry_price = market_price
                self.bankroll -= stake

                print(f"BUY executed at {market_price}")
                print(f"Stake: {stake}")
                print(f"Remaining bankroll: {self.bankroll}")

            elif decision["side"] == "SELL":

                print("SELL signal detected (short simulation not enabled)")

        else:
            print("No trade")

    def settle(self, outcome_yes):

        if self.position == 0:
            print("No open position")
            return

        if outcome_yes:
            payout = self.position * 1
        else:
            payout = 0

        pnl = payout - self.position
        self.bankroll += payout
        self.position = 0

        print(f"Trade settled. PnL: {pnl}")
        print(f"New bankroll: {self.bankroll}")


if __name__ == "__main__":

    blended_probability = 0.8847
    market_price = 0.82

    trader = PaperTrader()

    trader.execute(blended_probability, market_price)

    # simulate YES outcome
    trader.settle(outcome_yes=True)
