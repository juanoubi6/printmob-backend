from my_app.api.domain.balance import Balance


class PrinterDataDashboard:
    def __init__(
            self,
            campaigns_in_progress: int,
            completed_campaigns: int,
            pledges_in_progress: int,
            balance: Balance,
            pending_orders: int
    ):
        self.campaigns_in_progress = campaigns_in_progress
        self.completed_campaigns = completed_campaigns
        self.pledges_in_progress = pledges_in_progress
        self.balance = balance
        self.pending_orders = pending_orders

    def to_json(self):
        return {
            "campaigns_in_progress": self.campaigns_in_progress,
            "completed_campaigns": self.completed_campaigns,
            "pledges_in_progress": self.pledges_in_progress,
            "balance": self.balance.to_json(),
            "pending_orders": self.pending_orders
        }
