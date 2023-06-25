from loguru import logger

from utils.enums import Blocked
import utils.mailer as mailing
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
        await database_manager.insert_many_members_into_education_group(group_id=group_id,
                                                                        members=students)
        return folder_url, group_id

    @staticmethod
    async def is_group_name_exists(name: str):
        on_disk = CloudManager.is_group_exists(name)
        in_database = await database_manager.check_is_group_exists_by_group_name(
            group_name=name)
        # restore cloud folder
        if in_database and not on_disk:
            CloudManager.create_group_folder(name)
        return on_disk and in_database

    @staticmethod
    async def get_group_id_by_name(name: str):
        return await database_manager.select_group_id_by_group_name(group_name=name)

    @staticmethod
    async def get_group_name_by_id(id_: int):
        return await database_manager.select_group_name_by_group_id(group_id=id_)

    @staticmethod
    async def connect_student_to_group(group_name: str, student_name: str, member_id: int, telegram_id) -> bool:
        try:
            CloudManager.create_student_folder(group_name, student_name)
            await database_manager.insert_one_registered_user(member_id, telegram_id)
        except Exception as e:
            # TODO: handle specific exceptions
            logger.error(e)
            return False
        return True

    @staticmethod
    async def get_unregistered_users_of_group(group_name: str):
        unregistered_users = await database_manager.select_unregistered_users_from_group(group_name=group_name)
        ids_and_credentials = {record[0]: record[1]
                               for record in unregistered_users}
        return ids_and_credentials

    @staticmethod
    async def get_groups_for_student(telegram_id: int):
        student_groups = await database_manager.select_student_groups_names_with_id(telegram_id)
        return student_groups

    @staticmethod
    async def is_student_already_connected(telegram_id: int, group_id: int):
        users_in_group = await database_manager.select_registered_members_from_group(
            group_id, is_blocked=Blocked.ANY)
        return telegram_id in users_in_group

    @staticmethod
    async def add_lab_to_db(group_id: int, lab_name: str, lab_link: str):
        if await database_manager.insert_new_lab_link(group_id=group_id, lab_description=lab_name, cloud_link=lab_link):
            logger.success(f"Added lab {lab_name} to group {group_id}")
        else:
            logger.error(
                f"Error while adding lab {lab_name} to group {group_id}")

    @staticmethod
    async def notify_group_member_about_new_lab(group_id: int, lab_name: str, link_to_lab: str):
        mailer = mailing.Mailer()
        await mailer.send_notification_to_education_group(
            group_id=group_id, description=lab_name, link_to_lab=link_to_lab)

    @staticmethod
    async def add_lab_to_db_and_notify_students(group_id: int, lab_name: str, lab_link: str):
        await GroupManager.add_lab_to_db(group_id, lab_name, lab_link)
        await GroupManager.notify_group_member_about_new_lab(group_id, lab_name, lab_link)
