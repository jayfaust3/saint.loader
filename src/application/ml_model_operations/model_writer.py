from core.constants.blob_directory_names import MODELS_DIRECTORY_NAME as directory
from core.enums.prediction_type import PredictionType
from application.resolvers.blob_file_names.ml_model import MLModelFileNameResolver
from data_access.data_stores.blob.base import BaseBlobClient
from tensorflow.keras import Model

class ModelWriter(object):

    def __init__(self, 
    blob_client: BaseBlobClient) -> None:
        self.__blob_client: BaseBlobClient = blob_client
        self.__directory: str = directory

    def save_model(self, prediction_type: PredictionType, model: Model) -> None:
        blob_name: str = MLModelFileNameResolver.resolve_file_name(prediction_type)

        self.__blob_client.post_blob(self.__directory, blob_name, model.to_json())

        return