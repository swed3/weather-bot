class TradeDecision:

    @staticmethod
    def evaluate(blended_prob, market_price, min_edge=0.03):

        edge = blended_prob - market_price

        if edge > min_edge:
            return {
                "trade": True,
                "side": "BUY",
                "edge": round(edge, 4)
            }

        if edge < -min_edge:
            return {
                "trade": True,
                "side": "SELL",
                "edge": round(edge, 4)
            }

        return {
            "trade": False,
            "side": "NONE",
            "edge": round(edge, 4)
        }


if __name__ == "__main__":

    blended = 0.8847

    # Example market price
    market_price = 0.82

    result = TradeDecision.evaluate(blended, market_price)

    print(result)
