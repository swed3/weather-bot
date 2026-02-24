from engine.distribution_model import DistributionModel


class BlendModel:

    @staticmethod
    def blended_probability(
        threshold,
        historical_values,
        forecast_temp,
        weight_forecast=0.6
    ):

        model = DistributionModel()
        mean, std = model.calculate_stats(historical_values)

        # Historical probability
        hist_prob = model.probability_above(threshold, mean, std)

        # Adjust mean toward forecast
        adjusted_mean = (mean + forecast_temp) / 2

        forecast_prob = model.probability_above(
            threshold,
            adjusted_mean,
            std
        )

        final_prob = (
            weight_forecast * forecast_prob
            + (1 - weight_forecast) * hist_prob
        )

        return {
            "historical_prob": hist_prob,
            "forecast_prob": forecast_prob,
            "blended_prob": round(final_prob, 4)
        }


if __name__ == "__main__":

    historical = [
        43.0, 45.0, 44.0, 31.0, 32.0, 39.0, 44.0,
        52.0, 36.0, 48.0, 45.0, 37.0, 50.0, 55.0, 56.0
    ]

    forecast_temp = 39  # example

    result = BlendModel.blended_probability(
        threshold=33,
        historical_values=historical,
        forecast_temp=forecast_temp
    )

    print(result)
