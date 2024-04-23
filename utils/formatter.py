from aiogram.utils.markdown import hlink

from _legacy.laboratory_work import LaboratoryWork
from _legacy.students_labs import StudentsLabs


class Formatter:
    @staticmethod
    def list_of_students(studs: dict[int, str]):
        """
        formatting student list like:
        {id}. {creds}
        1. Иван Иванов
        2. Андрей Кутузов
        3. Евгений Пригожин
        """
        return '\n'.join([f"{id_}. {credentials}" for id_, credentials in studs.items()])

    @staticmethod
    def group_menu_lab_stats(lab_stats: StudentsLabs) -> str:
        """
        formatting lab_stats for menu:
        {accepted}/{not_done}
        Не сделаны:
        {id}.{descr}
        """
        if not lab_stats:
            return "Лабораторных еще нет :("
        accepted, not_done = len(lab_stats.accepted), len(lab_stats.not_done)
        result = f"{accepted}/{not_done + accepted}\n"
        for i, lab in enumerate(lab_stats.not_done):
            result += f"{i + 1}. {lab.description}\n"
        return result

    @staticmethod
    def list_lab_for_post(not_done_labs: list[LaboratoryWork]):
        result = ""
        for lab in not_done_labs:
            result += f"{lab.number}. {hlink(lab.description, lab.cloud_link)}\n"
        return result
