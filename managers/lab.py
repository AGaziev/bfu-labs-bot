from loguru import logger

from _legacy.laboratory_work import LaboratoryWork
from _legacy.students_labs import StudentsLabs
from managers import *
from .cloud import CloudManager
from loader import bot

from aiogram import types
from aiogram.utils.markdown import hlink


class LabManager:
    @staticmethod
    async def get_student_lab_stats(group_id: int, telegram_id: int):
        lab_statistic_of_student = await DatabaseManager.select_students_labs_with_status_in_group(group_id, telegram_id)

        accepted_labs: list = []
        not_done_labs: list = []
        # FIXME: а если == "Не проверено"?
        if lab_statistic_of_student:
            for lab_info in lab_statistic_of_student:
                current_lab = LaboratoryWork(
                    id_=lab_info["id"],
                    number=lab_info["number"],
                    description=lab_info["descr"],
                    cloud_link=lab_info["path"],
                )
                if lab_info["status"] == "Сдано":
                    accepted_labs.append(current_lab)
                else:
                    not_done_labs.append(current_lab)

        undone_labs = await DatabaseManager.select_undone_group_labs_for_student(group_id, telegram_id)
        undone_labs = [LaboratoryWork(
            id_=lab["id"],
            number=lab["lab_number"],
            description=lab["lab_description"],
            cloud_link=lab["cloud_link"],
        ) for lab in undone_labs]

        not_done_labs.extend(undone_labs)

        accepted_labs = list(sorted(accepted_labs, key=lambda x: x.number))
        not_done_labs = list(sorted(not_done_labs, key=lambda x: x.number))

        return StudentsLabs(accepted_labs, not_done_labs)

    @staticmethod
    async def get_student_undone_labs_files(group_id: int, telegram_id: int):
        undone_labs = await DatabaseManager.select_undone_group_labs_for_student(group_id, telegram_id)
        links = tuple([lab["cloud_link"] for lab in undone_labs])
        files, filenames = CloudManager.get_files_by_link(links)
        return zip(files, filenames)

    @staticmethod
    async def get_lab_link_by_path(path: str):
        return CloudManager.get_public_link_by_destination_path(path)

    @staticmethod
    async def accept_laboratory_work(lab_id: int):
        await DatabaseManager.update_lab_status(lab_id=lab_id, status='Сдано')
        lab, student_telegram_id = await DatabaseManager.select_lab_and_owner_telegram_id_by_lab_id(lab_id)
        lab_link = await LabManager.get_lab_link_by_path(lab.cloud_link)
        message = f"✅✅✅\nВаша лабораторная работа №{lab.number} была проверена и принята преподавателем\n"\
            f"Данные по работе:\n"\
            f"Название: {lab.description}\n"\
            f"{hlink('Ссылка', lab_link)} на работу\n"
        await bot.send_message(chat_id=student_telegram_id,
                               text=message,
                               parse_mode=types.ParseMode.HTML)

    @staticmethod
    async def reject_laboratory_work(lab_id: int):
        await DatabaseManager.update_lab_status(lab_id=lab_id, status='Отклонено')
        lab, student_telegram_id = await DatabaseManager.select_lab_and_owner_telegram_id_by_lab_id(lab_id)
        lab_link = await LabManager.get_lab_link_by_path(lab.cloud_link)
        message = f"❌❌❌\nВаша лабораторная работа №{lab.number} была проверена и отклонена преподавателем\n"\
            f"Данные по работе:\n"\
            f"Название: {lab.description}\n"\
            f"{hlink('Ссылка', lab_link)} на работу\n"
        await bot.send_message(chat_id=student_telegram_id,
                               text=message,
                               parse_mode=types.ParseMode.HTML)
