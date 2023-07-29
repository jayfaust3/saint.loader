from typing import List
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
        self.__saint_transaction_query_handler: SaintTransactionQueryHandler = saint_transaction_query_handler

    def consume(self) -> None:
        while True:
            msg: dict = self._consumer.poll(1.0)

            if msg is None or not msg:
                continue

            if msg.error():
                print("Consumer error happened: {}".format(msg.error()))
                continue

            print("Connected to Topic: {} and Partition : {}".format(msg.topic(), msg.partition()))
            print("Received Message : {} with Offset : {}".format(msg.value().decode('utf-8'), msg.offset()))
