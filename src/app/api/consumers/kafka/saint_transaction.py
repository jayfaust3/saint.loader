from typing import List
from os import getenv
from json import loads
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

            topic: str = msg.topic()
            message_data_json: str = msg.value().decode('utf-8')

            message_data: dict = loads(message_data_json)

            if topic == self.__saint_creation_topic or topic == self.__saint_update_topic:
                saint = Saint(message_data.get('_id'),
                              message_data.get('createdDate'),
                              message_data.get('modifiedDate'),
                              message_data.get('name'),
                              message_data.get('yearOfBirth'),
                              message_data.get('yearOfDeath'),
                              message_data.get('region'),
                              message_data.get('martyred'),
                              message_data.get('notes'),
                              message_data.get('hasAvatar'))

                self.__saint_transaction_query_handler.handle_create_and_update(saint)
            elif topic == self.__saint_deletion_topic:
                saint_id: str = message_data.get('id')

                self.__saint_transaction_query_handler.handle_delete(saint_id)
            else:
                raise Exception(f'{topic} is not a supported topic')
