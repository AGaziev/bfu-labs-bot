from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold, hitalic, hlink, hcode
from aiogram.utils.exceptions import BotBlocked
from loguru import logger
from loader import bot

import keyboards as kb
from middlewares import rate_limit
from utils import states
from managers import database_manager
from data import configuration


@rate_limit(limit=3)
async def register_as_teacher(call: types.CallbackQuery, state: FSMContext):
    """Register as teacher"""
    if state:
        await state.finish()
    await call.message.edit_text(f"Отлично, отправьте мне свое фио в формате:\n{hitalic('Иванов Иван Иванович')}\nЕсли у вас нет отчества - просто отправьте фамилию и имя",
                                parse_mode=types.ParseMode.HTML)
    await states.TeacherState.registration.input_credentials.set()


@rate_limit(limit=3)
async def confirm_teacher_credentials(message: types.Message, state: FSMContext):
    """Confirm teacher credentials"""
    credentials = message.text.strip().split()
    for value_index in range(len(credentials)):
        credentials[value_index] = credentials[value_index].capitalize()

    async with state.proxy() as data:
        data['credentials'] = credentials

    firstname = credentials[1]
    lastname = credentials[0]
    patronymic = credentials[2] if len(credentials) == 3 else None

    await message.answer(f"Ваши данные:\n\nИмя: {hbold(firstname)}\nФамилия: {hbold(lastname)}\n{'Отчество: '+hbold(patronymic) if patronymic else ''}",
                         parse_mode=types.ParseMode.HTML,
                         reply_markup=await kb.confirmation_teacher_credentials())
    await states.TeacherState.registration.confirmation.set()

async def change_teacher_credentials(call:types.CallbackQuery, state:FSMContext):
    await register_as_teacher(call,state)

@rate_limit(limit=3)
async def confirm_credentials_and_write_to_database(call: types.CallbackQuery, state: FSMContext):
    """Confirm credentials and write to database"""
    async with state.proxy() as data:
        credentials:list[str] = data['credentials']
    await database_manager.insert_new_teacher(telegram_id=call.from_user.id,
                                          last_name=credentials[0],
                                          first_name=credentials[1],
                                          patronymic=credentials[2] if len(credentials) == 3 else None)
    await call.message.edit_text("Вы успешно зарегистрированы", reply_markup=await kb.teacher_menu_kb())
    await state.finish()

    await notify_admins_about_teacher_registration_success(telegram_id=call.from_user.id,
                                                           username = call.from_user.username if call.from_user.username else None)
    logger.info(f"Teacher with telegram_id: {call.from_user.id} registered")


async def notify_admins_about_teacher_registration_success(telegram_id: int, username:str|None):
    """Notify admins about teacher registration success"""
    for admin_id in configuration.admins:
        try:
            await bot.send_message(chat_id=admin_id,
                                text=f"Преподаватель с telegram_id: {hcode(telegram_id)}{', '+hlink(title=username, url='t.me/'+username) if username else ''} зарегистрировался",
                                parse_mode=types.ParseMode.HTML)
        except BotBlocked:
            logger.warning(f"Admin with telegram_id: {admin_id} blocked bot")