from loguru import logger

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold

from managers.db import DatabaseManager
from middlewares import rate_limit
import keyboards as kb

from data import configuration
from utils import states


@rate_limit(limit=3)
async def cmd_start(message: types.Message, state: FSMContext):
    if state:
        await state.finish()
    DatabaseManager.update_user_is_blocked_field_by_user_id(user_id=message.from_user.id,
                                                                   is_blocked=False)
    user_id = message.from_user.id
    if not DatabaseManager.is_user_exist(user_id):
        DatabaseManager.insert_new_user(user_id=user_id,
                                               username=message.from_user.username)
        logger.info(
            f"New user {message.from_user.full_name} with id {user_id} was added to database")

    if user_id not in configuration.admins:

        # await message.reply(f"Привет, {hbold(message.from_user.full_name)}!\nЭто бот для проверки лабораторных работ",
        #                     reply_markup=await kb.student_menu_kb(telegram_id=message.from_user.id),
        #                     parse_mode=types.ParseMode.HTML)

        if DatabaseManager.check_is_user_teacher(user_id=user_id):
            await message.reply(f"С возвращением, {hbold(message.from_user.full_name)}",
                                reply_markup=await kb.teacher_menu_kb(),
                                parse_mode=types.ParseMode.HTML)
            logger.info(
                f"Teacher {message.from_user.full_name} with id {user_id} was returned")
            await states.TeacherState.start.set()

        else:
            await message.reply(f"С возвращением, {hbold(message.from_user.full_name)}",
                                reply_markup=await kb.student_menu_kb(telegram_id=user_id),
                                parse_mode=types.ParseMode.HTML)
            logger.info(
                f"Student {message.from_user.full_name} with id {user_id} was returned")
            await states.Student.start.set()

    else:
        await message.answer(f"С возвращением, администратор {hbold(message.from_user.full_name)}",
                             reply_markup=await kb.admin_menu_kb(),
                             parse_mode=types.ParseMode.HTML)
        logger.info(
            f"Admin {message.from_user.full_name} with id {message.from_user.id} was returned")
