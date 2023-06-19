from dataclasses import dataclass


@dataclass
class Teacher:
    """
    dataclass representing a teacher
        fields:
                firstname: str
                lastname: str
                patronymic: str
                username: str
    """
    firstname: str
    lastname: str
    patronymic: str
    username: str
