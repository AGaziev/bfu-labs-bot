from loguru import logger

from utils.enums import Blocked
from utils.mailer import Mailer
from .cloud import CloudManager
from .db import database_manager


class LabManager:
    @staticmethod
    def get_student_lab_stats(group_id, telegram_id) -> ([dict], [dict]):
        lab_statistic = await database_manager.select_students_labs_with_status_in_group(group_id, telegram_id)
        accepted_labs = []
        not_done_labs = []
        for lab_info in lab_statistic:
            if lab_info["status"] == "Сдано":
                accepted_labs.append(lab_info)
            else:
                not_done_labs.append(lab_info)
        return (accepted_labs, not_done_labs)
