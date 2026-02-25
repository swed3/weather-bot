class SettlementEngine:

    def __init__(self):
        pass

    def settle_trade(self, trade, actual_temp):
        """
        trade = {
            'side': 'BUY',
            'bucket': '≥48',
            'price': 0.22,
            'stake': 72.44
        }
        """

        bucket = trade['bucket']
        stake = trade['stake']
        price = trade['price']

        win = False

        if bucket == "≥48":
            if actual_temp >= 48:
                win = True

        # Add other bucket rules later

        if win:
            profit = stake * (1 - price)
        else:
            profit = -stake

        return {
            "win": win,
            "profit": profit
        }
