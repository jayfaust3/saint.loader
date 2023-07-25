from typing import List
from core.enums.prediction_type import PredictionType
from core.data_models.data_column import DataColumnModel
from core.constants.ml_model_data_transformable_columns import *

class MLModelDataTransformableColumnsResolver(object):

    def __init__(self) -> None:
        pass
    
    @staticmethod
    def resolve_transformable_columns(prediction_type: PredictionType) -> List[DataColumnModel]:
        match prediction_type:
            case PredictionType.MARTYRED:
                return MARTYRED_TRANSFORMABLE_COLUMNS
            case _:
                return None