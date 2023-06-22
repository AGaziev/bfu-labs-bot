from loguru import logger
from io import BytesIO
import chardet


class TxtParser:
    def __init__(self) -> None:
        logger.debug("TxtParser object was initialized")

    @staticmethod
    def get_all_lines(file_io: BytesIO) -> list[str]:
        """Returns list of all lines in file"""
        encoding = chardet.detect(file_io.getvalue())["encoding"]
        return file_io.getvalue().decode(encoding).splitlines()
