from .database_connector import DatabaseConnector
from loguru import logger


class Creator(DatabaseConnector):
    """
    Class for creating database tables
    """

    def __init__(self) -> None:
        super().__init__()
        logger.debug("Creator for database object was initialized")

    async def _create_table_users(self) -> None:
        query = """--sql
        CREATE TABLE IF NOT EXISTS users (
            telegram_id BIGINT PRIMARY KEY,
            username VARCHAR(32) NOT NULL,
            is_blocked BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
        """
        if await self._execute_query(query) is False:
            logger.error("Error while creating users table")
        else:
            logger.success("Table users was created successfully")

    async def _create_table_teacher(self) -> None:
        query = """--sql
        CREATE TABLE IF NOT EXISTS teacher (
            telegram_id BIGINT NOT NULL REFERENCES users(telegram_id),
            first_name VARCHAR(55) NOT NULL,
            last_name VARCHAR(55) NOT NULL,
            patronymic VARCHAR(55),
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            PRIMARY KEY (telegram_id)
        );
        """
        if await self._execute_query(query) is False:
            logger.error("Error while creating teacher table")
        else:
            logger.success("Table teacher was created successfully")

    async def _create_table_education_group(self) -> None:
        query = """--sql
        CREATE TABLE IF NOT EXISTS education_group (
            id SERIAL PRIMARY KEY,
            group_name VARCHAR(55) NOT NULL UNIQUE,
            owner_id BIGINT NOT NULL REFERENCES users(telegram_id),
            cloud_folder_link TEXT NOT NULL
        );
        """
        if await self._execute_query(query) is False:
            logger.error("Error while creating education_group table")
        else:
            logger.success("Table education_group was created successfully")

    async def _create_table_education_group_members(self) -> None:
        query = """--sql
        CREATE TABLE IF NOT EXISTS education_group_members (
            member_id SERIAL PRIMARY KEY,
            group_id INT NOT NULL REFERENCES education_group(id),
            credentials VARCHAR(255) NOT NULL
        );
        """
        if await self._execute_query(query) is False:
            logger.error("Error while creating education_group_members table")
        else:
            logger.success(
                "Table education_group_members was created successfully")

    async def _create_table_registered_members(self) -> None:
        query = """--sql
        CREATE TABLE IF NOT EXISTS registered_members (
            member_id INT REFERENCES education_group_members(member_id) PRIMARY KEY,
            telegram_id BIGINT NOT NULL REFERENCES users(telegram_id)
        );
        """
        if await self._execute_query(query) is False:
            logger.error("Error while creating registered_members table")
        else:
            logger.success("Table registered_members was created successfully")

    async def _create_table_lab_status_type(self) -> None:
        query = """--sql
        CREATE TABLE IF NOT EXISTS lab_status_type (
            id SERIAL PRIMARY KEY,
            status_name VARCHAR(55) NOT NULL
        );
        """
        if await self._execute_query(query) is False:
            logger.error("Error while creating lab_status_type table")
        else:
            logger.success("Table lab_status_type was created successfully")

    async def _create_table_lab_registry(self) -> None:
        query = """--sql
        CREATE TABLE IF NOT EXISTS lab_registry (
            id SERIAL PRIMARY KEY,
            lab_number INT NOT NULL,
            lab_description VARCHAR(255) NOT NULL,
            cloud_link TEXT NOT NULL,
            group_id INT NOT NULL REFERENCES education_group(id),
            created_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
        """
        if await self._execute_query(query) is False:
            logger.error("Error while creating lab_registry table")
        else:
            logger.success("Table lab_registry was created successfully")

    async def _create_table_lab_tracker(self) -> None:
        query = """--sql
        CREATE TABLE IF NOT EXISTS lab_tracker (
            id SERIAL PRIMARY KEY,
            lab_id INT NOT NULL REFERENCES lab_registry(id),
            member_id INT NOT NULL REFERENCES registered_members(member_id),
            status_id INT NOT NULL REFERENCES lab_status_type(id),
            cloud_link TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
            UNIQUE (lab_id, member_id)
        );
        """
        if await self._execute_query(query) is False:
            logger.error("Error while creating lab_tracker table")
        else:
            logger.success("Table lab_tracker was created successfully")

    async def _drop_all_tables(self) -> None:
        """
        Drop all tables from database on CASCADE mode if they exist
        """
        tables = ('lab_tracker', 'lab_registry', 'lab_status_type',
                  'registered_members', 'education_group_members',
                  'education_group', 'teacher', 'users')

        logger.warning("Dropping all tables from database")

        for table in tables:
            query = f"DROP TABLE IF EXISTS {table} CASCADE;"
            if await self._execute_query(query) is False:
                logger.error(f"Error while dropping {table} table")
            else:
                logger.success(f"Table [{table}] was dropped successfully")

        logger.warning("Finished dropping all tables from database")

    async def recreate_all_tables(self) -> None:
        """
        Recreate all tables in database
        """
        logger.warning("Recreating all tables in database")
        await self._drop_all_tables()
        logger.warning("Creating all tables in database")
        await self._create_table_users()
        await self._create_table_teacher()
        await self._create_table_education_group()
        await self._create_table_education_group_members()
        await self._create_table_registered_members()
        await self._create_table_lab_status_type()
        await self._create_table_lab_registry()
        await self._create_table_lab_tracker()
        logger.warning("Finished recreating all tables in database")


