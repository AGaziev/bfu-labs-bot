from repositories.disk import disk as cloud_drive


class CloudManager:
    @classmethod
    def create_group_folder(cls, group_name: str):
        dst_path = f"/{group_name}"
        cloud_drive.mkdir(dst_path)
        cls.make_group_public(group_name)
        cloud_drive.mkdir(dst_path + "/Лабораторные")

    @staticmethod
    def create_student_folder(group_name: str, student_name: str):
        dst_path = f"/{group_name}/{student_name}"
        cloud_drive.mkdir(dst_path)
        return dst_path

    @staticmethod
    def add_lab_to_group_folder(group_name: str, lab_path: str, lab_name: str):
        dst_path = f"/{group_name}/Лабораторные/{lab_name}"
        cloud_drive.upload(lab_path, dst_path)
        return dst_path

    @staticmethod
    def add_lab_from_student(group_name: str, student_name: str, lab_path: str, lab_name: str):
        student_lab_name = student_name + "_" + lab_name
        dst_path = f"/{group_name}/{student_name}/{student_lab_name}"
        cloud_drive.upload(lab_path, dst_path)
        return dst_path

    @staticmethod
    def make_group_public(group_name: str):
        cloud_drive.publish(f"/{group_name}")

    @staticmethod
    def get_group_folder_link(group_name: str):
        return cloud_drive.get_meta(f"/{group_name}").public_url

    @classmethod
    def is_group_exists(cls, group_name: str):
        return cloud_drive.exists(f"/{group_name}")
