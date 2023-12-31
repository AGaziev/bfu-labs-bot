import os
from dotenv import load_dotenv
from loguru import logger


class Config:
    def __init__(self) -> None:
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path, override=True)
        self.bot_token = os.getenv('BOT_TOKEN')
        self.cloud_drive_token = os.getenv('YANDEX_DISK_TOKEN')
        self.admins = self._get_admins()
        self.database_connection_parameters : DBCreds = DBCreds()

    def _get_admins(self) -> tuple:
        try:
            admins = tuple(map(int, [telegram_id for telegram_id in os.getenv(
                'ADMINS').split(',') if telegram_id != '']))
        except AttributeError:
            logger.error("ADMINS environment variable is not set")
            admins = ()

        return admins


class DBCreds():
    def __init__(self):
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_USER_PASSWORD')
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT')
        self.database = os.getenv('DB_NAME')
