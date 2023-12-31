from .database_connector import DatabaseConnector
from loguru import logger


class Deleter(DatabaseConnector):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Deleter for database object was initialized")
