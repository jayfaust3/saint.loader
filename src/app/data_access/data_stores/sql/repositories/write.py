from typing import Union
from psycopg.connection import Connection, Cursor, ServerCursor
from app.data_access.data_stores.sql.connection_manager import ConnectionManager


class WriteRepository(object):

    def __init__(self, connection_manager: ConnectionManager) -> None:
        self.__connection_manager: ConnectionManager = connection_manager

    def write(self, sql: str) -> None:
        connection: Connection = self.__connection_manager.get_connection()

        cursor: Union[Cursor, ServerCursor] = connection.cursor()

        cursor.execute(sql)

        connection.commit()

        connection.close()

        return
