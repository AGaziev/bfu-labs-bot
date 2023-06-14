from .database_connector import DatabaseConnector
from loguru import logger
from typing import Any


class Selector(DatabaseConnector):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Selector for database object was initialized")

    async def select_one_row_from_table(self, table_name: str, column_name: str, value: str) -> Any:
        """
        Selects one row from table by column name and value\n
        USE IT ONLY IF THIS CLASS HAS NO METHOD FOR YOUR QUERY\n

        Args:
            table_name (str): name of table to select from
            column_name (str): name of column to select from
            value (str): value of column to select from

        Returns:
            Any: result of query execution
        """
        query = f"""--sql
        SELECT * FROM {table_name}
        WHERE {column_name} = '{value}';
        """
        result = await self._execute_query_with_returning_one_row(query)
        if result is False:
            logger.error(
                f"Error while selecting from {table_name} with {column_name} = {value}")
            return None
        else:
            logger.success(f"Selected from {table_name} successfully")
            return result[0]

    async def select_all_rows_from_table(self, table_name: str, column_name: str, value: str) -> Any:
        """
        Selects all rows from table by column name and value\n
        USE IT ONLY IF THIS CLASS HAS NO METHOD FOR YOUR QUERY\n

        Args:
            table_name (str): name of table to select from
            column_name (str): name of column to select from
            value (str): value of column to select from

        Returns:
            Any: result of query execution
        """
        query = f"""--sql
        SELECT * FROM {table_name}
        WHERE {column_name} = '{value}';
        """
        result = await self._execute_query(query)
        if result is False:
            logger.error(
                f"Error while selecting from {table_name} with {column_name} = {value}")
            return None
        else:
            logger.success(f"Selected from {table_name} successfully")
            return result

    async def check_is_user_exist(self, user_id: int) -> bool:
        """
        Check if user exists in database in table users\n
        """
        query = f"""--sql
        SELECT EXISTS(SELECT 1 FROM users WHERE telegram_id = {user_id});
        """
        result = await self._execute_query_with_returning_one_row(query)
        if result is False:
            logger.error(
                f"Error while checking if user exists; user_id = {user_id}")
            return False
        else:
            logger.success(
                f"Checked if user exists successfully; user_id = {user_id}")
            return result[0]

    async def select_group_id_by_group_name(self, group_name: str) -> int | None:
        query = f"""--sql
        SELECT group_id FROM education_group
        WHERE group_name = '{group_name}';
        """
        result = await self._execute_query_with_returning_one_row(query)
        if result is False:
            logger.error(
                f"Error while selecting from education_groups with group_name = {group_name}")
            return None
        else:
            logger.success(
                f"Selected group_id from education_groups successfully; group_name = {group_name} with id = {result[0]}")
            return result[0]

    async def select_group_name_by_group_id(self, group_id: int) -> str | None:
        query = f"""--sql
        SELECT group_name FROM education_group
        WHERE group_id = {group_id};
        """
        result = await self._execute_query_with_returning_one_row(query)
        if result is False:
            logger.error(
                f"Error while selecting from education_groups with group_id = {group_id}")
            return None
        else:
            logger.success(
                f"Selected group_name from education_groups successfully; group_id = {group_id} with name = {result[0]}")
            return result[0]

    async def select_group_owner_id_by_group_id(self, group_id: int) -> int | None:
        query = f"""--sql
        SELECT owner_id FROM education_group
        WHERE group_id = {group_id};
        """
        result = await self._execute_query_with_returning_one_row(query)
        if result is False:
            logger.error(
                f"Error while selecting from education_groups with group_id = {group_id}")
            return None
        else:
            logger.success(
                f"Selected group_owner_id from education_groups successfully; group_id = {group_id} with id = {result[0]}")
            return result[0]

    async def check_is_user_teacher(self, user_id: int) -> bool:
        """
        Returns:
            bool: bool value 'is_teacher' for user_id in table users
        """
        query = f"""--sql
        SELECT is_teacher FROM users
        WHERE telegram_id = {user_id};
        """
        result = await self._execute_query_with_returning_one_row(query)
        if result is False:
            logger.error(
                f"Error while checking if user is teacher; user_id = {user_id}")
            return False
        else:
            logger.success(
                f"Checked if user is teacher successfully; user_id = {user_id}")
            return result[0]
