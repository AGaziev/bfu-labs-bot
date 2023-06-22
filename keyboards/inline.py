from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from managers import database_manager

async def menu_kb() -> InlineKeyboardMarkup:
    """returns inline keyboard with menu items"""
    kb = InlineKeyboardMarkup(row_width=2,)
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
        callback_data='help'),)

    kb.add(InlineKeyboardButton(
        text='❌Close❌', callback_data='close_menu'))

    return kb

async def cancel_kb() -> InlineKeyboardMarkup:
    """returns inline keyboard with menu items"""
    kb = InlineKeyboardMarkup(row_width=1,)
    kb.insert(InlineKeyboardButton(
            text='❌Отмена❌',
            callback_data='cancel'),)

    return kb

async def teacher_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1, )
    group_buttons = [
        InlineKeyboardButton(
            text='➕Добавить новую группу',
            callback_data='add_new_group'),
        InlineKeyboardButton(
            text='📃Посмотреть все группы',
            callback_data='show_all_groups'),
    ]

    for button in group_buttons:
        kb.insert(button)

    return kb

async def student_menu_kb(telegram_id:int)->InlineKeyboardMarkup:
    # TODO: Кнопки на основе групп у студента
    # TODO: Использовать group_id в генерации callback_data
    #TODO: Клавиатура с группами, к которым присоединен студент будет в другой функции
    kb = InlineKeyboardMarkup(row_width=2, )
    if await database_manager.check_is_user_joined_any_education_group(telegram_id=telegram_id):
        kb.insert(InlineKeyboardButton(
            text='Мои лабы',
            callback_data=f'my_labs_user_id_{telegram_id}'),)

    kb.insert(InlineKeyboardButton(
            text='Подключиться к новой группе',
            callback_data='connect_to_group'),)

    return kb

async def confirmation_kb()->InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()

    kb.insert(InlineKeyboardButton(
        text='✅Подтвердить',
        callback_data='confirm'))

    return kb


async def group_kb(group_id)->InlineKeyboardMarkup:
    """
    group_id - group's id from database to build a callback
    """
    kb = InlineKeyboardMarkup()
    group_buttons = [
        InlineKeyboardButton(
            text='Добавить лабораторные',
            callback_data=f'add_labs:{group_id}'  # 123 like test group id
        )
    ]

    for button in group_buttons:
        kb.insert(button)

    return kb

async def get_groups_kb(group_names_and_ids: list[tuple[int,str]]) -> InlineKeyboardMarkup:
    """returns inline keyboard with groups"""
    #TODO: rewrite this function, add navigation arrows buttons to avoiding long list of groups
    kb = InlineKeyboardMarkup(row_width=1,)
    group_buttons = [
        InlineKeyboardButton(
            text=f'{group_name}',
            callback_data=f'group:{group_id}')  # 123 like test group id
        for group_id, group_name in group_names_and_ids
    ]

    for button in group_buttons:
        kb.insert(button)

    return kb

async def register_as_teacher_kb() -> InlineKeyboardMarkup:
    """returns inline keyboard with register as teacher button"""
    kb = InlineKeyboardMarkup(row_width=1,)
    kb.insert(InlineKeyboardButton(
        text='Зарегистрироваться',
        callback_data='register_as_teacher'),)

    return kb

async def confirmation_teacher_credentials()->InlineKeyboardMarkup:
    kb = await confirmation_kb()
    kb.insert(InlineKeyboardButton(
        text='❌Ввести заново',
        callback_data='change_teacher_credentials'))

    return kb

async def admin_menu_kb()->InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1, )

    buttons = [
        InlineKeyboardButton(
            text='Войти как студент',
            callback_data='admin_mimic_a_student'),
        InlineKeyboardButton(
            text='Войти как преподаватель',
            callback_data='admin_mimic_a_teacher'),
    ]

    for button in buttons:
        kb.insert(button)

    return kb