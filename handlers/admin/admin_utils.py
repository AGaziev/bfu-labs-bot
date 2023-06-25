from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode
from middlewares import rate_limit
from pprint import pformat
from .is_admin_wrapper import is_user_admin


@rate_limit(limit=3)
@is_user_admin
async def cmd_info(message: types.Message, state: FSMContext):
    await message.reply(hcode(pformat(message.to_python())), parse_mode=types.ParseMode.HTML)


@rate_limit(limit=3)
@is_user_admin
async def show_admin_commands(message_or_call: types.Message | types.CallbackQuery, state: FSMContext):
    commands = f"""/info - информация о сообщении
{hcode('/invite_teacher <username or user_id>')} - пригласить пользователя зарегистрироваться как преподаватель"""
    try:
        # if message is CallbackQuery
        await message_or_call.message.answer(commands, parse_mode=types.ParseMode.HTML)
    except AttributeError:
        # if message is Message
        await message_or_call.answer(commands, parse_mode=types.ParseMode.HTML)
