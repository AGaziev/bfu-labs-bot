from aiogram import types
from aiogram.dispatcher import FSMContext

from data import configuration


def is_user_admin(func):
    async def wrapped(message: types.Message, state: FSMContext):
        if message.from_user.id in configuration.admins:
            await func(message, state)
        else:
            await message.answer("You don't have permission to use this command.")
    return wrapped
