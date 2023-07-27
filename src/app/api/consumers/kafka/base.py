from abc import ABC, abstractmethod
from typing import List
from kafka import KafkaConsumer


class BaseConsumer(ABC):

    def __init__(self,
                 broker_host: str,
                 broker_group_id: str,
                 topics: List[str]) -> None:
        self._consumer: KafkaConsumer = KafkaConsumer(
            *topics,
            bootstrap_servers=broker_host,
            group_id=broker_group_id
        )

    @abstractmethod
    def consume(self) -> None:
        pass
