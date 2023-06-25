from aiogram import Dispatcher
from loguru import logger

from .admin_utils import cmd_info, show_admin_commands
from .invite_teacher import invite_user_to_register_as_teacher
from .mimicry import mimic_a_student, mimic_a_teacher


def setup_admin_handlers(dp: Dispatcher):

    dp.register_message_handler(
        cmd_info,
        commands=['info'],
        state=None
    )

    dp.register_message_handler(
        show_admin_commands,
        commands=['admin'],
        state=None
    )

    dp.register_callback_query_handler(
        show_admin_commands,
        lambda call: call.data == 'admin_commands',
        state=None
    )

    dp.register_message_handler(
        invite_user_to_register_as_teacher,
        commands=['invite_teacher'],
        state=None
    )

    dp.register_callback_query_handler(
        mimic_a_student,
        lambda call: call.data == 'admin_mimic_a_student',
    )

    dp.register_callback_query_handler(
        mimic_a_teacher,
        lambda call: call.data == 'admin_mimic_a_teacher',
    )

    logger.info('Admin handlers are successfully registered')
