from aiogram.types import ContentType
from loguru import logger
from aiogram import Dispatcher
from .add_group import set_new_group_name, set_new_group_students, correcting_students_list, end_group_add
from .cancel_operation import cancel_operation
from .register import register_as_teacher, confirm_teacher_credentials, confirm_credentials_and_write_to_database, change_teacher_credentials
from utils import states


def setup_teacher_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        cancel_operation,
        lambda call: call.data == 'cancel',
        state='*'
    )

    dp.register_callback_query_handler(
        set_new_group_name,
        text="add_new_group",
        state=states.TeacherState.start
    )

    dp.register_message_handler(
        set_new_group_students,
        state=states.TeacherState.add_group.name
    )

    dp.register_message_handler(
        correcting_students_list,
        content_types=ContentType.DOCUMENT,
        state=states.TeacherState.add_group.students
    )

    dp.register_callback_query_handler(
        end_group_add,
        text='confirm',
        state=states.TeacherState.add_group.students
    )

    dp.register_callback_query_handler(
        register_as_teacher,
        lambda call: call.data == 'register_as_teacher',
        state='*'
    )

    dp.register_callback_query_handler(
        change_teacher_credentials,
        lambda call: call.data == 'change_teacher_credentials',
        state='*'
    )

    dp.register_message_handler(
        confirm_teacher_credentials,
        content_types=ContentType.TEXT,
        state=states.TeacherState.registration.input_credentials
    )

    dp.register_callback_query_handler(
        confirm_credentials_and_write_to_database,
        lambda call: call.data == 'confirm',
        state=states.TeacherState.registration.confirmation
    )
