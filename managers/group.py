from .ya_disk import DiskManager


class GroupManager:

    @staticmethod
    def create_group(name: str, students: list):
        DiskManager.create_group_folder(name)
        folder_url = DiskManager.get_group_folder_link(name)
        # TODO add group to db
        return folder_url, 2023  # test group_id

    @staticmethod
    def group_name_exists(name):
        on_disk = DiskManager.is_group_exists(name)
        # in_db = TODO: check if existed in db
        return on_disk  # and in_db
