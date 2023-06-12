from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified

import keyboards
from data import config
import keyboards as kb
from middlewares import rate_limit
from utils import states

@rate_limit(limit=5)
async def login(message: types.Message):
    await message.answer("hello teacher", reply_markup=await keyboards.teacher_menu_kb())
    await states.Teacher.start.set()