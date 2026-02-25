class RangeProbabilityModel:

    def __init__(self, historical_temps):
        """
        historical_temps: list of temperature values (can be str or float)
        Example:
        ["43.0", "52.0", 48.0, "37.0"]
        """
        self.historical_temps = historical_temps or []

    def calculate_probabilities(self):

        if not self.historical_temps:
            print("WARNING: No historical data available.")
            return {}

        cleaned_temps = []

        # --- SAFE CLEANING ---
        for temp in self.historical_temps:
            try:
                value = float(temp)
                cleaned_temps.append(value)
            except:
                # Skip bad NOAA values like None, "", etc.
                continue

        if not cleaned_temps:
            print("WARNING: All historical values invalid.")
            return {}

        total = len(cleaned_temps)

        # --- Polymarket Style Buckets ---
        buckets = {
            "≤33": 0,
            "34-35": 0,
            "36-37": 0,
            "38-39": 0,
            "40-41": 0,
            "42-43": 0,
            "44-45": 0,
            "46-47": 0,
            "≥48": 0
        }

        for temp in cleaned_temps:

            if temp <= 33:
                buckets["≤33"] += 1
            elif 34 <= temp <= 35:
                buckets["34-35"] += 1
            elif 36 <= temp <= 37:
                buckets["36-37"] += 1
            elif 38 <= temp <= 39:
                buckets["38-39"] += 1
            elif 40 <= temp <= 41:
                buckets["40-41"] += 1
            elif 42 <= temp <= 43:
                buckets["42-43"] += 1
            elif 44 <= temp <= 45:
                buckets["44-45"] += 1
            elif 46 <= temp <= 47:
                buckets["46-47"] += 1
            elif temp >= 48:
                buckets["≥48"] += 1

        probabilities = {}

        for bucket, count in buckets.items():
            probabilities[bucket] = round(count / total, 4)

        return probabilities


# --- Test Block ---
if __name__ == "__main__":

    sample_data = ["43.0", "45.0", 44.0, "31.0", "52.0", "48.0", "37.0"]

    model = RangeProbabilityModel(sample_data)

    probs = model.calculate_probabilities()

    print("Range Probabilities:")
    print(probs)
