"""Finite state machine states module
    """

from aiogram.dispatcher.filters.state import State, StatesGroup


class registrator(StatesGroup):
    name = State()


class AddGroup(StatesGroup):
    name = State()
    students = State()


class Teacher(StatesGroup):
    start = State()
    add_group = AddGroup()
    show_groups = State()
