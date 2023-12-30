from datetime import datetime

from peewee import Model, DateTimeField, ForeignKeyField, CharField, BooleanField, IntegerField
from repositories import db


class BaseModel(Model):
    class Meta:
        database = db


class RegisterDateModel(BaseModel):
    created_date = DateTimeField(default=datetime.datetime.now)


class User(BaseModel):
    telegram_id = CharField(primary_key=True)
    username = CharField()
    is_blocked = BooleanField(default=False)


class Teacher(RegisterDateModel):
    first_name = CharField()
    last_name = CharField()
    patronymic = CharField()
    user = ForeignKeyField(User)


class Group(RegisterDateModel):
    teacher = ForeignKeyField(Teacher)
    name = CharField()


class GroupMember(BaseModel):
    first_name = CharField()
    last_name = CharField()
    group = ForeignKeyField(Group)
    user = ForeignKeyField(User)


class LabRegistry(BaseModel):
    group = ForeignKeyField(Group)
    name = CharField()
    number = IntegerField()
    cloud_link = CharField()


class Status(BaseModel):
    title = CharField()


class LabWork(BaseModel):
    member = ForeignKeyField(GroupMember)
    lab = ForeignKeyField(LabRegistry)
    status = ForeignKeyField(Status)
