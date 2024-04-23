from io import BytesIO
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold, hitalic, hlink
from loguru import logger

import keyboards as kb
from _legacy.laboratory_work import LaboratoryWork
from middlewares import rate_limit
from utils import states
from managers import GroupManager, CloudManager, LabManager
from loader import bot


def create_message_by_lab_work(lab_work: LaboratoryWork) -> str:
    message = f"Лабораторная работа №{hbold(lab_work.number)}\n" \
              f"Студент: {hbold(lab_work.member_credentials)}\n" \
              f"Лабораторная работа: {hbold(lab_work.description)}\n\n"

    return message


@rate_limit(limit=2)
async def show_not_checked_labs(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Загружаю лабы...", reply_markup=None)
    await states.TeacherState.check_students_labs.set()
    async with state.proxy() as data:
        group_id: int = data['group_id']
        group_name: str = data['group_name']

    first_not_checked_lab = await GroupManager.get_first_not_checked_lab_in_group(group_id=group_id)
    message = f"Выбранная группа:\n{hbold(group_name)}\n\n"
    message += create_message_by_lab_work(lab_work=first_not_checked_lab)

    document, filename = CloudManager.get_file_by_link(
        path=first_not_checked_lab.cloud_link)

    input_file = types.InputFile(document, filename=filename)
    await call.message.delete()
    await call.message.answer_document(input_file, caption=message,
                                       reply_markup=await kb.teacher_check_students_labs_kb(
                                           lab_id=first_not_checked_lab.id_),
                                       parse_mode=types.ParseMode.HTML)
    await state.update_data(current_lab_id=first_not_checked_lab.id_)


@rate_limit(limit=1)
async def show_next_not_checked_lab(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        group_id = data['group_id']
        group_name = data['group_name']
        current_lab_id = data['current_lab_id']

    next_not_checked_lab = await GroupManager.get_next_not_checked_lab_in_group(group_id=group_id,
                                                                                current_lab_id=current_lab_id)
    message = f"Выбранная группа:\n{hbold(group_name)}\n\n"
    message += create_message_by_lab_work(lab_work=next_not_checked_lab)

    document, filename = CloudManager.get_file_by_link(
        path=next_not_checked_lab.cloud_link)
    input_file = types.InputFile(document, filename=filename)

    await call.message.edit_media(
        types.InputMediaDocument(input_file, caption=message, parse_mode=types.ParseMode.HTML),
        reply_markup=await kb.teacher_check_students_labs_kb(lab_id=next_not_checked_lab.id_))
    await state.update_data(current_lab_id=next_not_checked_lab.id_)


async def show_previous_not_checked_lab(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        group_id = data['group_id']
        group_name = data['group_name']
        current_lab_id = data['current_lab_id']

    previous_not_checked_lab = await GroupManager.get_previous_not_checked_lab_in_group(group_id=group_id,
                                                                                        current_lab_id=current_lab_id)
    message = f"Выбранная группа:\n{hbold(group_name)}\n\n"
    message += create_message_by_lab_work(lab_work=previous_not_checked_lab)

    document, filename = CloudManager.get_file_by_link(
        path=previous_not_checked_lab.cloud_link)
    input_file = types.InputFile(document, filename=filename)

    await call.message.edit_media(
        types.InputMediaDocument(input_file, caption=message, parse_mode=types.ParseMode.HTML),
        reply_markup=await kb.teacher_check_students_labs_kb(lab_id=previous_not_checked_lab.id_))
    await state.update_data(current_lab_id=previous_not_checked_lab.id_)


async def accept_laboratory_work(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        lab_id = data['current_lab_id']

    student_telegram_id, message = LabManager.accept_laboratory_work(lab_id=lab_id)
    await bot.send_message(chat_id=student_telegram_id,
                           text=message,
                           parse_mode=types.ParseMode.HTML)
    await call.message.edit_caption(f"✅Лабораторная работа принята\n\n{call.message.caption}",
                                    reply_markup=await kb.teacher_check_students_labs_kb(lab_id=lab_id,
                                                                                         show_rate_buttons=False),
                                    parse_mode=types.ParseMode.HTML)


async def reject_laboratory_work(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        lab_id = data['current_lab_id']

    student_telegram_id, message = LabManager.reject_laboratory_work(lab_id=lab_id)
    await bot.send_message(chat_id=student_telegram_id,
                           text=message,
                           parse_mode=types.ParseMode.HTML)
    await call.message.edit_caption(f"❌Лабораторная работа отклонена\n\n{call.message.caption}",
                                    reply_markup=await kb.teacher_check_students_labs_kb(lab_id=lab_id,
                                                                                         show_rate_buttons=False),
                                    parse_mode=types.ParseMode.HTML)
