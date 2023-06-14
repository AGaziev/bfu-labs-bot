from loguru import logger

from aiogram import types
from aiogram.dispatcher import FSMContext

from middlewares import rate_limit
import keyboards as kb

from data import configuration
from utils import states


@rate_limit(limit=5)
async def cmd_start(message: types.Message):
    if message.from_user.id not in configuration.admins:
        await states.registrator.name.set()
        await message.reply(f"Привет,{message.from_user.full_name}!\nКак тебя зовут?\n(Полное имя, фамилия)")


async def cmd_register_found_user(message: types.Message, state: FSMContext):
    # if found:
    await message.answer(f"Поздравляю с успешной регистрацией, {message.text} ")
    await state.finish()
