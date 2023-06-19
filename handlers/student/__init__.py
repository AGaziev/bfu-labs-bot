from aiogram import Dispatcher

from .start import login
from .connect_to_group import set_connecting_group_name, show_student_list_of_group, choosing_student, end_connecting_to_group
from utils import states
from loguru import logger


def setup_student_handlers(dp: Dispatcher):
    try:
        dp.register_message_handler(
            login,
            commands=['start'],
            state=None,
        )

        dp.register_callback_query_handler(
            set_connecting_group_name,
            text="connect_to_group",
            state=states.Student.start
        )

        dp.register_message_handler(
            show_student_list_of_group,
            state=states.Student.connect_to_group.group_name
        )

        dp.register_message_handler(
            choosing_student,
            state=states.Student.connect_to_group.choose_name
        )

        dp.register_callback_query_handler(
            end_connecting_to_group,
            text='apply',
            state=states.Student.connect_to_group.choose_name
        )

    except Exception as e:
        # TODO: switch base exception to more specific
        logger.error(
            f"Error while registering student handlers: {e.__class__.__name__, e}")
