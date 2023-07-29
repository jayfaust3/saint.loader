from os import getenv

settings = {
    'aws': {
        'access_key_id': getenv('AWS_ACCESS_KEY_ID'),
        'access_key_secret': getenv('AWS_SECRET_ACCESS_KEY'),
        'region': getenv('AWS_REGION')
    },
    'blob': {
        's3': {
            'endpoint': getenv('AWS_S3_ENDPOINT')
        }
    },
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
            'host': getenv('SAINT_ANALYTICS_DB_HOST'),
            'port': getenv('SAINT_ANALYTICS_DB_PORT'),
            'database': getenv('SAINT_ANALYTICS_DB_DATABASE'),
            'username': getenv('SAINT_ANALYTICS_DB_USER'),
            'password': getenv('SAINT_ANALYTICS_DB_PASSWORD'),
            'saint_lake_table_name': getenv('SAINT_ANALYTICS_DB_SAINT_LAKE_TABLE_NAME')
        }
    },
}
