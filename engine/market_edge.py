from engine.range_model import RangeProbabilityModel


class MarketEdgeEngine:

    def __init__(self, station_id):
        self.station_id = station_id

    def find_best_trade(self, market_prices):
        """
        market_prices = {
            "≤33": 0.18,
            "34-35": 0.05,
            ...
        }
        """

        model = RangeProbabilityModel(self.station_id)
        model_probs = model.calculate_probabilities()

        best_bucket = None
        best_edge = 0

        results = {}

        for bucket, market_price in market_prices.items():

            model_prob = model_probs.get(bucket, 0)

            edge = round(model_prob - market_price, 4)

            results[bucket] = {
                "model_prob": model_prob,
                "market_price": market_price,
                "edge": edge
            }

            if edge > best_edge:
                best_edge = edge
                best_bucket = bucket

        return {
            "all_edges": results,
            "best_bucket": best_bucket,
            "best_edge": best_edge
        }


if __name__ == "__main__":

    station = "GHCND:USW00094728"

    # 🔴 Example fake market prices (replace later with real Polymarket data)
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

    engine = MarketEdgeEngine(station)
    result = engine.find_best_trade(market_prices)

    print("\nAll Bucket Edges:")
    for k, v in result["all_edges"].items():
        print(f"{k}: Model={v['model_prob']} | Market={v['market_price']} | Edge={v['edge']}")

    print("\nBest Trade:")
    print("Bucket:", result["best_bucket"])
    print("Edge:", result["best_edge"])
