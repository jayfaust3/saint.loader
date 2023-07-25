from typing import Any
from data_access.data_stores.sql.connection_manager import ConnectionManager
from pandas import DataFrame, read_sql

class ReadRepository(object):

    def __init__(self, connection_manager: ConnectionManager) -> None:
        self.__connection_manager: ConnectionManager = connection_manager

    def read(self, sql: str) -> DataFrame:
        connection: Any = self.__connection_manager.get_connection()

        results: DataFrame = read_sql(sql, connection)

        connection.close()

        return results