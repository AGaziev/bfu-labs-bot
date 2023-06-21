from aiogram import Dispatcher

from .user import cmd_start
from .admin import cmd_info, show_admin_commands, invite_user_to_register_as_teacher
from .teacher import setup_teacher_handlers
from .student import setup_student_handlers
# DON'T TOUCH THIS IMPORT
from utils import states

from loguru import logger


def setup(dp: Dispatcher):
    """setup handlers for users and moders in one place and add throttling in 5 seconds

    Args:
        dp (Dispatcher): Dispatcher object
    """

    setup_teacher_handlers(dp)
    setup_student_handlers(dp)

    """user handlers"""
    dp.register_message_handler(
        cmd_start,
        commands=['start', 'menu'],
        state='*')

    """admin handlers"""
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
