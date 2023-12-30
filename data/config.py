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

    @property
    def bot_token(self) -> str:
        return self.bot_token

    @property
    def cloud_drive_token(self) -> str:
        return self.cloud_drive_token

    @property
    def database_connection_parameters(self) -> dict:
        return self.database_connection_parameters

    @property
    def admins(self) -> tuple[int, ...]:
        return self.admins

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
        user = os.getenv('DB_USER')
        password = os.getenv('DB_USER_PASSWORD')
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        database = os.getenv('DB_NAME')
