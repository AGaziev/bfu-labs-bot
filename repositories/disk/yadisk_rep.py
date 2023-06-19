import yadisk
from data import configuration
from loguru import logger
import os


class CloudDriveManager:
    def __init__(self) -> None:
        from database import DatabaseManager
        self._drive = yadisk.YaDisk(token=configuration.cloud_drive_token)
        self._db_manager = DatabaseManager()

    def _delete_temp_file(self, file_path: str) -> None:
        """Deletes file from local machine

        Args:
            file_path (str): path to file
        """
        try:
            file_abs_path = os.path.abspath(file_path)
            os.remove(file_abs_path)
        except FileNotFoundError:
            logger.warning(f"File {file_abs_path} not found")
        else:
            logger.info(f"File {file_abs_path} deleted successfully")

    async def _create_group_repository(self, group_id: int) -> bool:
        """Creates group repository on cloud drive

        Args:
            group_id (int): group id in database

        Returns:
            bool: True if group repository was created, False otherwise
        """
        group_name = await self._db_manager.select_group_name_by_group_id(group_id)
        owner_credentials = await self._db_manager.select_teacher_by_group_id(
            group_id)
        repository_name = f"{group_name}_{owner_credentials.firstname}_{owner_credentials.lastname}"
        if owner_credentials.patronymic:
            repository_name += f"_{owner_credentials.patronymic}"

        # TODO: create repository on cloud drive
        ...

    def upload_lab_rules_file(self, group_id: int, file_path: str):
        """Uploads lab rules file to cloud drive

        Args:
            group_id (int): group id in database
            file_path (str): path to file on local machine
        """

        # TODO: maybe we can unzip files if teacher uploads zip archive? or it's bad idea?
        # upload file to cloud drive
        ...
        # delete file from local machine
        self._delete_temp_file(file_path)

    def upload_user_solved_lab_file(self, user_id: int, file_path: str):
        """Uploads user solved lab file to cloud drive

        Args:
            user_id (int): telegram user id in database
            file_path (str): path to file on local machine
        """
        # upload file to cloud drive
        ...
        # delete file from local machine
        self._delete_temp_file(file_path)
