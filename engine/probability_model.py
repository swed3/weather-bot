class TemperatureProbabilityModel:

    def probability_above_threshold(self, temperature: float, threshold: float):
        """
        Simple deterministic probability model.
        Later we replace with statistical distribution.
        """

        diff = temperature - threshold

        # basic sigmoid-like scaling
        probability = 1 / (1 + pow(2.71828, -diff))

        return round(probability, 4)

    def probability_below_threshold(self, temperature: float, threshold: float):
        return round(1 - self.probability_above_threshold(temperature, threshold), 4)


if __name__ == "__main__":
    model = TemperatureProbabilityModel()

    temp = 10
    threshold = 8

    print("Above:", model.probability_above_threshold(temp, threshold))
    print("Below:", model.probability_below_threshold(temp, threshold))
