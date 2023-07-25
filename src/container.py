from config import settings
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Singleton
from boto3 import client
from data_access.data_stores.sql.connection_manager import ConnectionManager
from data_access.data_stores.sql.repositories.read import ReadRepository
from data_access.data_stores.sql.repositories.write import WriteRepository
from data_access.data_stores.sql.query_handlers.ml_model_data import MLModelQueryHandler
from data_access.data_stores.sql.query_handlers.logging import LoggingQueryHandler
from data_access.data_stores.blob.s3 import S3Client
from logging_management.logger import Logger
from application.ml_model_operations.model_writer import ModelWriter
from application.column_transformation_operations.column_transformer_writer import ColumnTransformerWriter
from application.ml_model_trainers.saint.martyred import MartyredModelTrainer

class Container(DeclarativeContainer):

    def __init__(self) -> None:
        pass

    __config = Configuration()

    __config.from_dict(settings)
    
    environment = __config.environment()

    # data access
    __logging_connection_manager = Singleton(ConnectionManager, 
    host = __config.sql.logging_db.host(),
    port = __config.sql.logging_db.port(),
    database = __config.sql.logging_db.database(),
    username = __config.sql.logging_db.username(),
    password = __config.sql.logging_db.password())

    __data_warehouse_connection_manager = Singleton(ConnectionManager, 
    host =  __config.sql.data_warehouse.host(),
    port = __config.sql.data_warehouse.port(),
    database = __config.sql.data_warehouse.database(),
    username = __config.sql.data_warehouse.username(),
    password = __config.sql.data_warehouse.password())

    __data_warehouse_read_repository = Singleton(ReadRepository, connection_manager = __data_warehouse_connection_manager)

    __logging_write_repository = Singleton(WriteRepository, connection_manager = __logging_connection_manager)

    __ml_model_data_query_handler = Singleton(MLModelQueryHandler, read_repository = __data_warehouse_read_repository)

    __logging_query_handler = Singleton(LoggingQueryHandler, write_repository = __logging_write_repository)
    # data access

    #blob
    __blob_client = Singleton(S3Client,
    s3_client = client('s3',
    region_name = __config.aws.region(),
    aws_access_key_id = __config.aws.access_key_id(),
    aws_secret_access_key = __config.aws.access_key_secret(),
    endpoint_url = __config.blob.s3.endpoint()))
    #blob

    # logging
    __logger = Singleton(Logger, query_handler = __logging_query_handler)
    # logging

    # application

    # ml model ops
    __model_writer = Singleton(ModelWriter, blob_client = __blob_client)
    # ml model ops

    # column transformer ops
    __column_transformer_writer = Singleton(ColumnTransformerWriter, blob_client = __blob_client)
    # column transformer ops

    # model trainers
    __martyred_model_trainer = Singleton(MartyredModelTrainer,
    logger = __logger,
    query_handler = __ml_model_data_query_handler,
    model_writer = __model_writer,
    column_transformer_writer = __column_transformer_writer)
    # model trainers

    # initialization
    train_models([
        __martyred_model_trainer()
    ])
    # initialization
    