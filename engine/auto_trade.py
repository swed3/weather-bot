from engine.market_edge import MarketEdgeEngine


class AutoTradeDecision:

    def __init__(self, station_id, edge_threshold=0.05):
        self.station_id = station_id
        self.edge_threshold = edge_threshold

    def generate_signal(self, market_prices):

        engine = MarketEdgeEngine(self.station_id)
        result = engine.find_best_trade(market_prices)

        best_bucket = result["best_bucket"]
        best_edge = result["best_edge"]

        if best_bucket is None:
            return {"trade": False, "reason": "No positive edge"}

        if best_edge >= self.edge_threshold:
            return {
                "trade": True,
                "side": "BUY",
                "bucket": best_bucket,
                "edge": best_edge
            }
        else:
            return {
                "trade": False,
                "reason": f"Edge {best_edge} below threshold {self.edge_threshold}"
            }


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

    trader = AutoTradeDecision(station, edge_threshold=0.05)
    signal = trader.generate_signal(market_prices)

    print("\nAuto Trade Signal:")
    print(signal)
