# TODO import refactor

from aiogram import types

import keyboards as kb
from middlewares import rate_limit
from utils import states

@rate_limit(limit=5)
async def login(message: types.Message):
    await message.answer("hello student", reply_markup=await kb.student_menu_kb())
    await states.Student.start.set()