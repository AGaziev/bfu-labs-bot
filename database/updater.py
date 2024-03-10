from datetime import datetime
from utils import Group, GroupMember, Status, LabWork, User


class Updater:
    @staticmethod
    def connect_user_to_group(member_id: int, telegram_id: int):
        return GroupMember.get_by_id(member_id).update(telegram_id=telegram_id)
