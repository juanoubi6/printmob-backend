import json
from unittest.mock import patch

from my_app.api import create_app
from tests.utils.mock_data import MOCK_PLEDGE

from tests.utils.test_json import PLEDGE_POST_REQUEST_JSON

app = create_app()
app.config['TESTING'] = True
app.testing = True
client = app.test_client()


@patch.object(app.pledge_controller, "pledge_service")
def test_create_pledge_returns_created_pledge(mock_pledge_service):
    mock_pledge_service.create_pledge.return_value = MOCK_PLEDGE

    res = client.post("/pledges", data=json.dumps(PLEDGE_POST_REQUEST_JSON))
    assert res.status_code == 201
    assert res.json["id"] == MOCK_PLEDGE.id
