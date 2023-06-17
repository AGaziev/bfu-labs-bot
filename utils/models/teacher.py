from dataclasses import dataclass


@dataclass
class Teacher:
    """dataclass representing a teacher
    """
    firstname: str
    lastname: str
    patronymic: str
    username: str
