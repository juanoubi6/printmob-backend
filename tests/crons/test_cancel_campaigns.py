import datetime
import unittest
from unittest.mock import Mock, MagicMock

from my_app.api.domain import CampaignStatus, TransactionType
from my_app.api.repositories.models import CampaignModel, UserModel, PledgeModel, BuyerModel, PrinterModel, \
    TransactionModel, DesignerModel
from my_app.crons.cancel_campaigns import cancel_campaigns


class TestCancelCampaignsCron(unittest.TestCase):

    def test_cancel_campaign_executes_successfully(self):
        session_factory_mock = MagicMock()
        email_repository_mock = Mock()
        executor_mock = Mock()
        mercadopago_repository_mock = Mock()

        # Mock context manager
        session_mock = Mock()
        session_factory_mock.return_value.__enter__.return_value = session_mock

        campaign_to_cancel = self._prepare_test_campaign()

        session_mock. \
            query.return_value. \
            filter.return_value. \
            filter.return_value. \
            options.return_value. \
            options.return_value. \
            all.return_value = [campaign_to_cancel]

        cancel_campaigns(session_factory_mock, email_repository_mock, executor_mock, mercadopago_repository_mock)

        # Assert calls to repositories
        assert session_mock.add.call_count == 4  # Refunded printer and designer transactions
        assert session_mock.commit.call_count == 3  # 2 for the pledges, 1 for the campaign at the end
        assert session_mock.rollback.call_count == 0  # No errors so no rollbacks
        assert executor_mock.submit.call_count == 1

        # Assert campaign final statuses
        assert campaign_to_cancel.status == CampaignStatus.CANCELLED.value

        # Assert pledges were deleted
        assert campaign_to_cancel.pledges[0].deleted_at is not None
        assert campaign_to_cancel.pledges[1].deleted_at is not None

        # Assert refund transactions were created
        assert session_mock.add.mock_calls[0][1][0].type == TransactionType.REFUND.value
        assert session_mock.add.mock_calls[0][1][0].amount == campaign_to_cancel.pledges[0].printer_transaction.amount * -1
        assert session_mock.add.mock_calls[1][1][0].type == TransactionType.REFUND.value
        assert session_mock.add.mock_calls[1][1][0].amount == campaign_to_cancel.pledges[0].designer_transaction.amount * -1
        assert session_mock.add.mock_calls[2][1][0].type == TransactionType.REFUND.value
        assert session_mock.add.mock_calls[2][1][0].amount == campaign_to_cancel.pledges[1].printer_transaction.amount * -1
        assert session_mock.add.mock_calls[3][1][0].type == TransactionType.REFUND.value
        assert session_mock.add.mock_calls[3][1][0].amount == campaign_to_cancel.pledges[1].designer_transaction.amount * -1

    def test_cancel_campaigns_rollbacks_pledge_on_exception(self):
        session_factory_mock = MagicMock()
        email_repository_mock = Mock()
        executor_mock = Mock()
        mercadopago_repository_mock = Mock()

        # Mock context manager
        session_mock = Mock()
        session_factory_mock.return_value.__enter__.return_value = session_mock

        campaign_to_cancel = self._prepare_test_campaign()

        session_mock. \
            query.return_value. \
            filter.return_value. \
            filter.return_value. \
            options.return_value. \
            options.return_value. \
            all.return_value = [campaign_to_cancel]

        session_mock.commit.side_effect = [None, Exception("Unexpected commit error"), None, None]

        cancel_campaigns(session_factory_mock, email_repository_mock, executor_mock, mercadopago_repository_mock)

        # Assert calls to repositories
        assert session_mock.rollback.call_count == 1  # Rollback the 2nd pledge
        assert session_mock.add_all.call_count == 1  # Add 1st pledge failure to DB
        assert executor_mock.submit.call_count == 1  # Emails for pledgers

    def test_cancel_campaigns_rollbacks_when_updating_campaign_status_fails(self):
        session_factory_mock = MagicMock()
        email_repository_mock = Mock()
        executor_mock = Mock()
        mercadopago_repository_mock = Mock()

        # Mock context manager
        session_mock = Mock()
        session_factory_mock.return_value.__enter__.return_value = session_mock

        campaign_to_cancel = self._prepare_test_campaign()

        session_mock. \
            query.return_value. \
            filter.return_value. \
            filter.return_value. \
            options.return_value. \
            options.return_value. \
            all.return_value = [campaign_to_cancel]

        # Just fail on the successful campaign update
        session_mock.commit.side_effect = [Exception("Unexpected commit error"), None, None]

        cancel_campaigns(session_factory_mock, email_repository_mock, executor_mock, mercadopago_repository_mock)

        # Assert calls to repositories
        assert session_mock.rollback.call_count == 1  # Rollback the update of the first campaign
        assert session_mock.add_all.call_count == 0  # There are no pledge refund fails
        assert executor_mock.submit.call_count == 0  # No emails are sent if campaign change status fails

    def _prepare_test_campaign(self) -> CampaignModel:
        mock_printer = PrinterModel(
            id=1,
            user=UserModel(
                id=1,
                first_name="Printer 1",
                last_name="Printer 1",
                user_name="Printer1",
                date_of_birth=datetime.datetime(2020, 5, 17),
                email="printer1@email.com",
                created_at=datetime.datetime(2020, 5, 17),
                updated_at=datetime.datetime(2020, 5, 17),
                deleted_at=None
            )
        )

        mock_designer = DesignerModel(
            id=2,
            user=UserModel(
                id=2,
                first_name="Designer 1",
                last_name="Designer 1",
                user_name="Designer",
                date_of_birth=datetime.datetime(2020, 5, 17),
                email="Designer@email.com",
                created_at=datetime.datetime(2020, 5, 17),
                updated_at=datetime.datetime(2020, 5, 17),
                deleted_at=None
            )
        )

        campaign_model = CampaignModel(
            id=1,
            name="Campaign to cancel",
            description="Description",
            campaign_picture_url="campaign picture url",
            pledge_price=10,
            end_date=datetime.datetime(2020, 5, 17),
            min_pledgers=2,
            max_pledgers=10,
            tech_detail=None,
            images=[],
            printer=mock_printer,
            pledges=[
                PledgeModel(
                    id=1,
                    campaign_id=1,
                    pledge_price=10,
                    buyer_id=2,
                    buyer=BuyerModel(
                        id=2,
                        user=UserModel(
                            id=2,
                            first_name="User 2",
                            last_name="Doe",
                            user_name="johnDoe5",
                            date_of_birth=datetime.datetime(2020, 5, 17),
                            email="user2@email.com",
                            created_at=datetime.datetime(2020, 5, 17),
                            updated_at=datetime.datetime(2020, 5, 17)
                        )
                    ),
                    created_at=datetime.datetime(2020, 5, 17),
                    updated_at=datetime.datetime(2020, 5, 17),
                    printer_transaction=TransactionModel(
                        id=1,
                        mp_payment_id=12345,
                        user_id=mock_printer.id,
                        amount=10,
                        type=TransactionType.PLEDGE.value,
                        is_future=True,
                    ),
                    designer_transaction=TransactionModel(
                        id=2,
                        mp_payment_id=12345,
                        user_id=mock_designer.id,
                        amount=5,
                        type=TransactionType.PLEDGE.value,
                        is_future=True,
                    )
                ),
                PledgeModel(
                    id=2,
                    campaign_id=1,
                    pledge_price=10,
                    buyer_id=3,
                    buyer=BuyerModel(
                        id=3,
                        user=UserModel(
                            id=3,
                            first_name="User 3",
                            last_name="Doe",
                            user_name="johnDoe5",
                            date_of_birth=datetime.datetime(2020, 5, 17),
                            email="user3@email.com",
                            created_at=datetime.datetime(2020, 5, 17),
                            updated_at=datetime.datetime(2020, 5, 17)
                        )
                    ),
                    created_at=datetime.datetime(2020, 5, 17),
                    updated_at=datetime.datetime(2020, 5, 17),
                    printer_transaction=TransactionModel(
                        id=3,
                        mp_payment_id=12345,
                        user_id=mock_printer.id,
                        amount=10,
                        type=TransactionType.PLEDGE.value,
                        is_future=True,
                    ),
                    designer_transaction=TransactionModel(
                        id=4,
                        mp_payment_id=12345,
                        user_id=mock_designer.id,
                        amount=5,
                        type=TransactionType.PLEDGE.value,
                        is_future=True,
                    )
                )
            ],
            created_at=datetime.datetime(2020, 5, 17),
            updated_at=datetime.datetime(2020, 5, 17),
            status="To be cancelled"
        )

        return campaign_model
