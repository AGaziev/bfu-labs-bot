from loguru import logger

from utils.enums import Blocked
from utils.mailer import Mailer
from .cloud import CloudManager
from .db import database_manager
from utils.models import StudentsLabs, LaboratoryWork


class LabManager:
    @staticmethod
    async def get_student_lab_stats(group_id: int, telegram_id: int) -> StudentsLabs | None:
        lab_statistic_of_student = await database_manager.select_students_labs_with_status_in_group(group_id, telegram_id)

        accepted_labs: list[LaboratoryWork | None] = []
        not_done_labs: list[LaboratoryWork | None] = []
        # FIXME: а если == "Не проверено"?
        if lab_statistic_of_student:
            for lab_info in lab_statistic_of_student:
                current_lab = LaboratoryWork(
                    lab_id=lab_info["id"],
                    number=lab_info["number"],
                    description=lab_info["descr"],
                    cloud_link=lab_info["path"],
                )
                if lab_info["status"] == "Сдано":
                    accepted_labs.append(current_lab)
                else:
                    not_done_labs.append(current_lab)

        undone_labs = await database_manager.select_undone_group_labs_for_student(group_id, telegram_id)
        undone_labs = [LaboratoryWork(
            lab_id=lab["id"],
            number=lab["lab_number"],
            description=lab["lab_description"],
            cloud_link=lab["cloud_link"],
        ) for lab in undone_labs]

        not_done_labs.extend(undone_labs)

        accepted_labs = list(sorted(accepted_labs, key=lambda x: x.number))
        not_done_labs = list(sorted(not_done_labs, key=lambda x: x.number))

        return StudentsLabs(accepted_labs, not_done_labs)

    @staticmethod
    async def get_student_undone_labs_files(group_id: int, telegram_id: int):
        undone_labs = await database_manager.select_undone_group_labs_for_student(group_id, telegram_id)
        links = tuple([lab["cloud_link"] for lab in undone_labs])
        files, filenames = CloudManager.get_files_by_link(links)
        return zip(files, filenames)

    @staticmethod
    async def get_lab_link_by_path(path):
        return CloudManager.get_public_link_by_destination_path(path)

    @staticmethod
    async def accept_laboratory_work(lab_id: int):
        # TODO: update lab status in database and send notification to student
        ...

    @staticmethod
    async def reject_laboratory_work(lab_id: int):
        # TODO: update lab status in database and send notification to student
        ...
