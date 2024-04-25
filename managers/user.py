from .db import DatabaseManager


class UserManager:
    @staticmethod
    def get_teacher(telegram_id):
        return DatabaseManager.get_teacher_by_telegram_id(telegram_id)

    @staticmethod
    def get_user_by_username(username):
        return DatabaseManager.get_user_by_username(username)

    @staticmethod
    def register_new_teacher(telegram_id, last_name, first_name, patronymic):
        DatabaseManager.insert_new_teacher(telegram_id, last_name, first_name, patronymic)