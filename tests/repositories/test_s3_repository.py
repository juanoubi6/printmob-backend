import unittest
from unittest.mock import MagicMock, patch

import pytest

from my_app.api.exceptions import ServerException
from my_app.api.repositories import S3Repository
from tests.test_utils.mock_entities import MOCK_RAW_IMAGE_FILE

bucket_name = "bucketName"


class TestS3Repository(unittest.TestCase):

    def setUp(self):
        self.test_s3_client = MagicMock()
        self.s3_repository = S3Repository(self.test_s3_client, bucket_name)

    def test_upload_file_returns_generated_image_url_on_success(self):
        self.test_s3_client.put_object.return_value = "mocked result"
        self.test_s3_client.meta.endpoint_url = "https://s3.us-east-2.amazonaws.com"

        response = self.s3_repository.upload_file(MOCK_RAW_IMAGE_FILE, "keyOfThe/image")

        assert response == "https://s3.us-east-2.amazonaws.com/{bucket}/keyOfThe/image".format(bucket=bucket_name)

    def test_upload_file_raises_server_exception_on_s3_failure(self):
        self.test_s3_client.put_object.side_effect = Exception("Some S3 error")

        with pytest.raises(ServerException):
            self.s3_repository.upload_file(MOCK_RAW_IMAGE_FILE, "keyOfThe/image")

    def test_delete_file_does_not_raise_any_exception_even_on_s3_failure(self):
        self.test_s3_client.delete_object.side_effect = Exception("Some S3 error")

        self.s3_repository.delete_file("keyOfThe/image")

        self.test_s3_client.delete_object.assert_called_once()
