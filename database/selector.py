from peewee import fn, JOIN

from _legacy.laboratory_work import LaboratoryWork
from utils import Group, GroupMember, LabRegistry, LabWork, User, Status, Teacher
from utils.enums import LabStatus


class Selector:
    # region Getters For GroupMember
    @staticmethod
    def get_group_member_by_telegram_and_group(group_id, telegram_id) -> GroupMember:
        member = GroupMember.get((GroupMember.group == group_id) &
                                 (GroupMember.user == telegram_id))
        return member

    @staticmethod
    def get_group_member_by_id(member_id) -> GroupMember:
        member = GroupMember.get_by_id(member_id)
        return member

    # endregion
    # region Getters For Group
    @staticmethod
    def get_group_by_name(name: str) -> Group:
        return Group.get_or_none(name=name)

    @staticmethod
    def get_group_by_id(group_id: str | int) -> Group:
        return Group.get_by_id(group_id)

    # endregion
    # region Getters For Status
    @staticmethod
    def get_lab_status(status: LabStatus) -> Status:
        return Status.get(Status.title == status.value)

    # endregion
    # region Getters For LabRegistry
    @staticmethod
    def get_group_lab_by_number(group: Group, lab_number) -> LabRegistry:
        query = (LabRegistry
                 .select()
                 .where((LabRegistry.lab_number == lab_number) &
                        (LabRegistry.group_id == group.id)))
        return query

    # endregion
    # region Getters For LabWork
    @staticmethod
    def get_lab_by_id(lab_id: int) -> LabWork:
        return LabWork.get_by_id(lab_id)

    # endregion
    # region Getters For User
    @staticmethod
    def get_lab_owner(lab_id: int) -> User:
        lab = LabWork.get_by_id(lab_id)
        member = Selector.get_group_member_by_id(lab.member)
        return User.get_by_id(member.user)

    @staticmethod
    def get_user_by_username(username) -> User:
        query = (User
                 .select()
                 .where(User.username == username))
        return query

    @staticmethod
    def get_user_by_telegram_id(telegram_id):
        return User.get_or_none(telegram_id)
    # endregion
    # region Getters For Teacher
    @staticmethod
    def get_teacher_by_telegram_id(telegram_id):
        return Teacher.get(Teacher.user == telegram_id)

    @staticmethod
    def get_teacher_by_group_id(group_id):
        teacher_id = Group.get_by_id(group_id).teacher
        return Teacher.get(Teacher.user == teacher_id)
    # endregion
    @staticmethod
    def select_all_members_from_group(group: Group) -> list[GroupMember]:
        return GroupMember.select() \
            .where(GroupMember.group == group.id)

    @staticmethod
    def select_type_members_for_group(group: Group, registered: bool) -> list[GroupMember]:
        return Selector.select_all_members_from_group(group.id) \
            .where((GroupMember.user is None) != registered)

    @staticmethod
    def select_user_groups_names_with_id(user: User) -> list[Group]:
        student_registers = GroupMember.select(GroupMember.group) \
            .where(GroupMember.user == user.id)

        return Group.select() \
            .where(Group.id << student_registers)

    @staticmethod
    def select_labs_for_group(group: Group) -> list[LabRegistry]:
        return LabRegistry.select() \
            .where(LabRegistry.group == group.id)

    @staticmethod
    def select_labs_with_status_count_from_group(group: Group, status: LabStatus) -> int:
        labs = Selector.select_labs_for_group(group)

        labStatus = Selector.get_lab_status(status)

        query = (LabWork
                 .select(fn.COUNT)
                 .where((LabWork.lab.in_(labs)) &
                        (LabWork.status == labStatus.id)))
        return query.scalar()

    @staticmethod
    def select_lab_stats_by_whole_group(group: Group) -> list[GroupMember | LabWork | LabRegistry]:
        query = (GroupMember
                 .select(
            GroupMember.name.alias('name'),
            LabRegistry.number.alias('number'),
            fn.COALESCE(GroupMember.user, "").alias('is_registered'),
            LabWork.created_date.alias('date'),
            LabWork.status.alias('status')
        )
                 .join(LabWork, JOIN.FULL, on=(GroupMember.id == LabWork.member))
                 .join(LabRegistry, on=(LabWork.lab == LabRegistry.id))
                 .where(GroupMember.group == group.id)
                 )
        return query

    @staticmethod
    def select_all_labs_count_from_group(group_id):
        query = LabRegistry \
            .select(fn.COUNT(LabRegistry.id)) \
            .where(LabRegistry.group == group_id)

        return query.scalar()

    # @staticmethod
    # def select_first_unchecked_lab_in_group(group_id):
    #     subquery = (Status
    #                 .select(Status.id)
    #                 .where(Status.status_name == 'Не проверено')
    #                 .limit(1))
    #
    #     query = (LabWork
    #              .select(LabWork.id,
    #                      LabRegistry.lab_number,
    #                      LabRegistry.lab_description,
    #                      LabRegistry.cloud_link,
    #                      GroupMember.credentials)
    #              .join(LabRegistry, JOIN.LEFT_OUTER, on=(LabWork.lab_id == LabRegistry.id))
    #              .switch(LabWork)
    #              .join(GroupMember, JOIN.LEFT_OUTER,
    #                    on=(LabWork.member_id == GroupMember.member_id))
    #              .where((GroupMember.group_id == group_id) &
    #                     (LabWork.status_id.in_(subquery)))
    #              .order_by(LabWork.id.asc())
    #              .limit(1))
    #     return query

    # @staticmethod
    # def select_next_unchecked_lab_in_group(group_id, current_lab_id):
    #     subquery = Selector.get_lab_status(LabStatus.NOTCHECKED)
    #
    #     query = (LabWork
    #              .select(LabWork.id,
    #                      LabRegistry.lab_number,
    #                      LabRegistry.lab_description,
    #                      LabRegistry.cloud_link,
    #                      GroupMember.credentials)
    #              .join(LabRegistry, JOIN.LEFT_OUTER, on=(LabWork.lab_id == LabRegistry.id))
    #              .switch(LabWork)
    #              .join(GroupMember, JOIN.LEFT_OUTER,
    #                    on=(LabWork.member_id == GroupMember.member_id))
    #              .where((GroupMember.group_id == group_id) &
    #                     (LabWork.status_id.in_(subquery)) &
    #                     (LabWork.id > current_lab_id))
    #              .order_by(LabWork.id.asc())
    #              .limit(1))
    #     return query
    #
    # @staticmethod
    # def select_previous_unchecked_lab_in_group(group_id, current_lab_id):
    #     subquery = (LabStatus
    #                 .select(LabStatus.id)
    #                 .where(LabStatus.status_name == 'Не проверено')
    #                 .limit(1))
    #
    #     return (LabWork
    #             .select(LabWork.id,
    #                     LabRegistry.lab_number,
    #                     LabRegistry.lab_description,
    #                     LabRegistry.cloud_link,
    #                     GroupMember.credentials)
    #             .join(LabRegistry, JOIN.LEFT_OUTER, on=(LabWork.lab_id == LabRegistry.id))
    #             .switch(LabWork)
    #             .join(GroupMember, JOIN.LEFT_OUTER,
    #                   on=(LabWork.member_id == GroupMember.member_id))
    #             .where((GroupMember.group_id == group_id) &
    #                    (LabWork.status_id.in_(subquery)) &
    #                    (LabWork.id < current_lab_id))
    #             .order_by(LabWork.id.asc())
    #             .limit(1))

    @staticmethod
    def select_students_labs_with_status_in_group(group: Group, user: User, status_filter=LabStatus.ALL) -> list[LabRegistry]:
        member = Selector.get_group_member_by_telegram_and_group(group.id, user.telegram_id)

        query = (LabRegistry
                 .select(LabRegistry.id,
                         LabRegistry.name,
                         LabRegistry.cloud_link,
                         fn.COALESCE(Status.title, LabStatus.NOTHANDOVER).alias('status'))
                 .join(LabWork, JOIN.LEFT_OUTER, on=(LabRegistry.id == LabWork.lab_id))
                 .join(Status, JOIN.LEFT_OUTER, on=(LabWork.status_id == Status.id))
                 .where(LabRegistry.group_id == group.id,
                        LabWork.member_id == member.id))
        if status_filter != LabStatus.ALL:
            query = query.where(query.status == status_filter)
        return query

    @staticmethod
    def is_user_exist(telegram_id):
        return bool(Selector.get_user_by_telegram_id(telegram_id))

    @staticmethod
    def select_teacher_groups(teacher: Teacher):
        query = (Group
                 .select(Group.id, Group.name)
                 .where(Group.teacher == Teacher.id))
        return query

    # @staticmethod
    # def ff(user_id):
    #     query = (Teacher
    #              .select(fn.EXISTS(
    #         Teacher.select(fn.COUNT(1))
    #         .where(Teacher.telegram_id == user_id)
    #     ).alias('exists')))
    #
    #     # Для выполнения запроса и получения результата
    #     return query.scalar()  # Возвращает True, если запись существует, иначе False
