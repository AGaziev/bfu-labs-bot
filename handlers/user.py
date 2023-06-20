from loguru import logger

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold

from middlewares import rate_limit
import keyboards as kb

from data import configuration
from utils import states
from managers import database_manager


@rate_limit(limit=3)
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    if message.from_user.id not in configuration.admins:

        if not await database_manager.check_is_user_exist(user_id=message.from_user.id):
            await database_manager.insert_new_user(user_id=message.from_user.id,
                                                   username=message.from_user.username)
            logger.info(
                f"New user {message.from_user.full_name} with id {message.from_user.id} was added to database")
            await message.reply(f"Привет,{hbold(message.from_user.full_name)}!\nЭто бот для проверки лабораторных работ",
                                reply_markup=await kb.student_menu_kb(),
                                parse_mode=types.ParseMode.HTML)

        elif await database_manager.check_is_user_teacher(user_id=message.from_user.id):
            await message.reply(f"С возвращением, {hbold(message.from_user.full_name)}",
                                reply_markup=await kb.teacher_menu_kb(),
                                parse_mode=types.ParseMode.HTML)
            logger.info(
                f"Teacher {message.from_user.full_name} with id {message.from_user.id} was returned")

        else:
            await message.reply(f"С возвращением, {hbold(message.from_user.full_name)}",
                                reply_markup=await kb.student_menu_kb(),
                                parse_mode=types.ParseMode.HTML)
            logger.info(
                f"Student {message.from_user.full_name} with id {message.from_user.id} was returned")

    else:
        await message.answer(f"С возвращением, администратор {hbold(message.from_user.username or message.from_user.full_name)}",
                             parse_mode=types.ParseMode.HTML)
        logger.info(
            f"Admin {message.from_user.full_name} with id {message.from_user.id} was returned")
