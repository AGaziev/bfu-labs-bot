"""Finite state machine states module
    """

from aiogram.dispatcher.filters.state import State, StatesGroup


class registrator(StatesGroup):
    name = State()


class AddGroup(StatesGroup):
    name = State()
    students = State()


class TeacherState(StatesGroup):
    start = State()
    add_group = AddGroup()
    add_new_lab = State()


class ConnectGroup(StatesGroup):
    group_name = State()
    choose_name = State()


class Student(StatesGroup):
    start = State()
    connect_to_group = ConnectGroup()
    show_groups = State()
