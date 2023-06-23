from loguru import logger

from .cloud import CloudManager
from .db import database_manager


class GroupManager:

    @staticmethod
    async def create_group(name: str, students: list, teacher_id: int):
        CloudManager.create_group_folder(name)
        folder_url = CloudManager.get_group_folder_link(name)
        await database_manager.insert_new_education_group(
            group_name=name,
            owner_id=teacher_id,
            cloud_folder_link=folder_url)
        group_id = await database_manager.select_group_id_by_group_name(group_name=name)
        return folder_url, group_id

    @staticmethod
    async def is_group_name_exists(name: str):
        on_disk = CloudManager.is_group_exists(name)
        in_database = await database_manager.check_is_group_exists_by_group_name(
            group_name=name)
        print(in_database, on_disk)
        # restore cloud folder
        if in_database and not on_disk:
            CloudManager.create_group_folder(name)
        return on_disk and in_database

    @staticmethod
    async def connect_student_to_group(group_name: str,student_name: str, member_id: int, telegram_id) -> bool:
        try:
            CloudManager.create_student_folder(group_name, student_name)
            await database_manager.insert_one_registered_user(member_id, telegram_id)
        except Exception as e:
            # TODO: handle specific exceptions
            logger.error(e)
            return False
        return True

    @staticmethod
    async def get_unregistered_users_of_group(group_name):
        unregistered_users = await database_manager.select_unregistered_users_from_group(group_name=group_name)
        return {i: creds for i,creds in unregistered_users}


