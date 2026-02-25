from weather.fetch_noaa import NOAAHistoricalFetcher


class RangeProbabilityModel:

    def __init__(self, station_id):
        self.station_id = station_id

        self.buckets = [
            ("≤33", lambda x: x <= 33),
            ("34-35", lambda x: 34 <= x <= 35),
            ("36-37", lambda x: 36 <= x <= 37),
            ("38-39", lambda x: 38 <= x <= 39),
            ("40-41", lambda x: 40 <= x <= 41),
            ("42-43", lambda x: 42 <= x <= 43),
            ("44-45", lambda x: 44 <= x <= 45),
            ("46-47", lambda x: 46 <= x <= 47),
            ("≥48", lambda x: x >= 48),
        ]

    def calculate_probabilities(self):

        fetcher = NOAAHistoricalFetcher(self.station_id)
        data = fetcher.fetch_feb26_history()

        total = len(data)
        results = {}

        for label, condition in self.buckets:
            count = sum(1 for temp in data if condition(temp))
            prob = count / total
            results[label] = round(prob, 3)

        return results


if __name__ == "__main__":

    station = "GHCND:USW00094728"  # NYC Central Park

    model = RangeProbabilityModel(station)
    probs = model.calculate_probabilities()

    print("Range Probabilities:")
    for k, v in probs.items():
        print(f"{k}: {v}")
