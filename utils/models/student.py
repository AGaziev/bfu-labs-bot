from dataclasses import dataclass


@dataclass
class Student:
    """
    dataclass representing a student
        fields:
                firstname: str
                lastname: str
                username: str | None
    """
    firstname: str = ''
    lastname: str = ''
    username: str | None = None
