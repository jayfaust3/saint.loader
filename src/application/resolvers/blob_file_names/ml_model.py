from core.enums.prediction_type import PredictionType
from core.constants.blob_file_names.ml_model import *

class MLModelFileNameResolver(object):
    
    def __init__(self) -> None:
        pass

    @staticmethod
    def resolve_file_name(prediction_type: PredictionType) -> str:
        match prediction_type:
            case PredictionType.MARTYRED:
                return MARTYRED_MODEL_FILE_NAME
            case _:
                return None