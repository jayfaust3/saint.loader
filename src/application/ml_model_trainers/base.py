from abc import ABC, abstractmethod
from typing import List
from traceback import format_exception
from pandas.core.frame import DataFrame
from application.column_transformation_operations.column_transformer_writer import ColumnTransformerWriter
from application.ml_model_operations.model_writer import ModelWriter
from core.data_models.error import ErrorModel
from core.enums.prediction_type import PredictionType
from core.enums.column_data_type import ColumnDataType
from core.data_models.data_column import DataColumnModel
from data_access.data_stores.sql.query_handlers.ml_model_data import MLModelQueryHandler
from application.transformer_builders.transformer_builder import TransformerBuilder
from application.resolvers.ml_model_data_transformable_columns import MLModelDataTransformableColumnsResolver
from logging_management.logger import Logger
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from tensorflow.keras import Model

class BaseModelTrainer(ABC):

    def __init__(self, 
    logger: Logger,
    query_handler: MLModelQueryHandler,
    model_writer: ModelWriter,
    column_transformer_writer: ColumnTransformerWriter,
    prediction_type: PredictionType) -> None:
        self.__logger: Logger = logger,
        self.__query_handler: MLModelQueryHandler = query_handler
        self.__model_writer: ModelWriter = model_writer
        self.__column_transformer_writer: ColumnTransformerWriter = column_transformer_writer
        self.__prediction_type: PredictionType = prediction_type

    def train_model(self) -> None:
        try:
            print('Training model: `{0}`'.format(self.__prediction_type.name).replace('`', "'"))

            model: Model = self.__get_trained_model()

            self.__model_writer.save_model(self.__prediction_type, model)

            return
        except Exception as err:
            error_model = ErrorModel(stack_trace = ''.join(format_exception(None, err, err.__traceback__)), 
            error_message = str(err),
            optional_data = 'Unable to train model: `{0}`'.format(self.__prediction_type.name).replace('`', "'"))
            
            self.__logger.log_error(error_model) 

    @abstractmethod
    def _initiate_model(self, training_data: list) -> Model:
        pass

    @abstractmethod
    def _compile_model(self, model: Model) -> None:
        pass

    @abstractmethod
    def _fit_model(self, model: Model, x_train: list, x_test: list, y_train: list, y_test: list) -> None:
        pass

    def __get_trained_model(self) -> Model:
        raw_data: DataFrame = self.__query_handler.query_for_model_data(self.__prediction_type)
        
        transformed_input_data: DataFrame = self.__transform_inputs(raw_data)

        transformed_target_data: DataFrame = self.__transform_targets(raw_data)

        x_train, x_test, y_train, y_test = train_test_split(transformed_input_data, 
        transformed_target_data, 
        test_size = 0.3, 
        random_state = 1)

        model: Model = self._initiate_model(x_train.toarray())

        self._compile_model(model)

        self._fit_model(model, 
        x_train.toarray(), 
        x_test.toarray(), 
        y_train.to_list(), 
        y_test.to_list())

        return model

    def __get_and_save_column_transformer(self, training_data: DataFrame) -> ColumnTransformer:
        column_transformer: ColumnTransformer = TransformerBuilder.get_column_transformer(self.__prediction_type, training_data)

        column_transformer.fit(training_data.drop('target', axis = 1))

        self.__column_transformer_writer.post_column_transformer(self.__prediction_type, column_transformer)

        return column_transformer

    def __transform_inputs(self, training_data: DataFrame) -> DataFrame:
        column_transformer: ColumnTransformer = self.__get_and_save_column_transformer(training_data)

        return column_transformer.transform(training_data.drop('target', axis = 1))

    def __transform_targets(self, training_data: DataFrame) -> DataFrame:
        transformable_columns: List[DataColumnModel] = MLModelDataTransformableColumnsResolver.resolve_transformable_columns(self.__prediction_type)

        for column in transformable_columns:
            if column.column_name == 'target' and column.data_type == ColumnDataType.BOOLEAN:
                training_data['target'] = (training_data['target'] == True).astype(int)
                break

        return training_data['target']