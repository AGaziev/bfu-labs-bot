from .cloud import CloudManager


class GroupManager:

    @staticmethod
    def create_group(name: str, students: list):
        CloudManager.create_group_folder(name)
        folder_url = CloudManager.get_group_folder_link(name)
        # TODO add group to db
        return folder_url, 2023  # test group_id

    @staticmethod
    def group_name_exists(name):
        on_disk = CloudManager.is_group_exists(name)
        # in_db = TODO: check if existed in db
        return on_disk  # and in_db

    @staticmethod
    def connect_student_to_group(name, id):
        # TODO добавить запись о подключении студента в бд
        CloudManager.create_student_folder(name)