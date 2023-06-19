from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified, BotBlocked
from loguru import logger

from data import configuration
import keyboards as kb
from middlewares import rate_limit

from loader import bot
from managers import database_manager


def is_user_admin(func):
    async def wrapped(message: types.Message, state: FSMContext):
        if message.from_user.id in configuration.admins:
            await func(message, state)
        else:
            await message.answer("You don't have permission to use this command.")
    return wrapped


@rate_limit(limit=3)
@is_user_admin
async def cmd_info(message: types.Message):
    await message.reply(message)


@rate_limit(limit=3)
@is_user_admin
async def show_admin_commands(message: types.Message):
    commands = """/info - информация о сообщении
/invite_teacher <username or user_id> - пригласить пользователя зарегистрироваться как преподаватель"""
    await message.answer(commands)


@rate_limit(limit=3)
@is_user_admin
async def invite_user_to_register_as_teacher(message: types.Message):
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
        user_id = await database_manager.select_telegram_id_by_username(username=username_or_user_id)

    try:
        await bot.send_message(chat_id=user_id, text="Вы были приглашены стать преподавателем.",
                               reply_markup=await kb.register_as_teacher_kb())

    except BotBlocked:
        logger.warning(
            f"User {user_id} blocked bot or he doesn't start bot yet")
        return False

    else:
        return True
