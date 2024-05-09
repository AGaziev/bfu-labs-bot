from peewee import fn

from handlers.error import error_handling
from utils import Group, GroupMember, LabWork, LabRegistry, Status, User, Teacher


class Inserter:
    @staticmethod
    def create_group(name, teacher_id):
        try:
            group = Group.create(name=name, teacher_id=teacher_id)
            group.save()
        except Exception as e:
            print(f"Не смогли зарегистрировать группу {name} для учителя {teacher_id}" + str(e))
            return False
        else:
            return group

    @staticmethod
    def add_group_members_to_group(group: Group, members_names: list):
        for memberName in members_names:
            try:
                GroupMember.create(group=group, name=memberName, user=None).save()
            except Exception as e:
                print(f"Не смогли зарегистрировать участника группы {group.name} "
                      f"с айди {group.id} с именем {memberName}" + str(e))
                return False
        return True

    @staticmethod
    def add_new_lab_to_group(group: Group, lab_descr: str, lab_link: str, number: int):
        try:
            LabRegistry.create(group=group, name=lab_descr, cloud_link=lab_link, number=number)
        except Exception as e:
            print(f"Не смогли зарегистрировать новую лабораторную "
                  f"для группы {group.id} с описанием {lab_descr} и ссылкой"
                  f"{lab_link}" + str(e))
            return False
        return True

    @staticmethod
    def insert_new_lab_from_student(lab_id: LabRegistry, member: GroupMember, status: Status, cloud_link):
        insert_query = (LabWork
        .insert({
            LabWork.lab_id: lab_id,
            LabWork.member_id: member.id,
            LabWork.status_id: status.id,
            LabWork.cloud_link: cloud_link
        }))
        insert_query.execute()

    @staticmethod
    def insert_new_user(user_id, username):
        query = (User
                 .insert(telegram_id=user_id, username=username))

        query.execute()

    @staticmethod
    def insert_new_teacher(telegram_id, first_name, last_name, patronymic):
        Teacher.insert(user=telegram_id, first_name=first_name, last_name=last_name, patronymic=patronymic) \
            .execute()
