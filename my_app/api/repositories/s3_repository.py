from my_app.api.domain import File
from my_app.api.exceptions import ServerException


class S3Repository:
    def __init__(self, s3_client, bucket_name: str):
        self.s3_client = s3_client
        self.bucket_name = bucket_name

    def create_image(self, file: File, key: str) -> str:
        try:
            self.s3_client.put_object(
                Body=file.content,
                Bucket=self.bucket_name,
                Key=key,
                ACL='public-read',
                ContentType=file.mimetype
            )

            return self._generate_file_url(key)
        except Exception as exc:
            raise ServerException("Unexpected error when uploading image to S3: {}".format(str(exc)))

    def _generate_file_url(self, key: str) -> str:
        return "{base_url}/{bucket}/{key}".format(
            base_url=self.s3_client.meta.endpoint_url, bucket=self.bucket_name, key=key
        )
