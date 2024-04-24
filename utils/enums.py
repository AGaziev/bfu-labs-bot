import enum


class Blocked(enum.Enum):
    FALSE = 'FALSE'
    TRUE = 'TRUE'
    ANY = 'TRUE, FALSE'


class LabStatus(enum.Enum):
    HANDOVER = "Сдано"
    REJECTED = "Отклонено"
    NOTCHECKED = "Не проверено"
    NOTHANDOVER = "Не сдано"
    ALL = "*"

