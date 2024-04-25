from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked, ChatIdIsEmpty
from aiogram.utils.markdown import hbold

from loguru import logger

import keyboards as kb
from managers.user import UserManager
from middlewares import rate_limit

from loader import bot
from .is_admin_wrapper import is_user_admin


@rate_limit(limit=3)
@is_user_admin
async def invite_user_to_register_as_teacher(message: types.Message, state: FSMContext):
    try:
        username_or_user_id = message.text.split()[1]

    except IndexError:
        await message.answer("Ошибка ввода, введите username/telegram_id")

    else:
        if await send_invitation_message_to_user(username_or_user_id=username_or_user_id):
            await message.answer("Приглашение отправлено")
        else:
            await message.answer("Пользователь не найден или он заблокировал бота")


async def send_invitation_message_to_user(username_or_user_id: str) -> bool:
    if username_or_user_id.isdigit():
        user_id = int(username_or_user_id)
    else:
        user_id = await UserManager.get_user_by_username(username=username_or_user_id)

    try:
        await bot.send_message(chat_id=user_id, text=f"Вы были приглашены стать преподавателем.\n"
                                                     f"Введите необходисмые данные после нажатия на кнопку "
                                                     f"{hbold('Зарегистрироваться')}",
                               parse_mode=types.ParseMode.HTML,
                               reply_markup=await kb.register_as_teacher_kb())

    except BotBlocked:
        logger.warning(
            f"User {user_id} blocked bot or he doesn't start bot yet")
        return False

    except ChatIdIsEmpty:
        logger.warning(
            f"User with username {username_or_user_id} doesn't exist")
        return False

    else:
        return True
