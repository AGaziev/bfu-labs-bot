import os
from dotenv import load_dotenv
from loguru import logger


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
    def admins(self) -> tuple[int, ...]:
        return self._admins

    def _get_admins(self) -> tuple:
        try:
            admins = tuple(map(int, os.getenv('ADMINS').split(',')))
        except AttributeError:
            logger.error("ADMINS environment variable is not set")
            admins = ()

        return admins

    def _get_database_connection_parameters(self) -> dict:
        dotenv_variables = ('DB_USER', 'DB_USER_PASSWORD',
                            'DB_HOST', 'DB_PORT', 'DB_NAME')
        keys = ('user', 'password', 'host', 'port', 'database')
        pairs = zip(keys, dotenv_variables)
        parameters = {}
        for key, dotenv_variable in pairs:
            try:
                parameters.update({key: os.getenv(dotenv_variable)})
            except AttributeError:
                logger.error(
                    f"{dotenv_variable} environment variable is not set")
                parameters.update({key: None})

        return parameters
