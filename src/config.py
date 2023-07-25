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
    'sql': {
        'logging_db': {
            'host': getenv('LOGGING_DB_HOST'),
            'port': getenv('LOGGING_DB_PORT'),
            'database': getenv('LOGGING_DB_DATABASE'),
            'username': getenv('LOGGING_DB_USERNAME'),
            'password': getenv('LOGGING_DB_PASSWORD')
        },
        'data_warehouse': {
            'host': getenv('DATA_WAREHOUSE_HOST'),
            'port': getenv('DATA_WAREHOUSE_PORT'),
            'database': getenv('DATA_WAREHOUSE_DATABASE'),
            'username': getenv('DATA_WAREHOUSE_USERNAME'),
            'password': getenv('DATA_WAREHOUSE_PASSWORD')
        }
    },
}