from typing import Any
from application.column_transformation_operations.column_transformer_writer import ColumnTransformerWriter
from application.ml_model_trainers.base import BaseModelTrainer
from application.ml_model_operations.model_writer import ModelWriter
from core.enums.prediction_type import PredictionType
from core.constants.ml_model_metrics import METRICS as metrics
from data_access.data_stores.sql.query_handlers.ml_model_data import MLModelQueryHandler
from logging_management.logger import Logger
from tensorflow.keras import Model, Input
from tensorflow.keras.layers import Layer, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.data import Dataset

class MartyredModelTrainer(BaseModelTrainer):

    def __init__(self,
    logger: Logger,
    query_handler: MLModelQueryHandler,
    model_writer: ModelWriter,
    column_transformer_writer: ColumnTransformerWriter) -> None:
        super().__init__(logger,
        query_handler,
        model_writer,
        column_transformer_writer,
        PredictionType.MARTYRED)

    def _initiate_model(self, training_data: list) -> Model:
        inputs: Any = Input(shape = (training_data.shape[1],))

        dense: Layer = Dense(12, activation = 'relu')

        x = dense(inputs)

        droupout: Layer = Dropout(0.3)

        x = droupout(x)

        dense = Dense(8, activation = 'relu')

        prediction: Layer = Dense(1, activation = 'sigmoid')

        predictions = prediction(x)

        model: Model = Model(inputs = inputs, outputs = predictions)

        return model

    def _compile_model(self, model: Model) -> None:
        optimizer: Adam = Adam(0.001)

        loss: BinaryCrossentropy = BinaryCrossentropy()
        
        model.compile(optimizer = optimizer, 
        loss = loss, 
        metrics = metrics)

    def _fit_model(self, model: Model, x_train: list, x_test: list, y_train: list, y_test: list) -> None:
        dataset_train = Dataset.from_tensor_slices((x_train, y_train))

        dataset_train = dataset_train.batch(16)

        dataset_train.shuffle(128)

        dataset_val = Dataset.from_tensor_slices((x_test, y_test))

        dataset_val = dataset_val.batch(16)

        dataset_val.shuffle(128)

        num_epochs: int = 100

        model.fit(dataset_train, epochs = num_epochs, validation_data = dataset_val)
