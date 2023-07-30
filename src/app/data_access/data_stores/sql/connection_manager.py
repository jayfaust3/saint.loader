from psycopg import connect
from psycopg.connection import Connection


class ConnectionManager(object):

    def __init__(self, connection_string: str) -> None:
        self.__connection_string: str = connection_string

    def get_connection(self) -> Connection:
        return connect(self.__connection_string)
