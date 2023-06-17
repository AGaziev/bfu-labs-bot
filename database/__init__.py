from loguru import logger
from .inserter import Inserter
from .selector import Selector
from .updater import Updater
from .deleter import Deleter

try:
    from .creator import configure_database_tables
except ImportError:
    logger.error("Error while importing creator.py")


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
