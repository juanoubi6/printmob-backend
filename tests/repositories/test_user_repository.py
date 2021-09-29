import copy
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch, Mock

from my_app.api.domain import Printer, Buyer, User, PrinterPrototype, UserPrototype, BankInformationPrototype, UserType, \
    AddressPrototype, BuyerPrototype, Designer, DesignerPrototype, PrinterDataDashboard, OrderStatus, \
    DesignerDataDashboard, BuyerDataDashboard
from my_app.api.repositories import UserRepository
from tests.test_utils.mock_entities import MOCK_BUYER_PROTOTYPE, MOCK_PRINTER_PROTOTYPE, MOCK_DESIGNER_PROTOTYPE, MOCK_BALANCE
from tests.test_utils.mock_models import MOCK_USER_PRINTER_MODEL, MOCK_PRINTER_MODEL, \
    MOCK_USER_BUYER_MODEL, MOCK_BUYER_MODEL, MOCK_USER_DESIGNER_MODEL, MOCK_DESIGNER_MODEL, MOCK_CAMPAIGN_MODEL, \
    MOCK_CONFIRMED_CAMPAIGN_MODEL, \
    MOCK_COMPLETED_CAMPAIGN_MODEL, MOCK_ORDER_MODEL, MOCK_MODEL_MODEL, MOCK_DISPATCHED_ORDER_MODEL


