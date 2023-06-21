from .database_connector import DatabaseConnector
from loguru import logger
from typing import Any
from utils.models import Teacher


class Selector(DatabaseConnector):
    """
    Class for selecting data from database\n
    """

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
            bool: bool value if user_id (telegram_id column) in teacher table
        """
        query = f"""--sql
        SELECT EXISTS(SELECT 1 FROM teacher WHERE telegram_id = {user_id});
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

    async def select_registered_unblocked_members_from_group(self, group_id: int) -> tuple[int, ...]:
        query = f"""--sql
        SELECT user_id FROM registered_members
        WHERE member_id IN (SELECT member_id FROM education_group_members
        WHERE group_id = {group_id})
        AND user_id IN (SELECT telegram_id FROM users
        WHERE is_blocked = FALSE);
        """

        result = await self._execute_query(query)
        if result is False:
            logger.error(
                f"Error while selecting registered members from group; group_id = {group_id}")
            raise AttributeError(
                f"Registered members not found; group_id = {group_id}")
        else:
            logger.success(
                f"Selected registered members from group successfully; group_id = {group_id}")
            return tuple([iterable[0] for iterable in result])

    async def _select_group_owner_by_group_id(self, group_id: int) -> list[str]:
        """
        Returns:
            list[str]: list of group owner first_name, last_name, patronymic
        """
        query = f"""--sql
        SELECT first_name, last_name, patronymic FROM teachers
        WHERE telegram_id = (SELECT owner_id FROM education_group
        WHERE group_id = {group_id});
        """

        result = await self._execute_query_with_returning_one_row(query)
        if result is False:
            logger.error(
                f"Error while selecting group owner by group_id; group_id = {group_id}")
            raise AttributeError(
                f"Group owner not found; group_id = {group_id}")
        else:
            logger.success(
                f"Selected group owner by group_id successfully; group_id = {group_id}; owner = {result}")
            return result

    async def _select_owner_username_by_group_id(self, group_id: int) -> str:
        query = f"""--sql
        SELECT username FROM users
        WHERE telegram_id = (SELECT owner_id FROM education_group
        WHERE group_id = {group_id});
        """

        result = await self._execute_query_with_returning_one_row(query)
        if result is False:
            logger.error(
                f"Error while selecting owner username by group_id; group_id = {group_id}")
            raise AttributeError(
                f"Owner username not found; group_id = {group_id}")
        else:
            logger.success(
                f"Selected owner username by group_id successfully; group_id = {group_id}; username = {result[0]}")
            return result[0]

    async def select_teacher_by_group_id(self, group_id: int) -> Teacher:
        """
        Returns:
            Teacher: Teacher object, representing teacher of group with field names:
                first_name, last_name, patronymic, username
        """
        teacher = Teacher()
        teacher.first_name, teacher.last_name, teacher.patronymic = await self._select_group_owner_by_group_id(
            group_id)
        teacher.username = await self._select_owner_username_by_group_id(
            group_id)
        return teacher

    async def select_group_name_by_group_id(self, group_id: int) -> str | None:
        query = f"""--sql
        SELECT group_name FROM education_group
        WHERE group_id = {group_id};
        """
        result = await self._execute_query_with_returning_one_row(query)
        if result is False:
            logger.error(
                f"Error while selecting group_name by group_id; group_id = {group_id}")
            return None
        else:
            logger.success(
                f"Selected group_name by group_id successfully; group_id = {group_id}; group_name = {result[0]}")
            return result[0]

    async def select_member_firstname_and_lastname_by_telegram_id_and_group_id(self, telegram_id: int, group_id: int) -> tuple[str, str] | None:
        query = f"""--sql
        SELECT first_name, last_name FROM education_group_members
        WHERE member_id = (SELECT member_id FROM registered_members
        WHERE user_id = {telegram_id})
        AND group_id = {group_id};
        """
        result = await self._execute_query_with_returning_one_row(query)
        if result is False:
            logger.error(
                f"Error while selecting member firstname and lastname by telegram_id and group_id; telegram_id = {telegram_id}; group_id = {group_id}")
            return None
        else:
            logger.success(
                f"Selected member firstname and lastname by telegram_id and group_id successfully; telegram_id = {telegram_id}; group_id = {group_id}; firstname = {result[0]}; lastname = {result[1]}")
            return result

    async def select_teacher_credentials_by_telegram_id(self, telegram_id: int) -> Teacher:
        """
        Returns:
            Teacher: Teacher object, representing teacher with field names:
                first_name, last_name, patronymic, WITHOUT username
        """
        query = f"""--sql
        SELECT first_name, last_name, patronymic FROM teachers
        WHERE telegram_id = {telegram_id};
        """
        result = await self._execute_query_with_returning_one_row(query)
        if result is False:
            logger.error(
                f"Error while selecting teacher credentials by telegram_id; telegram_id = {telegram_id}")
            raise AttributeError(
                f"Teacher credentials not found; telegram_id = {telegram_id}")
        else:
            logger.success(
                f"Selected teacher credentials by telegram_id successfully; telegram_id = {telegram_id}; credentials = {result}")
            teacher = Teacher()
            teacher.firstname, teacher.lastname, teacher.patronymic = result
            return teacher

    async def select_group_ids_and_names_owned_by_telegram_id(self, telegram_id: int) -> list[tuple[int, str]]:
        query = f"""--sql
        SELECT group_id, group_name FROM education_group
        WHERE owner_id = {telegram_id};
        """
        result = await self._execute_query(query)
        if result is False:
            logger.error(
                f"Error while selecting group ids and names owned by telegram_id; telegram_id = {telegram_id}")
            raise AttributeError(
                f"Groups not found; telegram_id = {telegram_id}")
        else:
            logger.success(
                f"Selected group ids and names owned by telegram_id successfully; telegram_id = {telegram_id}; groups = {result}")
            return result

    async def select_telegram_id_by_username(self, username: str) -> int | None:
        query = f"""--sql
        SELECT telegram_id FROM users
        WHERE username = '{username}';
        """
        result = await self._execute_query_with_returning_one_row(query)
        if result in (False, None):
            logger.error(
                f"Error while selecting telegram_id by username; username = {username}")
            return None
        else:
            logger.success(
                f"Selected telegram_id by username successfully; username = {username}; telegram_id = {result[0]}")
            return result[0]

    async def check_is_user_joined_any_education_group(self, telegram_id: int) -> bool:
        query = f"""--sql
        SELECT EXISTS(SELECT * FROM registered_members
        WHERE telegram_id = {telegram_id});
        """
        result = await self._execute_query_with_returning_one_row(query)
        if result is False:
            logger.error(
                f"Error while checking is user joined any education group; telegram_id = {telegram_id}")
            return False
        else:
            logger.success(
                f"Checked is user joined any education group successfully; telegram_id = {telegram_id}; result = {result[0]}")
            return result[0]

    async def check_is_group_exists_by_group_name(self, group_name: str) -> bool:
        query = f"""--sql
        SELECT EXISTS(SELECT * FROM education_group
        WHERE group_name = '{group_name}');
        """
        result = await self._execute_query_with_returning_one_row(query)
        if result is False:
            logger.error(
                f"Error while checking is group exists by group_name; group_name = {group_name}")
            return False
        else:
            logger.success(
                f"Checked is group exists by group_name successfully; group_name = {group_name}; result = {result[0]}")
            return result[0]
