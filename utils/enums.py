import enum


class Blocked(enum.Enum):
    FALSE = 'FALSE'
    TRUE = 'TRUE'
    ANY = 'TRUE, FALSE'


class LabStatus(enum.Enum):
    HandOver = "Сдано"
    Rejected = "Отклонено"
    NotChecked = "Не проверено"
    All = "*"

