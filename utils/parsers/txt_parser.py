from loguru import logger
from io import BytesIO


class TxtParser:
    def __init__(self) -> None:
        logger.debug("TxtParser object was initialized")

    @staticmethod
    def get_all_lines(file_io: BytesIO) -> list[str]:
        """Returns list of all lines in file"""
        return file_io.getvalue().decode("utf-8").splitlines()
