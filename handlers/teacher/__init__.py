from .start import *
from .add_group import *

def setup(dp):
    dp.register_message_handler(
        login,
        commands=['start'],
        state=None
        # TODO check if it from teacher
    )

    dp.register_callback_query_handler(
        set_new_group_name,
        text="add_new_group",
        state=states.Teacher.start
    )

    dp.register_message_handler(
        set_new_group_students,
        state=states.Teacher.add_group.name
    )

    dp.register_message_handler(
        correcting_students_list,
        content_types=['document'],
        state=states.Teacher.add_group.students
    )

    dp.register_callback_query_handler(
        end_group_add,
        text='apply',
        state=states.Teacher.add_group.students
    )