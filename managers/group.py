import itertools
from io import BytesIO

from loguru import logger

import utils.mailer as mailing
from utils import Group
from utils.enums import LabStatus
from utils.group_info import GroupInfo
from utils.stat_generator import StatsGenerator
from .cloud import CloudManager
from .db import DatabaseManager


class GroupManager:

    @staticmethod
    def create_group(name: str, students: list, teacher_user_id: int):
        # create in cloud
        CloudManager.create_group_folder(name)
        folder_url = CloudManager.get_group_folder_link(name)
        # create in db
        teacher = DatabaseManager.get_teacher_by_telegram_id(teacher_user_id)
        group = DatabaseManager.create_group(name, teacher.id)
        DatabaseManager.add_group_members_to_group(group, students)
        return folder_url, group.id

    @staticmethod
    def is_group_name_exists(name: str) -> bool:
        on_disk = CloudManager.is_group_exists(name)
        group = DatabaseManager.get_group_by_name(name)
        in_database = group is not None
        # restore cloud folder
        if in_database and not on_disk:
            CloudManager.create_group_folder(name)
        return on_disk and in_database

    @staticmethod
    def get_group_id_by_name(name: str):
        return DatabaseManager.get_group_by_name(name).get_id()

    @staticmethod
    def get_group_name_by_id(group_id: int):
        return DatabaseManager.get_group_by_id(group_id).name

    @staticmethod
    def connect_student_to_group(group_name: str, student_name: str, member_id: int, telegram_id) -> bool:
        try:
            CloudManager.create_student_folder(group_name, student_name)
            DatabaseManager.connect_user_to_group(member_id, telegram_id)
        except Exception as e:
            # TODO: handle specific exceptions
            logger.error(e)
            return False
        return True

    @staticmethod
    def get_unregistered_users_of_group(group_name: str) -> dict[int, str]:
        group = DatabaseManager.get_group_by_name(group_name)
        unregistered_users = DatabaseManager.select_type_members_for_group(group=group, registered=False)
        ids_and_credentials = {user.id: user.name
                               for user in unregistered_users}
        return ids_and_credentials

    @staticmethod
    def get_groups_for_student(telegram_id: int) -> list[Group]:
        user = DatabaseManager.get_user_by_telegram_id(telegram_id)
        student_groups = DatabaseManager.select_user_groups_names_with_id(user)
        return student_groups

    @staticmethod
    def is_student_already_connected(telegram_id: int, group_id: int) -> bool:
        group = DatabaseManager.get_group_by_id(group_id)
        users_in_group = DatabaseManager.select_type_members_for_group(group, True)
        return telegram_id in users_in_group

    @staticmethod
    def add_lab_to_db(group_id: int, lab_name: str, lab_link: str):
        new_lab_number = DatabaseManager.select_all_labs_count_from_group(group_id) + 1
        if (DatabaseManager.add_new_lab_to_group(group=DatabaseManager.get_group_by_id(group_id),
                                                 lab_descr=lab_name,
                                                 lab_link=lab_link,
                                                 number=new_lab_number)):
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
    async def add_lab_to_db_and_notify_students(group_id: int, lab_name: str, lab_link: str, lab_path: str):
        GroupManager.add_lab_to_db(group_id, lab_name, lab_path)
        await GroupManager.notify_group_member_about_new_lab(group_id, lab_name, lab_link)

    @staticmethod
    def get_count_of_type_members_from_group(group_id: int, registered: bool):
        group = DatabaseManager.get_group_by_id(group_id)
        members = DatabaseManager.select_type_members_for_group(group, registered)
        return len(members)

    @staticmethod
    def select_students_labs_statuses_count_from_group(group_id: int) -> tuple[int, int, int, int]:
        """
        Args:
            group_id (int): group id in database

        Returns:
            tuple[int, int, int, int]: passed, rejected, not checked, labs at all
        """
        group = DatabaseManager.get_group_by_id(group_id)
        passed = DatabaseManager.select_labs_with_status_count_from_group(group=group,
                                                                          status=LabStatus.HANDOVER)
        rejected = DatabaseManager.select_labs_with_status_count_from_group(group=group,
                                                                            status=LabStatus.REJECTED)
        not_checked = DatabaseManager.select_labs_with_status_count_from_group(group=group,
                                                                               status=LabStatus.NOTCHECKED)
        labs_at_all = DatabaseManager.select_labs_with_status_count_from_group(group=group,
                                                                               status=LabStatus.ALL)

        return passed, rejected, not_checked, labs_at_all

    @staticmethod
    def get_group_info(group_id: int):
        group = DatabaseManager.get_group_by_id(group_id)
        group_info = GroupInfo()
        group_info.registered_members_count = GroupManager.get_count_of_type_members_from_group(group_id, True)
        group_info.unregistered_members_count = GroupManager.get_count_of_type_members_from_group(group_id, False)
        group_info.students_at_all = group_info.registered_members_count + \
                                     group_info.unregistered_members_count
        group_info.lab_condition_files_count = len(DatabaseManager.select_labs_for_group(group))
        group_info.passed_labs_count, group_info.rejected_labs_count, group_info.not_checked_labs_count, group_info.labs_at_all = \
            GroupManager.select_students_labs_statuses_count_from_group(group_id)
        return group_info

    @staticmethod
    def get_group_stats_file(group_id: int):
        group = DatabaseManager.get_group_by_id(group_id)
        stats = DatabaseManager.select_lab_stats_by_whole_group(group)
        group_for_stats = DatabaseManager.get_group_by_id(group_id)
        group_name = group_for_stats.name
        lab_number = DatabaseManager.select_all_labs_count_from_group(group_id)
        info_for_generator = {}
        for name, labs in itertools.groupby(stats, key=lambda x: x.name):
            labs = list(labs)
            info_for_generator[name] = [bool(labs[0].is_registered),
                                        # bc any of elements in "labs" will have equal "is_registered"
                                        [[lab.number, lab.date, lab.status] for lab in labs if lab.number is not None]]
        if info_for_generator:
            return StatsGenerator.generate_stats(group_name, info_for_generator, lab_number)
        else:
            return False

    @staticmethod
    def get_first_not_checked_lab_in_group(group_id: int):
        return DatabaseManager.select_first_unchecked_lab_in_group(group_id=group_id)

    @staticmethod
    def get_next_not_checked_lab_in_group(group_id: int, current_lab_id: int):
        return DatabaseManager.select_next_unchecked_lab_in_group(group_id=group_id, current_lab_id=current_lab_id)

    @staticmethod
    def get_previous_not_checked_lab_in_group(group_id: int, current_lab_id: int):
        return DatabaseManager.select_previous_unchecked_lab_in_group(group_id=group_id, current_lab_id=current_lab_id)

    @staticmethod
    def post_lab_from_student(group_name: str, telegram_id: int, lab_number: int, lab_file: BytesIO,
                              file_extension: str) -> None:
        group = DatabaseManager.get_group_by_name(group_name)
        student_credentials = DatabaseManager.get_group_member_by_telegram_and_group(telegram_id=telegram_id,
                                                                                     group_id=group.id)
        lab_name, lab_id = DatabaseManager.get_lab_by_id(group_name=group_name,
                                                                            lab_number=lab_number)
        lab_name = f'{lab_name}.{file_extension}'

        cloud_path = CloudManager.add_lab_from_student(
            group_name=group_name, student_name=student_credentials, lab_path_or_file=lab_file, lab_name=lab_name)

        DatabaseManager.insert_new_lab_from_student(lab_id=lab_id, member_credentials=student_credentials,
                                                    status='Не проверено', cloud_link=cloud_path)
