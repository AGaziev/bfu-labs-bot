
from aiogram import types
from aiogram.dispatcher import FSMContext

from middlewares import rate_limit

from .is_admin_wrapper import is_user_admin


@rate_limit(limit=3)
@is_user_admin
async def cmd_info(message: types.Message):
    await message.reply(message)


@rate_limit(limit=3)
@is_user_admin
async def show_admin_commands(message: types.Message, state: FSMContext):
    commands = """/info - информация о сообщении
/invite_teacher <username or user_id> - пригласить пользователя зарегистрироваться как преподаватель"""
    await message.answer(commands)
