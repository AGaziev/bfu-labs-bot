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
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Database manager object was initialized")
