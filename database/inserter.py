from handlers.error import error_handling
from utils import Group, GroupMember


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