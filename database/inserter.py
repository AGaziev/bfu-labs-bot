from handlers.error import error_handling
from utils import Group, GroupMember, LabWork, LabRegistry, Status, User


class Inserter:
    @staticmethod
    def create_group(name, teacher_id):
        try:
            Group.create(name=name, teacher_id=teacher_id).save()
        except Exception as e:
            error_handling(e,
                           f"Не смогли зарегистрировать группу {name} для учителя {teacher_id}")
            return False
        else:
            return Group

    @staticmethod
    def add_group_members_to_group(group: Group, members_names: list):
        for memberName in members_names:
            try:
                GroupMember.create(group=group, name=memberName, user=None).save()
            except Exception as e:
                error_handling(e,
                               f"Не смогли зарегистрировать участника группы {group.name} "
                               f"с айди {group.id} с именем {memberName}")
                return False
        return True

    @staticmethod
    def add_new_lab_to_group(group: Group, lab_descr: str, lab_link: str):
        try:
            LabRegistry.create(group=group, name=lab_descr, link=lab_link)
        except Exception as e:
            error_handling(e,
                           f"Не смогли зарегистрировать новую лабораторную "
                           f"для группы {group.id} с описанием {lab_descr} и ссылкой"
                           f"{lab_link}")
            return False
        return True