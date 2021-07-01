import json
import unittest
from unittest.mock import patch

from my_app.api import create_app
from tests.utils.mock_entities import MOCK_PLEDGE
from tests.utils.test_json import PLEDGE_POST_REQUEST_JSON

from my_app.api.exceptions import NotFoundException
from my_app.api.exceptions.pledge_creation_exception import PledgeCreationException

app = create_app()
app.config['TESTING'] = True
app.testing = True
client = app.test_client()


class TestPledgeController(unittest.TestCase):

    @patch.object(app.pledge_controller, "pledge_service")
    def test_create_pledge_returns_created_pledge(self, mock_pledge_service):
        mock_pledge_service.create_pledge.return_value = MOCK_PLEDGE

        res = client.post("/pledges", data=json.dumps(PLEDGE_POST_REQUEST_JSON))
        assert res.status_code == 201
        assert res.json["id"] == MOCK_PLEDGE.id

    @patch.object(app.pledge_controller, "pledge_service")
    def test_create_pledge_fails_if_campaign_does_not_exist(self, mock_pledge_service):
        mock_pledge_service.create_pledge.side_effect = NotFoundException("some error")

        res = client.post("/pledges", data=json.dumps(PLEDGE_POST_REQUEST_JSON))
        assert res.status_code == 404
        assert res.json['error:'] == "An element was not found"
        assert res.json['message'] == "some error"

    @patch.object(app.pledge_controller, "pledge_service")
    def test_create_pledge_fails_if_campaign_has_reached_maximum_pledgers(self, mock_pledge_service):
        mock_pledge_service.create_pledge.side_effect = PledgeCreationException("some error")

        res = client.post("/pledges", data=json.dumps(PLEDGE_POST_REQUEST_JSON))
        assert res.status_code == 400
        assert res.json['error:'] == "Business error"
        assert res.json['message'] == "some error"

    @patch.object(app.pledge_controller, "pledge_service")
    def test_cancel_pledge_returns_200_on_success(self, mock_pledge_service):
        res = client.delete("/pledges/1")

        assert res.status_code == 200
        mock_pledge_service.cancel_pledge.assert_called_once_with(1)
