from loguru import logger


class TxtParser:
    def __init__(self, filepath: str) -> None:
        logger.debug("TxtParser object was initialized")
        self._filepath = filepath

    def get_all_lines(self) -> list:
        """Returns list of all lines in file"""
        with open(self._filepath, 'r', encoding='utf-8') as file:
            return file.readlines()
