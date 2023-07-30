from app.data_access.data_stores.sql.repositories.write import WriteRepository
from app.data_access.data_stores.sql.queries.saint_transaction import *
from app.core.data_models.saint import Saint


class SaintTransactionQueryHandler(object):

    def __init__(self,
                 saint_lake_table_name: str,
                 write_repository: WriteRepository) -> None:
        self.__saint_lake_table_name: str = saint_lake_table_name
        self.__write_repository: WriteRepository = write_repository

    def handle_create_and_update(self, saint: Saint) -> None:
        self.__write_repository.write(SAINT_CREATE_AND_UPDATE_QUERY.format(saint_lake=self.__saint_lake_table_name,
                                                                           id=saint.id,
                                                                           created_date=saint.created_date,
                                                                           modified_date=saint.modified_date,
                                                                           name=saint.name,
                                                                           year_of_birth=saint.year_of_birth,
                                                                           year_of_death=saint.year_of_death,
                                                                           region=saint.region,
                                                                           martyred=saint.martyred,
                                                                           notes=saint.notes,
                                                                           has_avatar=saint.has_avatar))

    def handle_delete(self, saint_id: str) -> None:
        self.__write_repository.write(SAINT_DELETE_QUERY.format(saint_lake=self.__saint_lake_table_name,
                                                                saint_id=saint_id))
