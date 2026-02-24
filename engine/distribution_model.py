import statistics
import math


class DistributionModel:

    @staticmethod
    def calculate_stats(values):
        mean = statistics.mean(values)
        std_dev = statistics.stdev(values)
        return mean, std_dev

    @staticmethod
    def probability_above(threshold, mean, std_dev):
        z = (threshold - mean) / std_dev
        cdf = 0.5 * (1 + math.erf(z / math.sqrt(2)))
        return round(1 - cdf, 4)


if __name__ == "__main__":

    data = [43.0, 45.0, 44.0, 31.0, 32.0, 39.0, 44.0,
            52.0, 36.0, 48.0, 45.0, 37.0, 50.0, 55.0, 56.0]

    model = DistributionModel()
    mean, std = model.calculate_stats(data)

    prob = model.probability_above(33, mean, std)

    print("Mean:", round(mean, 2))
    print("Std Dev:", round(std, 2))
    print("Probability ≥ 33°F:", prob)
