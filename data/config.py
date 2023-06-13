import os
from dotenv import load_dotenv


class Config:
    def __init__(self) -> None:
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path, override=True)
        self._bot_token = os.getenv('BOT_TOKEN')
        self._cloud_drive_token = os.getenv('YANDEX_DISK_TOKEN')
        self._admins = self._get_admins()
        self._database_connection_parameters = self._get_database_connection_parameters()

    @property
    def bot_token(self) -> str:
        return self._bot_token

    @property
    def cloud_drive_token(self) -> str:
        return self._cloud_drive_token

    @property
    def database_connection_parameters(self) -> dict:
        return self._database_connection_parameters

    @property
    def admins(self) -> list:
        return self._admins

    def _get_admins(self) -> list:
        return list(map(int, os.getenv('ADMINS').split(',')))

    def _get_database_connection_parameters(self) -> dict:
        return {
            "user": os.getenv('DB_USER'),
            "password": os.getenv('DB_USER_PASSWORD'),
            "host": os.getenv('DB_HOST'),
            "port": os.getenv('DB_PORT'),
            "database": os.getenv('DB_NAME')
        }
