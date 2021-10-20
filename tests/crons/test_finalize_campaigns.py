import datetime
import unittest
from unittest.mock import Mock, MagicMock

from my_app.api.domain import CampaignStatus, TransactionType
from my_app.api.repositories.models import CampaignModel, UserModel, PledgeModel, BuyerModel, PrinterModel, \
    TransactionModel, DesignerModel
from my_app.crons import finalize_campaign

session_factory_mock = MagicMock()
email_repository_mock = Mock()
executor_mock = Mock()
mercadopago_repository_mock = Mock()


class TestFinalizeCampaignsCron(unittest.TestCase):

    def setUp(self):
        session_factory_mock.reset_mock()
        email_repository_mock.reset_mock()
        executor_mock.reset_mock()
        mercadopago_repository_mock.reset_mock()

    def test_finalize_campaign_executes_successfully(self):
        # Mock context manager
        session_mock = Mock()
        session_factory_mock.return_value.__enter__.return_value = session_mock

        successful_campaign, unsuccessful_campaign = self._prepare_test_campaigns()

        session_mock. \
            query.return_value. \
            filter.return_value. \
            filter.return_value. \
            filter.return_value. \
            options.return_value. \
            options.return_value. \
            all.return_value = [successful_campaign, unsuccessful_campaign]

        finalize_campaign(session_factory_mock, email_repository_mock, executor_mock, mercadopago_repository_mock)

        # Assert calls to repositories
        assert session_mock.add.call_count == 6
        assert session_mock.commit.call_count == 4
        assert session_mock.rollback.call_count == 0
        assert executor_mock.submit.call_count == 4

        # Assert campaign final statuses
        assert successful_campaign.status == CampaignStatus.COMPLETED.value
        assert successful_campaign.end_date.day == datetime.datetime.now().day
        assert successful_campaign.end_date.month == datetime.datetime.now().month
        assert successful_campaign.end_date.year == datetime.datetime.now().year
        assert unsuccessful_campaign.status == CampaignStatus.UNSATISFIED.value

        # Assert orders were created
        assert session_mock.add.mock_calls[0][1][0].campaign_id == successful_campaign.id
        assert session_mock.add.mock_calls[0][1][0].buyer_id == successful_campaign.pledges[0].buyer_id
        assert session_mock.add.mock_calls[1][1][0].campaign_id == successful_campaign.id
        assert session_mock.add.mock_calls[1][1][0].buyer_id == successful_campaign.pledges[1].buyer_id

        # Assert unsuccessful campaign pledges were deleted
        assert unsuccessful_campaign.pledges[0].deleted_at is not None
        assert unsuccessful_campaign.pledges[1].deleted_at is not None

        # Assert refund transactions were created
        assert session_mock.add.mock_calls[2][1][0].type == TransactionType.REFUND.value
        assert session_mock.add.mock_calls[2][1][0].amount == unsuccessful_campaign.pledges[0].printer_transaction.amount * -1
        assert session_mock.add.mock_calls[3][1][0].type == TransactionType.REFUND.value
        assert session_mock.add.mock_calls[3][1][0].amount == unsuccessful_campaign.pledges[0].designer_transaction.amount * -1
        assert session_mock.add.mock_calls[4][1][0].type == TransactionType.REFUND.value
        assert session_mock.add.mock_calls[4][1][0].amount == unsuccessful_campaign.pledges[1].printer_transaction.amount * -1
        assert session_mock.add.mock_calls[5][1][0].type == TransactionType.REFUND.value
        assert session_mock.add.mock_calls[5][1][0].amount == unsuccessful_campaign.pledges[1].designer_transaction.amount * -1

    def test_finalize_campaign_rollbacks_pledge_on_exception(self):
        # Mock context manager
        session_mock = Mock()
        session_factory_mock.return_value.__enter__.return_value = session_mock

        _, unsuccessful_campaign = self._prepare_test_campaigns()

        session_mock. \
            query.return_value. \
            filter.return_value. \
            filter.return_value. \
            filter.return_value. \
            options.return_value. \
            options.return_value. \
            all.return_value = [unsuccessful_campaign]

        session_mock.commit.side_effect = [None, None, Exception("Unexpected commit error"), None]

        finalize_campaign(session_factory_mock, email_repository_mock, executor_mock, mercadopago_repository_mock)

        # Assert calls to repositories
        assert session_mock.rollback.call_count == 1  # Rollback the 2nd pledge
        assert session_mock.add_all.call_count == 1  # Add 2nd pledge failure to DB
        assert executor_mock.submit.call_count == 2  # Emails of unsatisfied campaign (for printer and the pledger whose transaction could be refunded)

    def test_finalize_campaign_rollbacks_when_updating_campaign_status_fails(self):
        # Mock context manager
        session_mock = Mock()
        session_factory_mock.return_value.__enter__.return_value = session_mock

        successful_campaign, unsuccessful_campaign = self._prepare_test_campaigns()

        session_mock. \
            query.return_value. \
            filter.return_value. \
            filter.return_value. \
            filter.return_value. \
            options.return_value. \
            options.return_value. \
            all.return_value = [successful_campaign, unsuccessful_campaign]

        # Just fail on the successful campaign update
        session_mock.commit.side_effect = [Exception("Unexpected commit error"), None, None, None]

        finalize_campaign(session_factory_mock, email_repository_mock, executor_mock, mercadopago_repository_mock)

        # Assert calls to repositories
        assert session_mock.rollback.call_count == 1  # Rollback the update of the first campaign
        assert session_mock.add_all.call_count == 0  # There are no pledge refund fails
        assert executor_mock.submit.call_count == 2  # Emails of unsatisfied campaign (for printer and pledgers)

    def _prepare_test_campaigns(self) -> (CampaignModel, CampaignModel):
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

        successful_campaign_model = CampaignModel(
            id=1,
            name="Successful campaign",
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
                        mp_payment_id=11111,
                        user_id=mock_printer.id,
                        amount=10,
                        type=TransactionType.PLEDGE.value,
                        is_future=True,
                    ),
                    designer_transaction=TransactionModel(
                        id=2,
                        mp_payment_id=22222,
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
                        mp_payment_id=22222,
                        user_id=mock_printer.id,
                        amount=10,
                        type=TransactionType.PLEDGE.value,
                        is_future=True,
                    ),
                    designer_transaction=TransactionModel(
                        id=4,
                        mp_payment_id=22222,
                        user_id=mock_designer.id,
                        amount=5,
                        type=TransactionType.PLEDGE.value,
                        is_future=True,
                    )
                )
            ],
            created_at=datetime.datetime(2020, 5, 17),
            updated_at=datetime.datetime(2020, 5, 17),
            status="In progress"
        )

        unsuccessful_campaign_model = CampaignModel(
            id=2,
            name="Unsuccessful campaign",
            description="Description",
            campaign_picture_url="campaign picture url",
            pledge_price=20,
            end_date=datetime.datetime(2020, 5, 17),
            min_pledgers=5,
            max_pledgers=10,
            tech_detail=None,
            images=[],
            printer=mock_printer,
            pledges=[
                PledgeModel(
                    id=3,
                    campaign_id=2,
                    pledge_price=20,
                    buyer_id=4,
                    buyer=BuyerModel(
                        id=4,
                        user=UserModel(
                            id=4,
                            first_name="User 4",
                            last_name="Doe",
                            user_name="johnDoe5",
                            date_of_birth=datetime.datetime(2020, 5, 17),
                            email="user4@email.com",
                            created_at=datetime.datetime(2020, 5, 17),
                            updated_at=datetime.datetime(2020, 5, 17)
                        )
                    ),
                    created_at=datetime.datetime(2020, 5, 17),
                    updated_at=datetime.datetime(2020, 5, 17),
                    printer_transaction=TransactionModel(
                        id=5,
                        mp_payment_id=33333,
                        user_id=mock_printer.id,
                        amount=10,
                        type=TransactionType.PLEDGE.value,
                        is_future=True,
                    ),
                    designer_transaction=TransactionModel(
                        id=6,
                        mp_payment_id=33333,
                        user_id=mock_designer.id,
                        amount=5,
                        type=TransactionType.PLEDGE.value,
                        is_future=True,
                    )
                ),
                PledgeModel(
                    id=4,
                    campaign_id=2,
                    pledge_price=20,
                    buyer_id=5,
                    buyer=BuyerModel(
                        id=5,
                        user=UserModel(
                            id=5,
                            first_name="User 5",
                            last_name="Doe",
                            user_name="johnDoe5",
                            date_of_birth=datetime.datetime(2020, 5, 17),
                            email="user5@email.com",
                            created_at=datetime.datetime(2020, 5, 17),
                            updated_at=datetime.datetime(2020, 5, 17)
                        )
                    ),
                    created_at=datetime.datetime(2020, 5, 17),
                    updated_at=datetime.datetime(2020, 5, 17),
                    printer_transaction=TransactionModel(
                        id=7,
                        mp_payment_id=44444,
                        user_id=mock_printer.id,
                        amount=10,
                        type=TransactionType.PLEDGE.value,
                        is_future=True,
                    ),
                    designer_transaction=TransactionModel(
                        id=6,
                        mp_payment_id=44444,
                        user_id=mock_designer.id,
                        amount=5,
                        type=TransactionType.PLEDGE.value,
                        is_future=True,
                    )
                )
            ],
            created_at=datetime.datetime(2020, 5, 17),
            updated_at=datetime.datetime(2020, 5, 17),
            status="In progress"
        )

        return successful_campaign_model, unsuccessful_campaign_model
