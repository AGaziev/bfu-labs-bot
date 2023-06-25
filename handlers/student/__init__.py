from aiogram import Dispatcher
from loguru import logger

from .connect_to_group import set_connecting_group_name, show_student_list_of_group, choosing_student, end_connecting_to_group
from .show_my_groups import show_my_groups
from .group_menu import student_group_menu, show_not_done_labs_files
from utils import states
from utils import callbacks


def setup_student_handlers(dp: Dispatcher):

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
        text='confirm',
        state=states.Student.connect_to_group.choose_name
    )

    dp.register_callback_query_handler(
        show_my_groups,
        callbacks.show_callback.filter(data_type="group", user_role="student"),
        state=states.Student.start
    )

    dp.register_callback_query_handler(
        student_group_menu,
        callbacks.group_callback.filter(role="student"),
        state=states.Student.show_groups
    )

    dp.register_callback_query_handler(
        show_not_done_labs_files,
        callbacks.show_callback.filter(data_type="lab", user_role="student"),
        state=states.Student.group_menu
    )
    logger.info('Student handlers are successfully registered')
