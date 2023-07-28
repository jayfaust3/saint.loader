from abc import ABC, abstractmethod
from typing import List
from confluent_kafka import Consumer


class BaseConsumer(ABC):

    def __init__(self,
                 broker_host: str,
                 broker_group_id: str,
                 topics: List[str]) -> None:
        conf = {
            'bootstrap.servers': broker_host,
            'group.id': broker_group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': True,
            'heartbeat.interval.ms': 25000,
            'max.poll.interval.ms': 180000,
            'session.timeout.ms': 180000,
        }
        self._consumer: Consumer = Consumer(conf)
        self._consumer.subscribe(topics)

    @abstractmethod
    def consume(self) -> None:
        pass
