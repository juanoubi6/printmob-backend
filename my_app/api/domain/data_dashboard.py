import datetime
from typing import List

from my_app.api.domain.balance import Balance


class EndingCampaignResume:
    def __init__(
            self,
            id: int,
            name: str,
            percentage: int,
            end_date: datetime.datetime,
    ):
        self.id = id
        self.name = name
        self.percentage = percentage
        self.end_date = end_date

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "percentage": self.percentage,
            "end_date": self.end_date
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


class DesignerDataDashboard:
    def __init__(
            self,
            uploaded_models: int,
            total_likes: int,
            balance: Balance,
            alliances_income: float,
            model_purchase_income: float,
    ):
        self.uploaded_models = uploaded_models
        self.total_likes = total_likes
        self.balance = balance
        self.alliances_income = alliances_income
        self.model_purchase_income = model_purchase_income

    def to_json(self):
        return {
            "uploaded_models": self.uploaded_models,
            "total_likes": self.total_likes,
            "balance": self.balance.to_json(),
            "alliances_income": self.alliances_income,
            "model_purchase_income": self.model_purchase_income,
        }


class BuyerDataDashboard:
    def __init__(
            self,
            take_part_campaigns: int,
            completed_orders: int,
            in_progress_orders: int,
            ending_campaigns: List[EndingCampaignResume]
    ):
        self.take_part_campaigns = take_part_campaigns
        self.completed_orders = completed_orders
        self.in_progress_orders = in_progress_orders
        self.ending_campaigns = ending_campaigns

    def to_json(self):
        return {
            "take_part_campaigns": self.take_part_campaigns,
            "completed_orders": self.completed_orders,
            "in_progress_orders": self.in_progress_orders,
            "ending_campaigns": [ec.to_json() for ec in self.ending_campaigns]
        }
