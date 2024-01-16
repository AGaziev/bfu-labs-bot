from handlers.error import error_handling
from utils import Group, GroupMember, LabRegistry


class Selector:
    @staticmethod
    def get_group_by_name(name: str) -> Group:
        return Group.get(name=name)
    @staticmethod
    def get_group_by_id(group_id: str|int) -> Group:
        return Group.get_by_id(group_id)

    @staticmethod
    def get_unregistered_members_for_group(group_name: str) -> list[GroupMember]:
        group = Selector.get_group_by_name(group_name)
        return GroupMember.select().where((GroupMember.group == group.get_id()) & (GroupMember.user == None))

    @staticmethod
    def select_student_groups_names_with_id(telegram_id) -> list[Group]:
        student_registers = GroupMember.select(GroupMember.group).where(GroupMember.user == telegram_id)
        return Group.select().where(Group << student_registers)

    @staticmethod
    def select_registered_members_from_group(group_id) -> list[GroupMember]:
        return GroupMember.select(GroupMember.id).where((GroupMember.group == group_id) & (GroupMember.user != None))

    @staticmethod
    def get_labs_for_group(group_id) -> list[LabRegistry]:
        return LabRegistry.select().where(LabRegistry.group == group_id)
