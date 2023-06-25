"""Finite state machine states module
    """

from aiogram.dispatcher.filters.state import State, StatesGroup


class Registration(StatesGroup):
    input_credentials = State()
    confirmation = State()


class AddGroup(StatesGroup):
    name = State()
    students = State()
    confirm = State()


class AddLab(StatesGroup):
    upload_lab_file = State()
    ask_for_filename_to_change = State()
    wait_for_new_filename = State()


class TeacherState(StatesGroup):
    registration = Registration()
    start = State()
    add_group = AddGroup()
    show_my_groups = State()
    group_menu = State()
    add_lab = AddLab()


class ConnectGroup(StatesGroup):
    group_name = State()
    choose_name = State()


class PostLab(StatesGroup):
    choose_lab = State()
    upload_lab_file = State()
    ask_for_filename_to_change = State()
    wait_for_new_filename = State()

class Student(StatesGroup):
    start = State()
    connect_to_group = ConnectGroup()
    show_groups = State()
    group_menu = State()
    post_lab = PostLab()
