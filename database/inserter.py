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

    async def insert_new_user(self, user_id: int, username: str) -> bool:
        """Creates new user in table 'users'

        Args:
            user_id (int): telegram id of user, can be get from message.from_user.id
            username (str): telegram username of user, can be get from message.from_user.username

        Returns:
            bool: result of query execution
        """
        query = f"""--sql
        INSERT INTO users (telegram_id, username)
        VALUES ({user_id}, '{username}');
        """
        result = await self._execute_query(query)
        if result is False:
            logger.error(f"Error while inserting into users with {user_id}")
            return False
        else:
            logger.success(
                f"Inserted into users {user_id} with username:{username} successfully")
            return True

    async def insert_new_education_group(self, group_name: str, owner_id: int, cloud_folder_link: str) -> bool:
        """Creates new education group in table 'education_groups'

        Args:
            group_name (str): name of new group, must be unique and less than 55 symbols
            owner_id (int): telegram id of group owner, can be get from message.from_user.id

        Returns:
            bool: result of query execution
        """
        query = f"""--sql
        INSERT INTO education_group (group_name, owner_id, cloud_folder_link)
        VALUES ('{group_name}', {owner_id}, '{cloud_folder_link}');
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

    async def insert_one_member_into_education_group(self, group_id: int, credentials: str) -> bool:
        """Adds one member into group

        Args:
            group_id (int): id of group to add member
            credentials (str): credentials of member in format 'firstname lastname' or 'firstname lastname patronymic'

        Returns:
            bool: result of query execution
        """

        query = f"""--sql
        INSERT INTO education_group_members (group_id, credentials)
        VALUES ({group_id}, '{credentials}');
        """
        result = await self._execute_query(query)
        if result is False:
            logger.error(
                f"Error while inserting into members with {group_id}, {credentials}")
            return False
        else:
            logger.success(
                f"Inserted into members {group_id}, {credentials} successfully")
            return True

    async def insert_many_members_into_education_group(self, group_id: int, members: list[str]) -> bool:
        """Adds many members into group

        Args:
            group_id (int): id of group to add members
            members (list[str]): list of members in format 'firstname lastname' or 'firstname lastname patronymic'
        """
        query = f"""--sql
        INSERT INTO education_group_members (group_id, credentials)
        VALUES {', '.join([f"({group_id}, '{member}')" for member in members])};
        """
        result = await self._execute_query(query)
        if result is False:
            logger.error(
                f"Error while inserting into members with {group_id}, {members}")
            return False
        else:
            logger.success(
                f"Inserted into members group_id:{group_id}, members:{members} successfully")
            return True

    async def insert_new_teacher(self, telegram_id: int, first_name: str, last_name: str, patronymic: str | None = None) -> bool:
        """Creates new teacher in table 'teachers'
            Args:
                telegram_id (int): telegram id of teacher, can be get from message.from_user.id
                first_name (str): first name of teacher
                last_name (str): last name of teacher
                patronymic (str|None): patronymic of teacher, can be None if teacher doesn't have it
            Returns:
                bool: result of query execution
        """
        query = f"""--sql
        INSERT INTO teacher (telegram_id, first_name, last_name, patronymic)
        VALUES ({telegram_id}, '{first_name}', '{last_name}', '{patronymic}');
        """
        result = await self._execute_query(query)
        if result is False:
            logger.error(
                f"Error while inserting into teachers with {telegram_id}, {first_name}, {last_name}, {patronymic}")
            return False
        else:
            logger.success(
                f"Inserted into teachers {telegram_id}, {first_name}, {last_name}, {patronymic} successfully")
            return True
