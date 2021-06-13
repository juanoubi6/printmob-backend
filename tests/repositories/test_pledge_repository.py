import unittest
from unittest.mock import MagicMock

from my_app.api.domain import PledgePrototype, Pledge
from my_app.api.repositories import PledgeRepository

test_db = MagicMock()
pledge_repository = PledgeRepository(test_db)


class TestPledgeRepository(unittest.TestCase):

    def setUp(self):
        test_db.reset_mock()

    def test_create_pledge_returns_created_pledge(self):
        test_proto = PledgePrototype(
            buyer_id=1,
            pledge_price=34,
            campaign_id=1
        )

        response = pledge_repository.create_pledge(test_proto)

        assert isinstance(response, Pledge)
        test_db.session.add.assert_called_once()
        test_db.session.commit.assert_called_once()
