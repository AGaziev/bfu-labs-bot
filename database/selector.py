from peewee import fn, JOIN, ModelSelect

from _legacy.laboratory_work import LaboratoryWork
from handlers.error import error_handling
from utils import Group, GroupMember, LabRegistry, LabWork, User, Status, Teacher
from utils.enums import LabStatus


class Selector:

    @staticmethod
    def get_group_member_by_telegram_and_group(group_id, telegram_id) -> GroupMember:
        member_subquery = GroupMember.get((GroupMember.group == group_id) &
                                          (GroupMember.user == telegram_id))
        return member_subquery

    @staticmethod
    def get_group_by_name(name: str) -> Group:
        return Group.get_or_none(name=name)

    @staticmethod
    def get_group_by_id(group_id: str | int) -> Group:
        return Group.get_by_id(group_id)

    @staticmethod
    def get_unregistered_members_for_group(group_name: str) -> list[GroupMember]:
        group = Selector.get_group_by_name(group_name)
        return GroupMember.select().where((GroupMember.group == group.id) & (GroupMember.user == None))

    @staticmethod
    def select_student_groups_names_with_id(telegram_id) -> list[Group]:
        student_registers = GroupMember.select(GroupMember.group).where(GroupMember.user == telegram_id)
        return Group.select().where(Group.id << student_registers)

    @staticmethod
    def select_registered_members_from_group(group_id) -> list[GroupMember]:
        return GroupMember.select().where((GroupMember.group == group_id) & (GroupMember.user != None)).objects()

    @staticmethod
    def get_labs_for_group(group_id) -> list[LabRegistry]:
        return LabRegistry.select().where(LabRegistry.group == group_id)

    @staticmethod
    def select_labs_with_status_count_from_group(group_id, status: LabStatus):
        subquery_member_ids = (GroupMember
                               .select(GroupMember.id)
                               .where(GroupMember.group == group_id))

        subquery_status_id = (Status
                              .select(Status.id)
                              .where(Status.title == status.value)
                              .limit(1))
        # Используем limit(1) для получения одного id, так как предполагается,
        # что status_name уникален

        query = (LabWork
                 .select(LabWork.id)
                 .where((LabWork.member.in_(subquery_member_ids)) &
                        (LabWork.status == subquery_status_id))).tuples()
        return len(query)

    @staticmethod
    def select_lab_stats_by_whole_group(group_id):
        query = (GroupMember
                 .select(
            GroupMember.credentials.alias('name'),
            fn.COALESCE(User.telegram_id, 0).alias('is_registered'),
            LabRegistry.number.alias('number'),
            LabRegistry.created_date.alias('date'),
            LabRegistry.status.alias('status')
        )
                 .join(User, JOIN.LEFT_OUTER,
                       on=(GroupMember.member_id == GroupMember.member_id))
                 .join(LabRegistry, JOIN.FULL, on=(User.member_id == LabWork.member_id))
                 .join(LabRegistry, JOIN.LEFT_OUTER, on=(LabWork.lab == LabRegistry.id))
                 .where(GroupMember.group == group_id)
                 )
        return query

    @staticmethod
    def select_all_labs_count_from_group(group_id):
        query = (LabRegistry
                 .select(fn.COUNT(LabRegistry.id))
                 .where(LabRegistry.member_id << (
            GroupMember.select(GroupMember.member_id).where(GroupMember.group == group_id)
        )))

        return query.scalar()

    @staticmethod
    def select_first_unchecked_lab_in_group(group_id):
        subquery = (Status
                    .select(LabStatus.id)
                    .where(LabStatus.status_name == 'Не проверено')
                    .limit(1))

        query = (LabWork
                 .select(LabWork.id,
                         LabRegistry.lab_number,
                         LabRegistry.lab_description,
                         LabRegistry.cloud_link,
                         GroupMember.credentials)
                 .join(LabRegistry, JOIN.LEFT_OUTER, on=(LabWork.lab_id == LabRegistry.id))
                 .switch(LabWork)
                 .join(GroupMember, JOIN.LEFT_OUTER,
                       on=(LabWork.member_id == GroupMember.member_id))
                 .where((GroupMember.group_id == group_id) &
                        (LabWork.status_id.in_(subquery)))
                 .order_by(LabWork.id.asc())
                 .limit(1))
        return query

    @staticmethod
    def select_next_unchecked_lab_in_group(group_id, current_lab_id):
        subquery = (LabStatus
                    .select(LabStatus.id)
                    .where(LabStatus.status_name == 'Не проверено')
                    .limit(1))

        query = (LabWork
                 .select(LabWork.id,
                         LabRegistry.lab_number,
                         LabRegistry.lab_description,
                         LabRegistry.cloud_link,
                         GroupMember.credentials)
                 .join(LabRegistry, JOIN.LEFT_OUTER, on=(LabWork.lab_id == LabRegistry.id))
                 .switch(LabWork)
                 .join(GroupMember, JOIN.LEFT_OUTER,
                       on=(LabWork.member_id == GroupMember.member_id))
                 .where((GroupMember.group_id == group_id) &
                        (LabWork.status_id.in_(subquery)) &
                        (LabWork.id > current_lab_id))
                 .order_by(LabWork.id.asc())
                 .limit(1))
        return query

    @staticmethod
    def select_previous_unchecked_lab_in_group(group_id, current_lab_id):
        subquery = (LabStatus
                    .select(LabStatus.id)
                    .where(LabStatus.status_name == 'Не проверено')
                    .limit(1))

        return (LabWork
                .select(LabWork.id,
                        LabRegistry.lab_number,
                        LabRegistry.lab_description,
                        LabRegistry.cloud_link,
                        GroupMember.credentials)
                .join(LabRegistry, JOIN.LEFT_OUTER, on=(LabWork.lab_id == LabRegistry.id))
                .switch(LabWork)
                .join(GroupMember, JOIN.LEFT_OUTER,
                      on=(LabWork.member_id == GroupMember.member_id))
                .where((GroupMember.group_id == group_id) &
                       (LabWork.status_id.in_(subquery)) &
                       (LabWork.id < current_lab_id))
                .order_by(LabWork.id.asc())
                .limit(1))

    @staticmethod
    def select_student_credentials(telegram_id, group_name):
        subquery_group_id = (Group
                             .select(Group.id)
                             .where(Group.group_name == group_name)
                             .limit(1))

        subquery_member_id = (User
                              .select(User.member_id)
                              .where(User.telegram_id == telegram_id))

        query = (GroupMember
                 .select(GroupMember.credentials)
                 .where((GroupMember.group_id.in_(subquery_group_id)) &
                        (GroupMember.member_id.in_(subquery_member_id))))
        return query

    @staticmethod
    def select_lab_name_and_id_by_number(group_name, lab_number):
        subquery_group_id = (Group
                             .select(Group.id)
                             .where(Group.group_name == group_name)
                             .limit(1))

        query = (LabRegistry
                 .select(LabRegistry.lab_description, LabRegistry.id)
                 .where((LabRegistry.lab_number == lab_number) &
                        (LabRegistry.group_id.in_(subquery_group_id))))
        return query

    @staticmethod
    def select_students_labs_with_status_in_group(group_id, telegram_id):
        member = Selector.get_group_member_by_telegram_and_group(group_id, telegram_id)

        query = (LabRegistry
                 .select(LabRegistry.id.alias('id'),
                         LabRegistry.name.alias('descr'),
                         LabRegistry.cloud_link.alias('path'),
                         fn.COALESCE(Status.title, 'Не сдано').alias('status'))
                 .join(LabWork, JOIN.LEFT_OUTER, on=(LabRegistry.id == LabWork.lab_id))
                 .join(Status, JOIN.LEFT_OUTER, on=(LabWork.status_id == Status.id))
                 .where(LabRegistry.group_id == group_id,
                        LabWork.member_id == member.id))
        return query

    @staticmethod
    def select_undone_group_labs_for_student(group_id, telegram_id):
        member = Selector.get_group_member_by_telegram_and_group(group_id, telegram_id)

        subquery_lab_id = (LabWork
                           .select(LabWork.lab_id)
                           .where((LabWork.member_id == member.id)))

        query = (LabRegistry
                 .select()
                 .where((LabRegistry.group_id == group_id) &
                        ~(LabRegistry.id.in_(subquery_lab_id))))
        return query

    @staticmethod
    def select_lab_and_owner_telegram_id_by_lab_id(lab_id):
        query = (LabRegistry
                 .select(LabRegistry.id.alias('lab_id'),
                         LabRegistry.lab_number,
                         LabRegistry.lab_description,
                         LabWork.cloud_link,
                         GroupMember.credentials,
                         User.telegram_id)
                 .join(LabWork, JOIN.LEFT_OUTER, on=(LabRegistry.id == LabWork.lab_id))
                 .join(GroupMember, JOIN.LEFT_OUTER, on=(LabWork.member_id == GroupMember.member_id))
                 .join(User, JOIN.LEFT_OUTER, on=(GroupMember.member_id == User.member_id))
                 .where(LabRegistry.id == lab_id)).dicts()
        lab = LaboratoryWork()
        lab.number = query['lab_number']
        lab.description = query['lab_description']
        lab.cloud_link = query['cloud_link']
        lab.member_credentials = query['credentials']
        return lab, query['telegram_id']

    @staticmethod
    def select_telegram_id_by_username(username):
        query = (User
                 .select(User.telegram_id)
                 .where(User.username == username))
        return query

    @staticmethod
    def check_is_user_exist(user_id):
        query = (User
                 .select(fn.EXISTS(
            User.select(fn.COUNT(1))
            .where(User.telegram_id == user_id)
        ).alias('exists')))
        return query

    @staticmethod
    def select_teacher_credentials_by_telegram_id(telegram_id):
        query = (Teacher
                 .select()
                 .where(Teacher.user_id == telegram_id).get())
        return query

    @staticmethod
    def select_teacher_credentials_by_group_id(group_id):
        teacher_id = Group.select(Group.teacher).where(Group.id == group_id)

        query = Teacher.get_by_id(teacher_id)
        return query

    @staticmethod
    def select_group_ids_and_names_owned_by_telegram_id(telegram_id):
        query = (Group
                 .select(Group.id, Group.name)
                 .where(Group.teacher ==
                        (Teacher.select().where(Teacher.user == telegram_id))))
        return query

    @staticmethod
    def ff(user_id):
        query = (Teacher
                 .select(fn.EXISTS(
            Teacher.select(fn.COUNT(1))
            .where(Teacher.telegram_id == user_id)
        ).alias('exists')))

        # Для выполнения запроса и получения результата
        return query.scalar()  # Возвращает True, если запись существует, иначе False
