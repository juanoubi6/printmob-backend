import unittest
from unittest.mock import MagicMock, patch

import pytest

from my_app.api.exceptions import ServerException
from my_app.api.repositories import S3Repository
from tests.utils.mock_data import MOCK_FILE

test_s3_client = MagicMock()
bucket_name = "bucketName"
s3_repository = S3Repository(test_s3_client, bucket_name)


class TestS3Repository(unittest.TestCase):

    def setUp(self):
        test_s3_client.reset_mock()

    @patch.object(test_s3_client, 'put_object')
    def test_create_image_returns_generated_image_url_on_success(self, put_object_mock):
        put_object_mock.return_value = "mocked result"
        test_s3_client.meta.endpoint_url = "https://s3.us-east-2.amazonaws.com"

        response = s3_repository.upload_file(MOCK_FILE, "keyOfThe/image")

        assert response == "https://s3.us-east-2.amazonaws.com/{bucket}/keyOfThe/image".format(bucket=bucket_name)

    @patch.object(test_s3_client, 'put_object')
    def test_create_image_raises_server_exception_on_s3_failure(self, put_object_mock):
        put_object_mock.side_effect = Exception("Some S3 error")

        with pytest.raises(ServerException):
            s3_repository.upload_file(MOCK_FILE, "keyOfThe/image")
