from loguru import logger
from io import BytesIO


class CsvParser:
    def __init__(self) -> None:
        logger.debug("Csv parser object was initialized")
