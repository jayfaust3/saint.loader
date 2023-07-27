from config import settings
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Singleton
# from boto3 import client
from app.data_access.data_stores.sql.connection_manager import ConnectionManager
from app.data_access.data_stores.sql.repositories.write import WriteRepository
# from app.data_access.data_stores.blob.s3 import S3Client
from app.api.consumers.kafka.saint_transaction import SaintTransactionConsumer
from app.core.utilities.startup_utils import initiate_consumers


class Container(DeclarativeContainer):

    def __init__(self) -> None:
        pass

    __config = Configuration()

    __config.from_dict(settings)

    environment = __config.environment()

    # data access
    __data_warehouse_connection_manager = Singleton(ConnectionManager,
                                                    host=__config.sql.data_warehouse.host(),
                                                    port=__config.sql.data_warehouse.port(),
                                                    database=__config.sql.data_warehouse.database(),
                                                    username=__config.sql.data_warehouse.username(),
                                                    password=__config.sql.data_warehouse.password())

    __data_warehouse_write_repository = Singleton(WriteRepository, connection_manager=__data_warehouse_connection_manager)
    # data access

    # blob
    # __blob_client = Singleton(S3Client,
    #                           s3_client=client('s3',
    #                                            region_name=__config.aws.region(),
    #                                            aws_access_key_id=__config.aws.access_key_id(),
    #                                            aws_secret_access_key=__config.aws.access_key_secret(),
    #                                            endpoint_url=__config.blob.s3.endpoint()))
    # blob

    # api
    __saint_transaction_consumer = Singleton(SaintTransactionConsumer,
                                             broker_host=f'{__config.kafka.broker.server_url()}:{__config.kafka.broker.port()}',
                                             broker_group_id=__config.kafka.broker.group_id(),
                                             topics=[
                                                 __config.kafka.topics.saint_creation_topic(),
                                                 __config.kafka.topics.saint_update_topic(),
                                                 __config.kafka.topics.saint_deletion_topic()
                                             ])
    # api

    # initialization
    initiate_consumers([
        __saint_transaction_consumer()
    ])
    # initialization
