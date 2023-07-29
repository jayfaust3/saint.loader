from app.data_access.data_stores.sql.repositories.write import WriteRepository
from app.data_access.data_stores.sql.queries.saint_transaction import *


class SaintTransactionQueryHandler(object):

    def __init__(self,
                 saint_lake_table_name: str,
                 write_repository: WriteRepository) -> None:
        self.__saint_lake_table_name: str = saint_lake_table_name
        self.__write_repository: WriteRepository = write_repository

    def handle_create_and_update(self) -> None:
        self.__write_repository.write(SAINT_CREATE_AND_UPDATE_QUERY)

    def handle_delete(self) -> None:
        self.__write_repository.write(SAINT_DELETE_QUERY)
