class EdgeDetector:

    def __init__(self, min_edge=0.05):
        """
        min_edge = minimum difference required to trigger trade
        default 5%
        """
        self.min_edge = min_edge

    def detect_edge(self, model_probability: float, market_probability: float):

        edge = model_probability - market_probability

        if abs(edge) >= self.min_edge:
            return {
                "trade": True,
                "edge": round(edge, 4),
                "side": "BUY" if edge > 0 else "SELL"
            }

        return {
            "trade": False,
            "edge": round(edge, 4),
            "side": None
        }


if __name__ == "__main__":
    detector = EdgeDetector(min_edge=0.05)

    model_prob = 0.72
    market_prob = 0.60

    print(detector.detect_edge(model_prob, market_prob))
