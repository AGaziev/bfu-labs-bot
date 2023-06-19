from .user import *
from .admin import *
from .teacher import setup as setup_teacher
from .student import setup as setup_student

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

    setup_teacher(dp)
    setup_student(dp)

