from dataclasses import dataclass


@dataclass
class Teacher:
    firstname: str = ''
    lastname: str = ''
    patronymic: str = ''
    username: str | None = None
