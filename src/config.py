from os import getenv

settings = {
    'environment': getenv('ENVIRONMENT', 'development'),
    'kafka': {
        'broker': {
            'server_url': getenv('KAFKA_BROKER_SERVER_URL'),
            'port': getenv('KAFKA_BROKER_PORT'),
            'group_id': getenv('KAFKA_BROKER_GROUP_ID')
        },
        'topics': {
            'saint_creation_topic': getenv('SAINT_CREATION_KAFKA_TOPIC'),
            'saint_update_topic': getenv('SAINT_UPDATE_KAFKA_TOPIC'),
            'saint_deletion_topic': getenv('SAINT_DELETION_KAFKA_TOPIC')
        }
    },
    'sql': {
        'data_warehouse': {
            'connection_string': getenv('SAINT_ANALYTICS_DB_CONNECTION_STRING'),
            'saint_lake_table_name': getenv('SAINT_ANALYTICS_DB_SAINT_LAKE_TABLE_NAME')
        }
    },
}
