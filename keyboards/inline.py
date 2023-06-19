from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def menu_kb():
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


async def teacher_menu_kb():
    kb = InlineKeyboardMarkup(row_width=2, )
    group_buttons = [
        # TODO: Кнопки на основе групп у преподавателя
        # TODO: Использовать group_id в генерации callback_data
        InlineKeyboardButton(
            text='Группа 1',
            callback_data='group:1'),
        InlineKeyboardButton(
            text='Группа 2',
            callback_data='group:2'),
    ]

    for button in group_buttons:
        kb.insert(button)

    kb.add(InlineKeyboardButton(
        text='Добавить новую группу', callback_data='add_new_group'))

    return kb

async def student_menu_kb():
    kb = InlineKeyboardMarkup(row_width=2, )
    group_buttons = [
        # TODO: Кнопки на основе групп у студента
        # TODO: Использовать group_id в генерации callback_data
        InlineKeyboardButton(
            text='Группа 1',
            callback_data='group:1'),
        InlineKeyboardButton(
            text='Группа 2',
            callback_data='group:2'),
    ]

    for button in group_buttons:
        kb.insert(button)

    kb.add(InlineKeyboardButton(
        text='Подключиться к новой группе', callback_data='connect_to_group'))

    return kb

async def applying_kb():
    kb = InlineKeyboardMarkup()
    applying_buttons = [
        InlineKeyboardButton(
            text='Принять',
            callback_data='apply')
    ]

    for button in applying_buttons:
        kb.insert(button)

    return kb


async def group_kb(group_id):
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