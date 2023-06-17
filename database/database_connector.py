from loguru import logger
from data import Config
import asyncpg


class DatabaseConnector(Config):
    def __init__(self) -> None:
        super().__init__()
        logger.info("Database connector object was created")

    async def _create_connection(self) -> asyncpg.connection.Connection:
        conn = await asyncpg.connect(**self.database_connection_parameters)
        logger.debug(
            f"Connection to {self.database_connection_parameters.get('database')} database established")
        return conn

    async def _execute_query(self, query: str, *args) -> list[asyncpg.Record] | bool:
        """Executes query and returns result or None if error occurred

        Args:
            query (str): SQL query to execute
            *args (tuple): arguments for query

        Returns:
            list[asyncpg.Record] | None: result of query execution
        """
        conn = await self._create_connection()

        try:
            result = await conn.fetch(query, *args)
        except asyncpg.exceptions.PostgresError as e:
            logger.error(
                f"Error while executing query: {e.__class__.__name__} {e}")
            logger.error(f"Query: {query}")
            return False
        finally:
            await conn.close()

        return result

    async def _execute_query_with_returning_one_row(self, query: str, *args) -> asyncpg.Record | bool:
        """Executes query and returns first row of result or None if error occurred

        Args:
            query (str): SQL query to execute
            *args (tuple): arguments for query

        Returns:
            list[asyncpg.Record] | None: result of query execution
        """
        conn = await self._create_connection()

        try:
            result = await conn.fetchrow(query, *args)
        except asyncpg.exceptions.PostgresError as e:
            logger.error(
                f"Error while executing query: {e.__class__.__name__} {e}")
            logger.error(f"Query: {query}")
            return False
        finally:
            await conn.close()

        return result
