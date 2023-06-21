from loguru import logger

from .ya_disk import CloudDriveManager
from .db import database_manager


class GroupManager:

    @staticmethod
    async def create_group(name: str, students: list, teacher_id: int):
        CloudDriveManager.create_group_folder(name)
        folder_url = CloudDriveManager.get_group_folder_link(name)
        await database_manager.insert_new_education_group(
            group_name=name,
            owner_id=teacher_id,
            folder_url=folder_url)
        group_id = await database_manager.select_group_id_by_group_name(group_name=name)
        return folder_url, group_id

    @staticmethod
    async def group_name_exists(name: str):
        on_disk = CloudDriveManager.is_group_exists(name)
        in_database = await database_manager.check_is_group_exists_by_group_name(
            group_name=name)
        return on_disk and in_database

    @staticmethod
    def connect_student_to_group(name: str, id: int) -> bool:
        # TODO добавить запись о подключении студента в бд
        try:
            CloudDriveManager.create_student_folder(name)
            ...
        except Exception as e:
            # TODO: handle specific exceptions
            logger.error(e)
            return False
        return True