class TestUserRepository(unittest.TestCase):

    def setUp(self):
        self.test_db = MagicMock()
        self.mock_transaction_repository = Mock()
        self.user_repository = UserRepository(self.test_db, self.mock_transaction_repository)

    def test_get_printer_by_email_returns_printer(self):
        user_printer_model = copy.deepcopy(MOCK_USER_PRINTER_MODEL)
        user_printer_model.printer = MOCK_PRINTER_MODEL
        self.test_db.session.query.return_value.filter_by.return_value.first.return_value = user_printer_model

        response = self.user_repository.get_printer_by_email("email")

        assert isinstance(response, Printer)

    def test_get_designer_by_email_returns_designer(self):
        user_designer_model = copy.deepcopy(MOCK_USER_DESIGNER_MODEL)
        user_designer_model.designer = MOCK_DESIGNER_MODEL
        self.test_db.session.query.return_value.filter_by.return_value.first.return_value = user_designer_model

        response = self.user_repository.get_designer_by_email("email")

        assert isinstance(response, Designer)

    def test_get_buyer_by_email_returns_buyer(self):
        user_buyer_model = copy.deepcopy(MOCK_USER_BUYER_MODEL)
        user_buyer_model.buyer = MOCK_BUYER_MODEL
        self.test_db.session.query.return_value.filter_by.return_value.first.return_value = user_buyer_model

        response = self.user_repository.get_buyer_by_email("email")

        assert isinstance(response, Buyer)

    def test_get_user_by_email_returns_user(self):
        self.test_db.session.query.return_value.filter_by.return_value.first.return_value = MOCK_USER_BUYER_MODEL

        response = self.user_repository.get_user_by_email("email")

        assert isinstance(response, User)

    def test_is_user_name_in_use_returns_true_if_user_name_is_being_used(self):
        self.test_db.session.query.return_value.filter_by.return_value.first.return_value = MOCK_USER_BUYER_MODEL

        response = self.user_repository.is_user_name_in_use("username")

        assert response is True

    def test_is_email_in_use_returns_true_if_email_is_being_used(self):
        self.test_db.session.query.return_value.filter_by.return_value.first.return_value = MOCK_USER_BUYER_MODEL

        response = self.user_repository.is_email_in_use("email")

        assert response is True

    @patch('my_app.api.repositories.user_repository.BuyerModel')
    def test_create_buyer_creates_buyer(self, mock_buyer_model_instance):
        mock_buyer_model_instance.return_value = MOCK_BUYER_MODEL

        response = self.user_repository.create_buyer(MOCK_BUYER_PROTOTYPE)

        assert isinstance(response, Buyer)
        assert self.test_db.session.add.call_count == 3
        self.test_db.session.flush.assert_called_once()
        self.test_db.session.commit.assert_called_once()

    @patch('my_app.api.repositories.user_repository.PrinterModel')
    def test_create_printer_creates_printer(self, mock_printer_model_instance):
        mock_printer_model_instance.return_value = MOCK_PRINTER_MODEL

        response = self.user_repository.create_printer(MOCK_PRINTER_PROTOTYPE)

        assert isinstance(response, Printer)
        assert self.test_db.session.add.call_count == 3
        self.test_db.session.flush.assert_called_once()
        self.test_db.session.commit.assert_called_once()

    @patch('my_app.api.repositories.user_repository.DesignerModel')
    def test_create_designer_creates_designer(self, mock_designer_model_instance):
        mock_designer_model_instance.return_value = MOCK_DESIGNER_MODEL

        response = self.user_repository.create_designer(MOCK_DESIGNER_PROTOTYPE)

        assert isinstance(response, Designer)
        assert self.test_db.session.add.call_count == 3
        self.test_db.session.flush.assert_called_once()
        self.test_db.session.commit.assert_called_once()

    def test_update_printer_only_updates_certain_fields_and_returns_printer(self):
        self.test_db.session.query.return_value.filter_by.return_value.first.return_value = copy.deepcopy(MOCK_PRINTER_MODEL)

        proto = PrinterPrototype(
            user_prototype=UserPrototype(
                first_name="upd first name",
                last_name="upd last name",
                user_name="upd user name",
                date_of_birth=datetime.strptime("20-07-1995", '%d-%m-%Y'),
                email="upd email",
                user_type=UserType.PRINTER,
                profile_picture_url="url",
            ),
            bank_information_prototype=BankInformationPrototype(
                cbu="upd cbu",
                bank="upd bank",
                account_number="upd acc number",
                alias="upd alias"
            )
        )

        response = self.user_repository.update_printer(1, proto)

        assert isinstance(response, Printer)
        assert response.first_name != MOCK_PRINTER_MODEL.user.first_name
        assert response.last_name != MOCK_PRINTER_MODEL.user.last_name
        assert response.user_name == MOCK_PRINTER_MODEL.user.user_name
        assert response.date_of_birth != MOCK_PRINTER_MODEL.user.date_of_birth
        assert response.email == MOCK_PRINTER_MODEL.user.email
        assert response.user_type.value == MOCK_PRINTER_MODEL.user.user_type

        assert response.bank_information.cbu != MOCK_PRINTER_MODEL.bank_information.cbu
        assert response.bank_information.alias != MOCK_PRINTER_MODEL.bank_information.alias
        assert response.bank_information.bank != MOCK_PRINTER_MODEL.bank_information.bank
        assert response.bank_information.account_number != MOCK_PRINTER_MODEL.bank_information.account_number

    def test_update_designer_only_updates_certain_fields_and_returns_designer(self):
        self.test_db.session.query.return_value.filter_by.return_value.first.return_value = copy.deepcopy(MOCK_DESIGNER_MODEL)

        proto = DesignerPrototype(
            user_prototype=UserPrototype(
                first_name="upd first name",
                last_name="upd last name",
                user_name="upd user name",
                date_of_birth=datetime.strptime("20-07-1995", '%d-%m-%Y'),
                email="upd email",
                user_type=UserType.DESIGNER,
                profile_picture_url="url",
            ),
            bank_information_prototype=BankInformationPrototype(
                cbu="upd cbu",
                bank="upd bank",
                account_number="upd acc number",
                alias="upd alias"
            )
        )

        response = self.user_repository.update_designer(1, proto)

        assert isinstance(response, Designer)
        assert response.first_name != MOCK_DESIGNER_MODEL.user.first_name
        assert response.last_name != MOCK_DESIGNER_MODEL.user.last_name
        assert response.user_name == MOCK_DESIGNER_MODEL.user.user_name
        assert response.date_of_birth != MOCK_DESIGNER_MODEL.user.date_of_birth
        assert response.email == MOCK_DESIGNER_MODEL.user.email
        assert response.user_type.value == MOCK_DESIGNER_MODEL.user.user_type

        assert response.bank_information.cbu != MOCK_DESIGNER_MODEL.bank_information.cbu
        assert response.bank_information.alias != MOCK_DESIGNER_MODEL.bank_information.alias
        assert response.bank_information.bank != MOCK_DESIGNER_MODEL.bank_information.bank
        assert response.bank_information.account_number != MOCK_DESIGNER_MODEL.bank_information.account_number

    def test_update_buyer_only_updates_certain_fields_and_returns_buyer(self):
        self.test_db.session.query.return_value.filter_by.return_value.first.return_value = copy.deepcopy(MOCK_BUYER_MODEL)

        proto = BuyerPrototype(
            user_prototype=UserPrototype(
                first_name="upd first name",
                last_name="upd last name",
                user_name="upd user name",
                date_of_birth=datetime.strptime("20-07-1995", '%d-%m-%Y'),
                email="upd email",
                user_type=UserType.PRINTER,
                profile_picture_url="url",
            ),
            address_prototype=AddressPrototype(
                address="upd address",
                zip_code="updz",
                province="upd province",
                city="upd city",
                floor="updf",
                apartment="upda",
            )
        )

        response = self.user_repository.update_buyer(1, proto)

        assert isinstance(response, Buyer)
        assert response.first_name != MOCK_BUYER_MODEL.user.first_name
        assert response.last_name != MOCK_BUYER_MODEL.user.last_name
        assert response.user_name == MOCK_BUYER_MODEL.user.user_name
        assert response.date_of_birth != MOCK_BUYER_MODEL.user.date_of_birth
        assert response.email == MOCK_BUYER_MODEL.user.email
        assert response.user_type.value == MOCK_BUYER_MODEL.user.user_type

        assert response.address.address != MOCK_BUYER_MODEL.address.address
        assert response.address.zip_code != MOCK_BUYER_MODEL.address.zip_code
        assert response.address.province != MOCK_BUYER_MODEL.address.province
        assert response.address.city != MOCK_BUYER_MODEL.address.city
        assert response.address.floor != MOCK_BUYER_MODEL.address.floor
        assert response.address.apartment != MOCK_BUYER_MODEL.address.apartment

    def test_get_user_by_id_returns_user(self):
        self.test_db.session.query.return_value.filter_by.return_value.first.return_value = MOCK_USER_BUYER_MODEL

        response = self.user_repository.get_user_by_id(MOCK_USER_BUYER_MODEL.id)

        assert isinstance(response, User)

    def test_get_printer_data_dashboard_returns_printer_data_dashboard(self):
        # Mock campaigns query
        self.test_db.session.query.return_value.\
            filter.return_value. \
            filter.return_value. \
            filter.return_value. \
            options.return_value. \
            options.return_value. \
            options.return_value. \
            options.return_value. \
            all.return_value = [MOCK_CAMPAIGN_MODEL, MOCK_CONFIRMED_CAMPAIGN_MODEL, MOCK_COMPLETED_CAMPAIGN_MODEL]

        # Mock balance
        self.mock_transaction_repository.get_user_balance.return_value = MOCK_BALANCE

        # Mock orders query
        pending_order = copy.deepcopy(MOCK_ORDER_MODEL)
        pending_order.status = OrderStatus.IN_PROGRESS.value
        self.test_db.session.query.return_value.\
            filter.return_value. \
            filter.return_value. \
            options.return_value. \
            options.return_value. \
            all.return_value = [pending_order]

        response = self.user_repository.get_printer_data_dashboard(MOCK_USER_BUYER_MODEL.id)

        assert isinstance(response, PrinterDataDashboard)
        assert response.completed_campaigns == 1
        assert response.campaigns_in_progress == 2
        assert response.pending_orders == 1
        assert response.pledges_in_progress == len(MOCK_CAMPAIGN_MODEL.pledges) + len(MOCK_CONFIRMED_CAMPAIGN_MODEL.pledges)
        assert response.balance == MOCK_BALANCE
        assert len(response.ending_campaigns) == 2

    def test_get_designer_data_dashboard_returns_designer_data_dashboard(self):
        mock_model_1 = copy.deepcopy(MOCK_MODEL_MODEL)
        mock_model_2 = copy.deepcopy(MOCK_MODEL_MODEL)

        mock_model_1.likes = 2
        mock_model_2.likes = 3

        # Mock models query
        self.test_db.session.query.return_value.\
            filter.return_value. \
            filter.return_value. \
            options.return_value. \
            options.return_value. \
            options.return_value. \
            options.return_value. \
            all.return_value = [mock_model_1, mock_model_2]

        # Mock balance
        self.mock_transaction_repository.get_user_balance.return_value = MOCK_BALANCE

        # Mock alliances income
        self.test_db.session.query.return_value.\
            filter.return_value. \
            filter.return_value. \
            filter.return_value. \
            first.return_value = [50.0]

        # Mock model purchase income
        self.test_db.session.query.return_value.\
            filter.return_value. \
            first.return_value = [100.0]

        response = self.user_repository.get_designer_data_dashboard(MOCK_USER_DESIGNER_MODEL.id)

        assert isinstance(response, DesignerDataDashboard)
        assert response.uploaded_models == 2
        assert response.total_likes == 5
        assert response.alliances_income == 50.0
        assert response.model_purchase_income == 100.0
        assert response.balance == MOCK_BALANCE

    def test_get_buyer_data_dashboard_returns_buyer_data_dashboard(self):
        # Mock campaigns query
        self.test_db.session.query.return_value.\
            join.return_value. \
            filter.return_value. \
            filter.return_value. \
            filter.return_value. \
            filter.return_value. \
            filter.return_value. \
            options.return_value. \
            options.return_value. \
            options.return_value. \
            all.return_value = [MOCK_CAMPAIGN_MODEL, MOCK_CONFIRMED_CAMPAIGN_MODEL]

        # Mock orders query
        self.test_db.session.query.return_value.\
            filter.return_value. \
            options.return_value. \
            options.return_value. \
            all.return_value = [MOCK_ORDER_MODEL, MOCK_DISPATCHED_ORDER_MODEL]

        response = self.user_repository.get_buyer_data_dashboard(MOCK_USER_BUYER_MODEL.id)

        assert isinstance(response, BuyerDataDashboard)
        assert response.take_part_campaigns == 2
        assert response.completed_orders == 1
        assert response.in_progress_orders == 1
        assert len(response.ending_campaigns) == 2
