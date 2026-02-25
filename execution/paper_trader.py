class PaperTrader:

    def __init__(self, bankroll=1000):
        self.bankroll = bankroll

    def place_trade(self, side, price, stake):

        if stake > self.bankroll:
            return {
                "status": "REJECTED",
                "reason": "Insufficient bankroll"
            }

        self.bankroll -= stake

        print(f"\n{side} executed at price {price}")
        print(f"Stake: {stake}")
        print(f"Remaining bankroll: {self.bankroll}")

        # For now assume trade settles immediately (demo mode)
        pnl = 0

        self.bankroll += stake + pnl

        return {
            "status": "FILLED",
            "side": side,
            "price": price,
            "stake": stake,
            "pnl": pnl,
            "new_bankroll": self.bankroll
        }
