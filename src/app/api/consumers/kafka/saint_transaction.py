from typing import List
from os import getenv
from app.api.consumers.kafka.base import BaseConsumer
from app.data_access.data_stores.sql.query_handlers.saint_transaction import SaintTransactionQueryHandler
from app.core.data_models.saint import Saint


class SaintTransactionConsumer(BaseConsumer):

    def __init__(self,
                 broker_host: str,
                 broker_group_id: str,
                 topics: List[str],
                 saint_transaction_query_handler: SaintTransactionQueryHandler) -> None:
        super().__init__(
            broker_host,
            broker_group_id,
            topics
        )
        self.__saint_creation_topic: str = getenv('SAINT_CREATION_KAFKA_TOPIC')
        self.__saint_update_topic: str = getenv('SAINT_UPDATE_KAFKA_TOPIC')
        self.__saint_deletion_topic: str = getenv('SAINT_DELETION_KAFKA_TOPIC')
        self.__saint_transaction_query_handler: SaintTransactionQueryHandler = saint_transaction_query_handler

    def consume(self) -> None:
        while True:
            msg: dict = self._consumer.poll(1.0)

            if msg is None or not msg:
                continue

            if msg.error():
                print("Consumer error happened: {}".format(msg.error()))
                continue

            topic = msg.topic()
            message_data = msg.value().decode('utf-8')
            print('Connected to Topic: {} and Partition : {}'.format(topic, msg.partition()))
            print('Received Message : {} with Offset : {}'.format(message_data, msg.offset()))

            match topic:
                case self.__saint_creation_topic:
                     saint = Saint(message_data._id(),
                                   message_data.createdDate(),
                                   message_data.modifiedDate(),
                                   message_data.name(),
                                   message_data.yearOfBirth(),
                                   message_data.yearOfDeath(),
                                   message_data.region(),
                                   message_data.martyred(),
                                   message_data.notes(),
                                   message_data.hasAvatar())

                     self.__saint_transaction_query_handler.handle_create_and_update(saint)

                case self.__saint_update_topic:
                     saint = Saint(message_data._id(),
                                   message_data.createdDate(),
                                   message_data.modifiedDate(),
                                   message_data.name(),
                                   message_data.yearOfBirth(),
                                   message_data.yearOfDeath(),
                                   message_data.region(),
                                   message_data.martyred(),
                                   message_data.notes(),
                                   message_data.hasAvatar())

                     self.__saint_transaction_query_handler.handle_create_and_update(saint)

                case self.__saint_transaction_query_handler:
                     saint_id: str = message_data.id()

                     self.__saint_transaction_query_handler.handle_delete(saint_id)

                case _:
                    raise Exception('{} is not a supported topic'.format())
