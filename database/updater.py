from datetime import datetime
from utils import Group, GroupMember, Status, LabWork, User


class Updater:
    @staticmethod
    def connect_user_to_group(member_id: int, telegram_id: int):
        return GroupMember.update(user=telegram_id)\
            .where(GroupMember.id == member_id).execute()

    @staticmethod
    def update_lab_status(lab_id: int, status: str):
        status_id_subquery = (Status
                              .select(Status.id)
                              .where(Status.status_name == status)
                              .limit(1))

        query = (LabWork
                 .update({
            LabWork.status_id: status_id_subquery,
            LabWork.updated_at: datetime.datetime.now()
        })
                 .where(LabWork.id == lab_id))

        query.execute()

    @staticmethod
    def update_user_is_blocked_field_by_user_id(user_id, is_blocked):
        query = (User
                 .update({User.is_blocked: is_blocked})
                 .where(User.telegram_id == user_id))
        query.execute()
