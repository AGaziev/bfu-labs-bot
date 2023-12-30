from dataclasses import dataclass
from .laboratory_work import LaboratoryWork


@dataclass
class StudentsLabs:
    accepted: list[LaboratoryWork] | None = None
    not_done: list[LaboratoryWork] | None = None
