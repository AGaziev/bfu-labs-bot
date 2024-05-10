from aiogram import Dispatcher

from .user import cmd_start
from .admin import setup_admin_handlers
from .teacher import setup_teacher_handlers
from .student import setup_student_handlers
from .error import error_handler
# DON'T TOUCH THIS IMPORT
from utils import states


def setup(dp: Dispatcher):
    """setup handlers for users and moders in one place and add throttling in 5 seconds

    Args:
        dp (Dispatcher): Dispatcher object
    """
    setup_admin_handlers(dp)
    setup_teacher_handlers(dp)
    setup_student_handlers(dp)

    """user handlers"""
    dp.register_message_handler(
        cmd_start,
        commands=['start', 'menu'],
        state='*')

    """admin handlers"""
    dp.register_errors_handler(
        error_handler
    )