from typing import Any
from botocore.client import BaseClient
from botocore.response import StreamingBody
from data_access.data_stores.blob.base import BaseBlobClient

class S3Client(BaseBlobClient):

    def __init__(self,
    s3_client: BaseClient) -> None:
        self.__s3_client: BaseClient = s3_client

    def get_blob(self, blob_directory: str, blob_name: str) -> bytes:
        response: Any = self.__s3_client.get_object(Bucket = blob_directory, Key = blob_name)

        stream: StreamingBody = response['Body']

        return stream.read()

    def post_blob(self, blob_directory: str, blob_name: str, data: Any) -> None:        
        self.__s3_client.put_object(Bucket = blob_directory, Key = blob_name, Body = data)

        return

