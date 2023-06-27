from loguru import logger

from utils.enums import Blocked
from utils.mailer import Mailer
from .cloud import CloudManager
from .db import database_manager


class LabManager:
    @staticmethod
    async def get_student_lab_stats(group_id, telegram_id) -> tuple[tuple[tuple[int, str] | None, tuple[int, str] | None]]:
        lab_statistic = await database_manager.select_students_labs_with_status_in_group(group_id, telegram_id)
        accepted_labs: list[tuple[int, str] | None] = []
        not_done_labs: list[tuple[int, str] | None] = []
        for lab_info in lab_statistic:
            if lab_info["status"] == "Сдано":
                accepted_labs.append(lab_info)
            else:
                not_done_labs.append(lab_info)
        accepted_labs = tuple(sorted(accepted_labs, key=lambda x: x[0]))
        not_done_labs = tuple(sorted(not_done_labs, key=lambda x: x[0]))
        return (accepted_labs, not_done_labs)

    @staticmethod
    async def get_student_undone_labs(group_id: int, telegram_id: int):
        undone_labs = await database_manager.select_undone_group_labs_for_student(group_id, telegram_id)
        links = tuple([lab["cloud_link"] for lab in undone_labs])
        # FIXME: зачем словарь, если ты не используешь его ключи, а в функции get_files_by_link
        # качаешь файлы по значениям словаря? в тайпхинте вообще tuple..
        files, filenames = CloudManager.get_files_by_link(links)
        return zip(files, filenames)
