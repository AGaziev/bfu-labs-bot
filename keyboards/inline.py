from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from managers.db import DatabaseManager
from utils import Group
from utils.callbacks import group_callback, show_callback, add_lab_callback, check_lab_callback, stats_callback


async def menu_kb() -> InlineKeyboardMarkup:
    """returns inline keyboard with menu items"""
    kb = InlineKeyboardMarkup(row_width=2, )
    buttons = [
        InlineKeyboardButton(
            text='Search',
            callback_data='search'),

        InlineKeyboardButton(
            text='Sample',
            callback_data='sample'),
        InlineKeyboardButton(
            text='Home',
            callback_data='home'),
    ]
    for button in buttons:
        kb.insert(button)

    kb.add(InlineKeyboardButton(
        text='Help',
        callback_data='help'), )

    kb.add(InlineKeyboardButton(
        text='❌Close❌', callback_data='close_menu'))

    return kb


async def cancel_kb() -> InlineKeyboardMarkup:
    """returns inline keyboard with menu items"""
    kb = InlineKeyboardMarkup(row_width=1, )
    kb.insert(InlineKeyboardButton(
        text='❌Отмена',
        callback_data='cancel'),)

    return kb


async def teacher_menu_kb(show_all_groups_button: bool = True) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1, )
    group_buttons = [
        InlineKeyboardButton(
            text='➕Создать новую группу',
            callback_data='create_new_group'),
    ]
    if show_all_groups_button:
        group_buttons.append(InlineKeyboardButton(
            text='📃Посмотреть все группы',
            callback_data='teacher_show_my_groups'))

    for button in group_buttons:
        kb.insert(button)

    return kb


async def student_menu_kb(telegram_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2, )
    user = DatabaseManager.get_user_by_telegram_id(telegram_id)
    if DatabaseManager.select_user_groups_names_with_id(user):
        kb.insert(InlineKeyboardButton(
            text='👥Мои группы',
            callback_data=show_callback.new(data_type="group", user_role="student")), )

    kb.insert(InlineKeyboardButton(
        text='➕Подключиться к новой группе',
        callback_data='connect_to_group'), )

    return kb


async def confirmation_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()

    kb.insert(InlineKeyboardButton(
        text='✅Подтвердить',
        callback_data='confirm'))

    return kb


def teacher_group_menu_kb(group_id) -> InlineKeyboardMarkup:
    """
    group_id - group's id from database to build a callback
    """
    kb = InlineKeyboardMarkup(row_width=1,)
    group_buttons = [
        InlineKeyboardButton(
            text='➕Добавить лабораторную работу',
            callback_data=add_lab_callback.new(
                group_id=group_id, user_role="teacher")
        ),
        InlineKeyboardButton(
            text='📚Проверить лабораторные',
            callback_data=show_callback.new(
                data_type="labs", user_role="teacher")
        ),
        InlineKeyboardButton(
            text='📊Статистика по лабораторным',
            callback_data=stats_callback.new(
                group_id=group_id, user_role="teacher"
            )
        ),
        InlineKeyboardButton(
            text='📃Переименовать группу(IN PROGRESS)',
            callback_data='rename_group'
        )
    ]

    for button in group_buttons:
        kb.insert(button)

    return kb


async def student_group_menu_kb(group_id) -> InlineKeyboardMarkup:
    """
    group_id - group's id from database to build a callback
    """
    kb = InlineKeyboardMarkup()
    group_buttons = [
        InlineKeyboardButton(
            text='➕Отправить лабораторную работу',
            callback_data=add_lab_callback.new(
                group_id=group_id, user_role="student")
        ),
        InlineKeyboardButton(
            text='📚Файлы лабораторных',
            callback_data=show_callback.new(
                data_type="lab", user_role="student")
        ),
    ]

    for button in group_buttons:
        kb.insert(button)

    return kb


