from peewee import fn, JOIN

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
        return Teacher.get(Teacher.id == teacher_id)
    # endregion
    @staticmethod
    def select_all_members_from_group(group: Group) -> list[GroupMember]:
        return GroupMember.select().where(GroupMember.group == group.id)

    @staticmethod
    def select_type_members_for_group(group: Group, registered: bool) -> list[GroupMember]:
        query = Selector.select_all_members_from_group(group) \
            .where((GroupMember.user.is_null() != registered))
        return query

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
    def select_labs_with_status_for_group(group: Group, status: LabStatus) -> list[LabWork]:
        labs = Selector.select_labs_for_group(group)

        if status != LabStatus.ALL:
            lab_status = Selector.get_lab_status(status)
        else:
            lab_status = "*"

        query = (LabWork
                 .select()
                 .where((LabWork.lab.in_(labs)) &
                        ((LabWork.status == lab_status.id) if lab_status != "*" else True)))
        return query

    @staticmethod
    def select_labs_with_status_count_from_group(group: Group, status: LabStatus) -> int:
        lab_works = Selector.select_labs_with_status_for_group(group, status)
        query = lab_works.select(fn.COUNT("*"))
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
                 .where(Group.teacher == teacher.id))
        return query

    @staticmethod
    def select_undone_group_labs_for_student(student: GroupMember):
        user = Selector.get_user_by_telegram_id(student.user)
        group = Selector.get_group_by_id(student.group)
        labs = Selector.select_students_labs_with_status_in_group(group, user).select(LabWork.lab)
        query = LabRegistry.select().where(~(LabRegistry.id.not_in(labs)))
        return query
