from loguru import logger

from _legacy.laboratory_work import LaboratoryWork
from _legacy.students_labs import StudentsLabs
from utils.enums import LabStatus
from .cloud import CloudManager
from loader import bot

from aiogram import types
from aiogram.utils.markdown import hlink

from .db import DatabaseManager


class LabManager:
    @staticmethod
    def get_student_lab_stats(group_id: int, telegram_id: int):
        user = DatabaseManager.get_user_by_telegram_id(telegram_id)
        group = DatabaseManager.get_group_by_id(group_id)
        lab_statistic_of_student = DatabaseManager.select_students_labs_with_status_in_group(group, user)

        current_lab: LaboratoryWork


        accepted_labs = filter(lambda  lab: lab.status == LabStatus.ACCEPTED.value, lab_statistic_of_student)
        undone_labs = filter(lambda lab: lab.status == LabStatus.NOTHANDOVER.value, lab_statistic_of_student)
        # TODO: выпилить это г**
        undone_labs = [LaboratoryWork(
            id_=lab.id,
            description=lab.name,
            cloud_link=lab.cloud_link,
            number=lab.number
        ) for lab in undone_labs]

        accepted_labs = [LaboratoryWork(
            id_=lab.id,
            description=lab.name,
            cloud_link=lab.cloud_link,
            number=lab.number
        ) for lab in accepted_labs]

        #accepted_labs = list(sorted(accepted_labs, key=lambda x: x.number))
        #not_done_labs = list(sorted(not_done_labs, key=lambda x: x.number))

        return StudentsLabs(accepted_labs, undone_labs)

    @staticmethod
    def get_student_undone_labs_files(group_id: int, telegram_id: int):
        student = DatabaseManager.get_group_member_by_telegram_and_group(group_id, telegram_id)
        undone_labs = DatabaseManager.select_undone_group_labs_for_student(student)
        links = tuple([lab.cloud_link for lab in undone_labs])
        files, filenames = CloudManager.get_files_by_link(links)
        return zip(files, filenames)

    @staticmethod
    def get_lab_link_by_path(path: str):
        return CloudManager.get_public_link_by_destination_path(path)

    @staticmethod
    def accept_laboratory_work(lab_id: int) -> [int, str]:
        DatabaseManager.update_lab_status(lab_id=lab_id, status='Сдано')
        lab, student_telegram_id = DatabaseManager.select_lab_and_owner_telegram_id_by_lab_id(lab_id)
        lab_link = LabManager.get_lab_link_by_path(lab.cloud_link)
        message = f"✅✅✅\nВаша лабораторная работа №{lab.number} была проверена и принята преподавателем\n" \
                  f"Данные по работе:\n" \
                  f"Название: {lab.description}\n" \
                  f"{hlink('Ссылка', lab_link)} на работу\n"
        return student_telegram_id, message

    @staticmethod
    def reject_laboratory_work(lab_id: int):
        DatabaseManager.update_lab_status(lab_id=lab_id, status='Отклонено')
        lab = DatabaseManager.get_lab_by_id(lab_id)
        student = DatabaseManager.get_group_member_by_id(lab.member)
        lab_link = LabManager.get_lab_link_by_path(lab.cloud_link)
        message = f"❌❌❌\nВаша лабораторная работа №{lab.number} была проверена и отклонена преподавателем\n" \
                  f"Данные по работе:\n" \
                  f"Название: {lab.description}\n" \
                  f"{hlink('Ссылка', lab_link)} на работу\n"
        return student.user, message

    @staticmethod
    def get_all_labs_for_group(group_id):
        group = DatabaseManager.get_group_by_id(group_id)
        return DatabaseManager.select_labs_for_group(group)

    @staticmethod
    def get_not_checked_labs_for_teacher(group_id):
        group = DatabaseManager.get_group_by_id(group_id)
        return DatabaseManager.select_labs_with_status_for_group(group, LabStatus.NOTCHECKED)

    @staticmethod
    def select_lab_condition_files_count_from_group(group_id: int):
        group = DatabaseManager.get_group_by_id(group_id)
        files = DatabaseManager.select_labs_for_group(group)
        return len(files)


        return student_telegram_id, message
