class RiskEngine:
    """
    Professional capital protection system
    """

    def __init__(
        self,
        balance=1000,
        max_risk_per_trade=0.02,
        max_daily_loss=0.05
    ):
        self.balance = balance
        self.start_balance = balance

        self.max_risk_per_trade = max_risk_per_trade
        self.max_daily_loss = max_daily_loss

        self.daily_loss = 0

    def allowed_trade_size(self, price):
        """
        Kelly-lite sizing
        """
        risk_amount = self.balance * self.max_risk_per_trade

        if price <= 0:
            return 0

        size = risk_amount / price
        return round(size, 2)

    def update_pnl(self, pnl):
        self.balance += pnl

        if pnl < 0:
            self.daily_loss += abs(pnl)

    def trading_allowed(self):
        loss_limit = self.start_balance * self.max_daily_loss

        if self.daily_loss >= loss_limit:
            print("⚠ Daily loss limit reached.")
            return False

        return True
