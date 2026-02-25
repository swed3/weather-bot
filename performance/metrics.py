class PerformanceTracker:

    def __init__(self, starting_bankroll=1000):
        self.starting_bankroll = starting_bankroll
        self.bankroll_history = [starting_bankroll]
        self.trades = []

    def record_trade(self, stake, pnl, new_bankroll):
        self.trades.append({
            "stake": stake,
            "pnl": pnl,
            "bankroll": new_bankroll
        })
        self.bankroll_history.append(new_bankroll)

    def total_return(self):
        return (self.bankroll_history[-1] - self.starting_bankroll) / self.starting_bankroll

    def win_rate(self):
        if not self.trades:
            return 0
        wins = [t for t in self.trades if t["pnl"] > 0]
        return len(wins) / len(self.trades)

    def expectancy(self):
        if not self.trades:
            return 0
        avg_win = sum(t["pnl"] for t in self.trades if t["pnl"] > 0)
        avg_loss = sum(t["pnl"] for t in self.trades if t["pnl"] <= 0)

        wins = len([t for t in self.trades if t["pnl"] > 0])
        losses = len([t for t in self.trades if t["pnl"] <= 0])

        if wins > 0:
            avg_win /= wins
        if losses > 0:
            avg_loss /= losses

        win_rate = self.win_rate()

        return (win_rate * avg_win) + ((1 - win_rate) * avg_loss)

    def max_drawdown(self):
        peak = self.bankroll_history[0]
        max_dd = 0

        for value in self.bankroll_history:
            if value > peak:
                peak = value
            dd = (peak - value) / peak
            if dd > max_dd:
                max_dd = dd

        return max_dd

    def summary(self):
        print("\n===== PERFORMANCE SUMMARY =====")
        print("Total Trades:", len(self.trades))
        print("Total Return:", round(self.total_return() * 100, 2), "%")
        print("Win Rate:", round(self.win_rate() * 100, 2), "%")
        print("Expectancy per Trade:", round(self.expectancy(), 4))
        print("Max Drawdown:", round(self.max_drawdown() * 100, 2), "%")
        print("================================\n")
