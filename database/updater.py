from .database_connector import DatabaseConnector
from loguru import logger


class Updater(DatabaseConnector):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Updater for database object was initialized")
