from typing import Any
from sklearn.compose import ColumnTransformer
from pickle import dumps
from core.constants.blob_directory_names import COLUMN_TRANSFORMERS_DIRECTORY_NAME as directory
from core.enums.prediction_type import PredictionType
from application.resolvers.blob_file_names.column_transformer import ColumnTransformerFileNameResolver
from data_access.data_stores.blob.base import BaseBlobClient

class ColumnTransformerWriter(object):

    def __init__(self, 
    blob_client: BaseBlobClient) -> None:
        self.__blob_client: BaseBlobClient = blob_client
        self.__directory: str = directory

    def post_column_transformer(self, prediction_type: PredictionType, column_transformer: ColumnTransformer) -> None:
        blob_name: str = ColumnTransformerFileNameResolver.resolve_file_name(prediction_type)

        blob: Any = dumps(column_transformer)

        self.__blob_client.post_blob(self.__directory, blob_name, blob)
        
        return