from aiogram.types import ContentType
from aiogram import Dispatcher

from loguru import logger

from utils import states, callbacks
from .add_group import set_new_group_name, set_new_group_students, correcting_students_list, change_stundents_list_to_new_file, end_group_add, send_file_sample
from .cancel_operation import cancel_operation
from .register import register_as_teacher, confirm_teacher_credentials, confirm_credentials_and_write_to_database, change_teacher_credentials
from .show_my_groups import show_my_groups
from .group_menu import teacher_group_menu, send_stats_of_group
from .add_new_lab import wait_for_lab_conditions_file, ask_for_filename_to_change, wait_for_new_filename, upload_file_to_cloud_drive, change_filename
from .check_students_labs import navigate_labs, show_not_checked_labs, accept_laboratory_work, reject_laboratory_work


def setup_teacher_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        cancel_operation,
        lambda call: call.data == 'cancel',
        state='*'
    )

    dp.register_callback_query_handler(
        set_new_group_name,
        text="create_new_group",
        state=states.TeacherState.start
    )

    dp.register_message_handler(
        set_new_group_students,
        state=states.TeacherState.add_group.name
    )

    dp.register_callback_query_handler(
        send_file_sample,
        lambda call: call.data.startswith('sample'),
        state=states.TeacherState.add_group.students
    )

    dp.register_message_handler(
        correcting_students_list,
        content_types=ContentType.DOCUMENT,
        state=states.TeacherState.add_group.students
    )

    dp.register_callback_query_handler(
        end_group_add,
        lambda call: call.data == 'yes',
        state=states.TeacherState.add_group.confirm
    )

    dp.register_callback_query_handler(
        change_stundents_list_to_new_file,
        lambda call: call.data == 'no',
        state=states.TeacherState.add_group.confirm
    )

    dp.register_callback_query_handler(
        show_my_groups,
        lambda call: call.data == 'teacher_show_my_groups',
        state=states.TeacherState.start
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

    dp.register_callback_query_handler(
        show_my_groups,
        lambda call: call.data == 'teacher_show_my_groups',
        state=states.TeacherState.start
    )

    dp.register_callback_query_handler(
        teacher_group_menu,
        lambda call: call.data.startswith('group:'),
        state=states.TeacherState.show_my_groups
    )

    dp.register_callback_query_handler(
        wait_for_lab_conditions_file,
        lambda call: call.data.startswith('add_lab'),
        state=states.TeacherState.group_menu
    )

    dp.register_message_handler(
        ask_for_filename_to_change,
        content_types=ContentType.DOCUMENT,
        state=states.TeacherState.add_lab.upload_lab_file
    )

    dp.register_callback_query_handler(
        wait_for_new_filename,
        lambda call: call.data == 'no',
        state=states.TeacherState.add_lab.ask_for_filename_to_change
    )

    dp.register_message_handler(
        change_filename,
        content_types=ContentType.TEXT,
        state=states.TeacherState.add_lab.wait_for_new_filename
    )

    dp.register_callback_query_handler(
        upload_file_to_cloud_drive,
        lambda call: call.data == 'changed_mind',
        state=states.TeacherState.add_lab.wait_for_new_filename
    )

    dp.register_callback_query_handler(
        upload_file_to_cloud_drive,
        lambda call: call.data == 'yes',
        state=states.TeacherState.add_lab.ask_for_filename_to_change
    )

    dp.register_callback_query_handler(
        send_stats_of_group,
        callbacks.stats_callback.filter(user_role="teacher"),
        state=states.TeacherState.group_menu
    )

    dp.register_callback_query_handler(
        show_not_checked_labs,
        callbacks.show_callback.filter(user_role="teacher", data_type="labs"),
        state=states.TeacherState.group_menu
    )

    dp.register_callback_query_handler(
        show_previous_not_checked_lab,
        callbacks.check_lab_callback.filter(status="previous"),
        state=states.TeacherState.check_students_labs
    )

    dp.register_callback_query_handler(
        show_next_not_checked_lab,
        callbacks.check_lab_callback.filter(status="next"),
        state=states.TeacherState.check_students_labs
    )

    dp.register_callback_query_handler(
        accept_laboratory_work,
        callbacks.check_lab_callback.filter(status="accepted"),
        state=states.TeacherState.check_students_labs
    )

    dp.register_callback_query_handler(
        reject_laboratory_work,
        callbacks.check_lab_callback.filter(status="rejected"),
        state=states.TeacherState.check_students_labs
    )

    logger.info('Teacher handlers are successfully registered')
