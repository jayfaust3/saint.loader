from kafka import KafkaConsumer


class SaintTransactionConsumer(object):

    def __init__(self,
                 broker_host: str,
                 broker_port: str,
                 broker_group_id: str,
                 saint_creation_topic: str,
                 saint_update_topic: str,
                 saint_deletion_topic: str) -> None:
        self.__saint_creation_topic = saint_creation_topic,
        self.__saint_update_topic = saint_update_topic,
        self.__saint_deletion_topic = saint_deletion_topic,
        self.__consumer: KafkaConsumer = KafkaConsumer(
            self.__saint_creation_topic,
            self.__saint_update_topic,
            self.__saint_deletion_topic,
            bootstrap_servers=f'{broker_host}:{broker_port}',
            group_id=broker_group_id
        )
