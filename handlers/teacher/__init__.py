from aiogram.types import ContentType
from loguru import logger
from aiogram import Dispatcher
from .add_group import set_new_group_name, set_new_group_students, correcting_students_list, end_group_add
from .cancel_operation import cancel_operation
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
        text='apply',
        state=states.TeacherState.add_group.students
    )
