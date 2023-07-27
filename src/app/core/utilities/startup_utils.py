from typing import List
from app.api.consumers.kafka.base import BaseConsumer


def initiate_consumers(consumers: List[BaseConsumer]) -> None:
    for consumer in consumers:
        consumer.consume()
