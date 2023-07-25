from typing import List
from application.resolvers.ml_model_data_transformable_columns import MLModelDataTransformableColumnsResolver
from core.data_models.data_column import DataColumnModel
from core.enums.prediction_type import PredictionType
from core.enums.column_data_type import ColumnDataType
from pandas import DataFrame
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

class TransformerBuilder(object):

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_column_transformer(prediction_type: PredictionType, data: DataFrame) -> ColumnTransformer:
        data = data.drop('target', axis = 1)

        transformable_columns: List[DataColumnModel] = MLModelDataTransformableColumnsResolver.resolve_transformable_columns(prediction_type)

        non_numeric_columns: List[DataColumnModel] = [column for column in transformable_columns 
        if (column.column_name != 'target' and column.data_type != ColumnDataType.BOOLEAN and column.data_type != ColumnDataType.INT)]

        transformer = ColumnTransformer(
        [('one_hot_encoder', OneHotEncoder(categories = 'auto', handle_unknown = 'ignore'), 
        [data.columns.get_loc(column.column_name) for column in non_numeric_columns])],
        remainder = 'passthrough')

        transformer.fit(data)

        return transformer