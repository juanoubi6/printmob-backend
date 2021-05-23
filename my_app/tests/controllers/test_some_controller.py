import unittest
from unittest.mock import Mock

from my_app.api import create_app
from my_app.api.domain import User

app = create_app("test")
app.config['TESTING'] = True
app.config['FLASK_ENV'] = 'TESTING'
app.testing = True
client = app.test_client()


class TestSomeController(unittest.TestCase):

    def test_some_controller_works(self):
        mock_test_service = Mock()
        mock_test_service.get_test_data_from_service.return_value = User("5555", "fullname", "nickname")
        app.test_controller.test_service = mock_test_service

        res = client.get("/test-controller/testUrl")
        self.assertEqual(res.json["name"], "5555")
