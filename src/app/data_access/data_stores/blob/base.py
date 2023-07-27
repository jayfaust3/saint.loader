from typing import Any
from abc import ABC, abstractmethod


class BaseBlobClient(ABC):

    @abstractmethod
    def get_blob(self, blob_directory: str, blob_name: str) -> Any:
        pass

    @abstractmethod
    def post_blob(self, blob_directory: str, blob_name: str, data: Any) -> None:
        pass