async def get_groups_kb(group_names_and_ids: list[Group], role: str) -> InlineKeyboardMarkup:
    """returns inline keyboard with groups

    Args:
        group_names_and_ids: list of tuples with group's id and name
        role: str - student or teacher
    """
    # TODO: rewrite this function, add navigation arrows buttons to avoiding long list of groups
    kb = InlineKeyboardMarkup(row_width=1, )
    if group_names_and_ids:
        group_buttons = [
            InlineKeyboardButton(
                text=f'{group.name}',
                callback_data=group_callback.new(group_id=group.id, role=role))
            for group in group_names_and_ids
        ]

        for button in group_buttons:
            kb.insert(button)

    return kb


async def register_as_teacher_kb() -> InlineKeyboardMarkup:
    """returns inline keyboard with register as teacher button"""
    kb = InlineKeyboardMarkup(row_width=1, )
    kb.insert(InlineKeyboardButton(
        text='Зарегистрироваться',
        callback_data='register_as_teacher'), )

    return kb


async def confirmation_teacher_credentials() -> InlineKeyboardMarkup:
    kb = await confirmation_kb()
    kb.insert(InlineKeyboardButton(
        text='❌Ввести заново',
        callback_data='change_teacher_credentials'))

    return kb


async def admin_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1, )

    buttons = [
        InlineKeyboardButton(
            text='Войти как студент',
            callback_data='admin_mimic_a_student'),
        InlineKeyboardButton(
            text='Войти как преподаватель',
            callback_data='admin_mimic_a_teacher'),
        InlineKeyboardButton(
            text='Команды администратора',
            callback_data='admin_commands'),
    ]

    for button in buttons:
        kb.insert(button)

    return kb


async def yes_no_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2, )
    buttons = [
        InlineKeyboardButton(
            text='✅Да',
            callback_data='yes'),
        InlineKeyboardButton(
            text='❌Нет',
            callback_data='no'),
    ]

    for button in buttons:
        kb.insert(button)

    return kb


async def changed_mind_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1, )
    kb.insert(InlineKeyboardButton(
        text='❌Я передумал',
        callback_data='changed_mind'),)

    return kb


async def cloud_link_to_lab_kb(url: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1, )
    kb.insert(InlineKeyboardButton(
        text='🔗Ссылка на облако',
        url=url),)

    return kb


async def sample_files_with_cancel_button_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=3, )
    buttons = [
        InlineKeyboardButton(
            text='📄TXT пример',
            callback_data='sample:txt'),
        InlineKeyboardButton(
            text='📄CSV пример',
            callback_data='sample:csv'),
        InlineKeyboardButton(
            text='📄XLSX пример',
            callback_data='sample:xlsx'),
    ]
    for button in buttons:
        kb.insert(button)

    kb.add(InlineKeyboardButton(
        text='❌Отмена',
        callback_data='cancel'),)

    return kb


async def teacher_check_students_labs_kb(lab_id: int, show_rate_buttons: bool = True) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2, )
    if show_rate_buttons:
        rate_buttons = [
            InlineKeyboardButton(
                text='✅Принять',
                callback_data=check_lab_callback.new(
                    lab_id=lab_id, status='accepted'
                )
            ),
            InlineKeyboardButton(
                text='❌Отклонить',
                callback_data=check_lab_callback.new(
                    lab_id=lab_id, status='rejected'
                )
            ),
        ]
    else:
        rate_buttons = []

    if await database_manager.is_exist_previous_unchecked_lab_in_group(lab_id):
        rate_buttons.append(InlineKeyboardButton(
            text='⬅️',
            callback_data=check_lab_callback.new(
                lab_id=lab_id, status='previous'
            )
        )
        )

    if await database_manager.is_exist_next_unchecked_lab_in_group(lab_id):
        rate_buttons.append(InlineKeyboardButton(
            text='➡️',
            callback_data=check_lab_callback.new(
                lab_id=lab_id, status='next'
            )
        )
        )

    for button in rate_buttons:
        kb.insert(button)

    return kb
