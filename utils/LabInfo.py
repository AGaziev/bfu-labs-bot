from dataclasses import dataclass

from utils import GroupMember, LabWork, LabRegistry


@dataclass
class LabInfo:
    owner: GroupMember
    lab_work: LabWork
    lab: LabRegistry
