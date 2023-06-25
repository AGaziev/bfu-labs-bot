from .database_connector import DatabaseConnector
from loguru import logger


class Filler(DatabaseConnector):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Inserter for database object was initialized")

    async def fill_table_lab_status_type(self) -> None:
        statuses = ('Сдано', 'Отклонено',
                    'Не проверено')
        query = """--sql
        INSERT INTO lab_status_type (status_name)
        VALUES ($1)
        """
        for status in statuses:
            if await self._execute_query(query, status) is False:
                logger.error("Error while filling lab_status_type table")
            else:
                logger.success("Table lab_status_type was filled successfully")

    async def fill_necessarily_tables(self) -> None:
        logger.warning("Start filling neccecery tables")
        await self.fill_table_lab_status_type()
        logger.warning("Filling neccecery tables was finished successfully")
