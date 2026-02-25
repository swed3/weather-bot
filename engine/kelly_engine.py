class KellyEngine:

    def __init__(self, kelly_fraction=0.5):
        self.kelly_fraction = kelly_fraction  # 0.5 = half Kelly

    def calculate_bet_size(self, model_prob, market_price, bankroll):

        if market_price <= 0 or market_price >= 1:
            return 0

        p = model_prob
        q = 1 - p

        # payout multiple for prediction market
        b = (1 - market_price) / market_price

        full_kelly = (b * p - q) / b

        if full_kelly <= 0:
            return 0

        adjusted_kelly = full_kelly * self.kelly_fraction

        stake = bankroll * adjusted_kelly

        return round(stake, 2)


if __name__ == "__main__":

    bankroll = 1000
    model_prob = 0.333
    market_price = 0.22

    engine = KellyEngine(kelly_fraction=0.5)
    stake = engine.calculate_bet_size(model_prob, market_price, bankroll)

    print("\nHalf Kelly Recommended Stake:")
    print("Stake:", stake)
