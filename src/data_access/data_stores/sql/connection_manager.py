from typing import Any
# from pyodbc import connect
from psycopg2 import connect
# from core.constants.sql_drivers import POSTGRESQL as driver

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

    def get_connection(self) -> Any:
        # connection_string: str = 'DRIVER={' + f'{driver}' + '}' + f';SERVER={self.__host};DATABASE={self.__database};UID={self.__username};PWD={self.__password}'
        
        # return connect(connection_string)

        return connect(host = self.__host,
        # port = self.__port,
        dbname = self.__database,
        user = self.__username,
        password = self.__password)
