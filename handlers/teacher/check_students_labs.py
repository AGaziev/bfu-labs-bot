from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold

import keyboards as kb
from middlewares import rate_limit
from utils import states, LabWork
from managers import GroupManager, CloudManager, LabManager
from loader import bot
from utils.LabInfo import LabInfo
from utils.carousel import Carousel


def create_message_by_lab_work(lab_work: LaboratoryWork) -> str:
    message = f"Лабораторная работа №{hbold(lab_work.number)}\n" \
              f"Студент: {hbold(lab_work.member_credentials)}\n" \
              f"Лабораторная работа: {hbold(lab_work.description)}\n\n"

    return message


@rate_limit(limit=2)
async def show_not_checked_labs(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Загружаю лабы...", reply_markup=None)
    async with state.proxy() as data:
        group_id: int = data['group_id']
        group_name: str = data['name']
    not_checked_labs = LabManager.get_not_checked_labs_for_teacher(group_id)
    if len(not_checked_labs) == 0:
        await call.message.answer("Лабораторных нет")
        return
    labs_carousel = Carousel(not_checked_labs)
    await state.update_data(labs_carousel=labs_carousel)

    await states.TeacherState.check_students_labs.set()
    first_not_checked_lab = not_checked_labs[0]
    message = f"Выбранная группа:\n{hbold(group_name)}\n\n"
    message += create_message_by_lab_work(lab_work=first_not_checked_lab)

    document, filename = CloudManager.get_file_by_link(
        path=first_not_checked_lab.cloud_link)

    input_file = types.InputFile(document, filename=filename)
    await call.message.delete()
    await call.message.answer_document(input_file, caption=message,
                                       reply_markup=await kb.teacher_check_students_labs_kb(
                                           lab_id=first_not_checked_lab.id),
                                       parse_mode=types.ParseMode.HTML)
    await state.update_data(current_lab_id=first_not_checked_lab.id)


@rate_limit(limit=1)
async def navigate_labs(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data['status']

    async with state.proxy() as data:
        group_id: int = data['group_id']
        group_name: str = data['name']
        labs: Carousel = data["labs_carousel"]
    if action == "previous":
        current_lab = labs.prev()
    elif action == "next":
        current_lab = labs.next()
    else:
        current_lab = labs.get()

    prepared_lab = get_input_media_from_lab(current_lab, group_name)

    await call.message.edit_media(
        prepared_lab,
        reply_markup=await kb.teacher_check_students_labs_kb(lab_id=current_lab.id))


def get_input_media_from_lab(lab: LabWork, group_name: str):
    message = f"Выбранная группа:\n{hbold(group_name)}\n\n"
    message += create_message_by_lab_work(lab_work=lab)

    document, filename = CloudManager.get_file_by_link(
        path=lab.cloud_link)
    input_file = types.InputFile(document, filename=filename)
    return types.InputMediaDocument(input_file, caption=message, parse_mode=types.ParseMode.HTML)

async def update_unchecked_labs(group_id, call, state):
    not_checked_labs = LabManager.get_not_checked_labs_for_teacher(group_id)
    if len(not_checked_labs) == 0:
        await call.message.answer("Лабораторных нет")
        return False
    labs_carousel = Carousel(not_checked_labs)
    await state.update_data(labs_carousel=labs_carousel)
    return True

# TODO: UNION THIS TWO METHODS BY CALLBACKS (like mark:accept/reject:lab_id)
async def accept_laboratory_work(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        labs = data['labs_carousel']
        group_id: int = data['group_id']
    current_lab = labs.get()
    student, message = LabManager.accept_laboratory_work(current_lab)
    await bot.send_message(chat_id=student.telegram_id,
                           text=message,
                           parse_mode=types.ParseMode.HTML)
    if not await update_unchecked_labs(group_id, call, state):
        await call.message.answer("Все сданные на данный момент лабораторные проверены!")
        return
    await call.message.edit_caption(f"✅Лабораторная работа принята\n\n{call.message.caption}",
                                    reply_markup=await kb.teacher_check_students_labs_kb(lab_id=current_lab.id,
                                                                                         show_rate_buttons=False),
                                    parse_mode=types.ParseMode.HTML)


async def reject_laboratory_work(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        labs = data['labs_carousel']
        group_id: int = data['group_id']
    current_lab = labs.get()
    student, message = LabManager.reject_laboratory_work(current_lab)
    await bot.send_message(chat_id=student.telegram_id,
                           text=message,
                           parse_mode=types.ParseMode.HTML)
    if not await update_unchecked_labs(group_id, call, state):
        await call.message.answer("Все сданные на данный момент лабораторные проверены!")
        return
    await call.message.edit_caption(f"❌Лабораторная работа отклонена\n\n{call.message.caption}",
                                    reply_markup=await kb.teacher_check_students_labs_kb(lab_id=current_lab.id,
                                                                                         show_rate_buttons=False),
                                    parse_mode=types.ParseMode.HTML)
