from loguru import logger

from utils.enums import Blocked
from utils.mailer import Mailer
from .cloud import CloudManager
from .db import database_manager

class LabManager:
    @staticmethod
    def get_student_lab_stats(group_id, telegram_id):
        lab_statistic = await database_manager.select_students_labs_with_status_in_group(group_id, telegram_id)
        for lab_info in lab_statistic:
            pass

