from dataclasses import dataclass


@dataclass
class GroupInfo:
    registered_members_count: int | None = None
    unregister_members_count: int | None = None
    students_at_all: int | None = None
    lab_condition_files_count: int | None = None
    passed_labs_count: int | None = None
    rejected_labs_count: int | None = None
    not_checked_labs_count: int | None = None
    labs_at_all: int | None = None
