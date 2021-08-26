from typing import List

from my_app.api.domain.balance import Balance


class EndingCampaignResume:
    def __init__(
            self,
            id: int,
            name: str,
            percentage: int,
            remaining_days: int,
    ):
        self.id = id
        self.name = name
        self.percentage = percentage
        self.remaining_days = remaining_days

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "percentage": self.percentage,
            "remaining_days": self.remaining_days
        }


class PrinterDataDashboard:
    def __init__(
            self,
            campaigns_in_progress: int,
            completed_campaigns: int,
            pledges_in_progress: int,
            balance: Balance,
            pending_orders: int,
            ending_campaigns: List[EndingCampaignResume]
    ):
        self.campaigns_in_progress = campaigns_in_progress
        self.completed_campaigns = completed_campaigns
        self.pledges_in_progress = pledges_in_progress
        self.balance = balance
        self.pending_orders = pending_orders
        self.ending_campaigns = ending_campaigns

    def to_json(self):
        return {
            "campaigns_in_progress": self.campaigns_in_progress,
            "completed_campaigns": self.completed_campaigns,
            "pledges_in_progress": self.pledges_in_progress,
            "balance": self.balance.to_json(),
            "pending_orders": self.pending_orders,
            "ending_campaigns": [ec.to_json() for ec in self.ending_campaigns]
        }
