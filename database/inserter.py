from .database_connector import DatabaseConnector
from loguru import logger


class Inserter(DatabaseConnector):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Inserter for database object was initialized")

    async def insert_row_into_table(self, table_name: str, *args) -> bool:
        """
        Inserts row into table\n
        USE IT ONLY IF THIS CLASS HAS NO METHOD FOR YOUR QUERY\n

        Args:
            table_name (str): name of table to insert into
            *args (tuple): values to insert

        Returns:
            bool: result of query execution
        """
        query = f"""--sql
        INSERT INTO {table_name}
        VALUES {args};
        """
        result = await self._execute_query(query)
        if result is False:
            logger.error(
                f"Error while inserting into {table_name} with {args}")
            return False
        else:
            logger.success(f"Inserted into {table_name} successfully")
            return True

    async def insert_new_education_group(self, group_name: str, owner_id: int) -> bool:
        """Creates new education group in table 'education_groups'

        Args:
            group_name (str): name of new group, must be unique and less than 55 symbols
            owner_id (int): telegram id of group owner, can be get from message.from_user.id

        Returns:
            bool: result of query execution
        """
        query = f"""--sql
        INSERT INTO education_groups (group_name, owner_id)
        VALUES ('{group_name}', {owner_id});
        """
        result = await self._execute_query(query)
        if result is False:
            logger.error(
                f"Error while inserting into education_groups with {group_name}, {owner_id}")
            return False
        else:
            logger.success(
                f"Inserted into education_groups {group_name} with owner:{owner_id} successfully")
            return True

    async def insert_one_member_into_education_group(self, group_id: int, first_name: str, last_name: str) -> bool:
        """Adds one member into group

        Args:
            group_id (int): id of group to add member
            first_name (str): first name of member
            last_name (str): last name of member

        Returns:
            bool: result of query execution
        """

        query = f"""--sql
        INSERT INTO education_group_members (group_id, first_name, last_name)
        VALUES ({group_id}, '{first_name}', '{last_name}');
        """
        result = await self._execute_query(query)
        if result is False:
            logger.error(
                f"Error while inserting into members with {group_id}, {first_name}, {last_name}")
            return False
        else:
            logger.success(
                f"Inserted into members {group_id}, {first_name}, {last_name} successfully")
            return True

    async def insert_many_members_into_education_group(self, group_id: int, members: list[tuple[str, str]]) -> bool:
        """Adds many members into group

        Args:
            group_id (int): id of group to add members
            members (list[tuple[str,str]]): list of tuples with first and last names of members
        """
        ...
