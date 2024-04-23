from loguru import logger

from _legacy.laboratory_work import LaboratoryWork
from _legacy.students_labs import StudentsLabs
from .cloud import CloudManager
from loader import bot

from aiogram import types
from aiogram.utils.markdown import hlink

from .db import DatabaseManager


class LabManager:
    @staticmethod
    def get_student_lab_stats(group_id: int, telegram_id: int):
        lab_statistic_of_student = DatabaseManager.select_students_labs_with_status_in_group(group_id, telegram_id)

        accepted_labs: list = []
        not_done_labs: list = []
        # FIXME: а если == "Не проверено"?
        if lab_statistic_of_student:
            for lab_info in lab_statistic_of_student:
                current_lab = LaboratoryWork(
                    id_=lab_info.id,
                    description=lab_info.name,
                    cloud_link=lab_info.cloud_link,
                )
                if lab_info["status"] == "Сдано":
                    accepted_labs.append(current_lab)
                else:
                    not_done_labs.append(current_lab)

        undone_labs = DatabaseManager.select_undone_group_labs_for_student(group_id, telegram_id)
        undone_labs = [LaboratoryWork(
            id_=lab.id,
            description=lab.name,
            cloud_link=lab.cloud_link,
        ) for lab in undone_labs]

        not_done_labs.extend(undone_labs)

        accepted_labs = list(sorted(accepted_labs, key=lambda x: x.number))
        not_done_labs = list(sorted(not_done_labs, key=lambda x: x.number))

        return StudentsLabs(accepted_labs, not_done_labs)

    @staticmethod
    def get_student_undone_labs_files(group_id: int, telegram_id: int):
        undone_labs = DatabaseManager.select_undone_group_labs_for_student(group_id, telegram_id)
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
        lab, student_telegram_id = DatabaseManager.select_lab_and_owner_telegram_id_by_lab_id(lab_id)
        lab_link = LabManager.get_lab_link_by_path(lab.cloud_link)
        message = f"❌❌❌\nВаша лабораторная работа №{lab.number} была проверена и отклонена преподавателем\n" \
                  f"Данные по работе:\n" \
                  f"Название: {lab.description}\n" \
                  f"{hlink('Ссылка', lab_link)} на работу\n"
        return student_telegram_id, message
