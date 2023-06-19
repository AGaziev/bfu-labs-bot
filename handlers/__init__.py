from .user import *
from .admin import *
from .teacher import setup_teacher_handlers
from .student import setup_student_handlers
# DON'T TOUCH THIS IMPORT
from loader import dispatcher
from utils import states

from loguru import logger


def setup(dp=dispatcher):
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

    """admin handlers"""
    try:
        dp.register_message_handler(
            cmd_info,
            commands=['info'],
            state=None)

        dp.register_message_handler(
            show_admin_commands,
            commands=['admin'],
            state=None)

        dp.register_message_handler(
            invite_user_to_register_as_teacher,
            commands=['invite_teacher'],
            state=None)

    except Exception as e:
        # TODO: switch base exception to more specific
        logger.error(
            f"Error while registering admin handlers: {e.__class__.__name__, e}")

    else:
        logger.debug("Handlers registered successfully")

    setup_teacher_handlers(dp)
    setup_student_handlers(dp)
