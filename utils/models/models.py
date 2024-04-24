from datetime import datetime

from peewee import Model, DateTimeField, ForeignKeyField, CharField, BooleanField, IntegerField, AutoField
from repositories import db


class BaseModel(Model):
    class Meta:
        database = db


class RegisterDateModel(BaseModel):
    created_date = DateTimeField(default=datetime.now)


class User(BaseModel):
    telegram_id = CharField(primary_key=True, unique=True)
    username = CharField()
    is_blocked = BooleanField(default=False)

    class Meta:
        db_table = 'User'


class Teacher(RegisterDateModel):
    first_name = CharField()
    last_name = CharField()
    patronymic = CharField()
    user = ForeignKeyField(User, on_delete='CASCADE')

    class Meta:
        db_table = 'Teacher'


class Group(RegisterDateModel):
    teacher = ForeignKeyField(Teacher, on_delete='SET NULL', null=True)
    name = CharField()

    class Meta:
        db_table = 'Group'


class GroupMember(BaseModel):
    name = CharField()
    group = ForeignKeyField(Group, on_delete='CASCADE')
    user = ForeignKeyField(User, on_delete='SET NULL', null=True)

    class Meta:
        db_table = 'GroupMember'


class LabRegistry(RegisterDateModel):
    group = ForeignKeyField(Group, on_delete='CASCADE')
    name = CharField()
    number = IntegerField()
    cloud_link = CharField()
    deadline = IntegerField(null=True)

    class Meta:
        db_table = 'LabRegistry'


class Status(BaseModel):
    title = CharField()

    class Meta:
        db_table = 'Status'


class LabWork(BaseModel):
    member = ForeignKeyField(GroupMember, on_delete='NO ACTION')
    lab = ForeignKeyField(LabRegistry, on_delete='NO ACTION')
    status = ForeignKeyField(Status, on_delete='NO ACTION')

    class Meta:
        db_table = 'LabWork'
