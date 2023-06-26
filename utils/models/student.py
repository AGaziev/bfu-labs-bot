from dataclasses import dataclass


@dataclass
class Student:
    firstname: str = ''
    lastname: str = ''
    username: str | None = None
