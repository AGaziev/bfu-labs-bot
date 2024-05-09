from datetime import datetime

from database import Selector
from utils import Group, GroupMember, Status, LabWork, User
from utils.enums import LabStatus


class Updater:
    @staticmethod
    def connect_user_to_group(member_id: int, telegram_id: int):
        return GroupMember.update(user=telegram_id)\
            .where(GroupMember.id == member_id).execute()

    @staticmethod
    def update_lab_status(lab: LabWork, status: LabStatus):
        new_status: Status = Selector.get_status(status)

        query = (LabWork
                 .update({
            LabWork.status_id: new_status.id,
            LabWork.updated_at: datetime.now()
        })
                 .where(LabWork.id == lab.id))

        query.execute()

    @staticmethod
    def update_user_is_blocked_field_by_user_id(user_id, is_blocked):
        query = (User
                 .update({User.is_blocked: is_blocked})
                 .where(User.telegram_id == user_id))
        query.execute()
