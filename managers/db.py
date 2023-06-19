from loguru import logger
from database import Inserter, Selector, Updater, Deleter


class DatabaseManager(Inserter, Selector, Updater, Deleter):
    """Class representing database manager, which contains all database operations\n
        CRUD operations are separated into different classes\n

    Args:
        Inserter (class): CREATE
        Selector (class): READ
        Updater (class): UPDATE
        Deleter (class): DELETE
    """

    def __init__(self) -> None:
        super().__init__()
        logger.debug("Database manager object was initialized")


database_manager = DatabaseManager()
