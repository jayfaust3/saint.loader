from psycopg import connect
from psycopg.connection import Connection


class ConnectionManager(object):

    def __init__(self,
                 host: str,
                 port: str,
                 database: str,
                 username: str,
                 password: str) -> None:
        self.__host: str = host
        self.__port: str = port,
        self.__database: str = database
        self.__username: str = username
        self.__password: str = password

    def get_connection(self) -> Connection:
        connection_string: str = f'postgresql://{self.__username}:{self.__password}@{self.__host}:{self.__port}/{self.__database}'
        print('Connecting with connection string: {}'.format(connection_string))
        return connect(connection_string)
