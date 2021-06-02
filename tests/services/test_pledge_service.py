from unittest.mock import Mock

from my_app.api.domain import PledgePrototype
from my_app.api.services import PledgeService
from tests.mock_data import MOCK_PLEDGE

mock_pledge_repository = Mock()
pledge_service = PledgeService(mock_pledge_repository)


def test_create_pledge_returns_created_pledge():
    mock_pledge_repository.create_pledge.return_value = MOCK_PLEDGE

    created_pledge = pledge_service.create_pledge(
        PledgePrototype(
            buyer_id=1,
            pledge_price=34,
            campaign_id=1
        )
    )

    assert created_pledge.id == MOCK_PLEDGE.id
    mock_pledge_repository.create_pledge.assert_called_once()
