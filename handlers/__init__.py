from .user import *
from .admin import *
from .teacher import *

# DON'T TOUCH THIS IMPORT
from loader import dispatcher
from utils import states


def setup(dp:dispatcher):
    """setup handlers for users and moders in one place and add throttling in 5 seconds

    Args:
        dp (Dispatcher): Dispatcher object
    """

    """user handlers"""
    # dp.register_message_handler(
    #     cmd_start,
    #     commands=['start'],
    #     state=None)
    #
    # dp.register_message_handler(
    #     cmd_register_found_user,
    #     state=[states.registrator.name])

    """moder handlers"""
    # dp.register_message_handler(
    #     cmd_info,
    #     commands=["info"],
    #     state=None)

    """teacher handlers"""
    dp.register_message_handler(
        teacher.login,
        commands=['start'],
        state=None
    )

    dp.register_callback_query_handler(
        teacher.set_new_group_name,
        text="add_new_group",
        state=states.Teacher.start
    )

    dp.register_message_handler(
        teacher.set_new_group_students,
        state=states.Teacher.add_group.name
    )

    dp.register_message_handler(
        teacher.correcting_students_list,
        content_types=['document'],
        state=states.Teacher.add_group.students
    )

    dp.register_callback_query_handler(
        teacher.end_group_add,
        state=states.Teacher.add_group.students
    )

