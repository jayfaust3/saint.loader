from typing import Any
from data_access.data_stores.sql.connection_manager import ConnectionManager

class WriteRepository(object):

    def __init__(self, connection_manager: ConnectionManager) -> None:
        self.__connection_manager: ConnectionManager = connection_manager

    def write(self, sql: str) -> None:
        connection: Any = self.__connection_manager.get_connection()

        cursor: Any = connection.cursor()

        cursor.execute(sql)

        connection.commit()

        connection.close()

        return
