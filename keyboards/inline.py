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
        InlineKeyboardButton(
            text='Группа 1',
            callback_data='group1name'),
        InlineKeyboardButton(
            text='Группа 2',
            callback_data='group2name'),
    ]

    for button in group_buttons:
        kb.insert(button)

    kb.add(InlineKeyboardButton(
        text='Добавить новую группу', callback_data='add_new_group'))

    return kb

async def applying_kb():
    kb = InlineKeyboardMarkup()
    applying_buttons = [
        InlineKeyboardButton(
            text='Принять',
            callback_data='apply')
    ]

    return kb