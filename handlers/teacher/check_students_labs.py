from io import BytesIO
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold, hitalic, hlink
from loguru import logger

import keyboards as kb
from middlewares import rate_limit
from utils import states
from utils.models import LaboratoryWork
from managers import GroupManager, CloudManager, database_manager


def create_message_by_lab_work(lab_work: LaboratoryWork) -> str:
    message = f"Лабораторная работа №{hbold(lab_work.lab_number)}\n"\
        f"Студент: {hbold(lab_work.member_credentials)}\n"\
        f"Лабораторная работа: {hbold(lab_work.lab_description)}\n\n"

    return message


@rate_limit(limit=2)
async def show_not_checked_labs(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Загружаю лабы...", reply_markup=None)
    async with state.proxy() as data:
        group_id = data['group_id']
        group_name = data['group_name']

    first_not_checked_lab = await GroupManager.get_first_not_checked_lab_in_group(group_id=group_id)
    message = f"Вы выбрали группу\n{hbold(group_name)}\n\n"
    message += create_message_by_lab_work(lab_work=first_not_checked_lab)

    document: BytesIO = await CloudManager.get_file_by_link(file_link=first_not_checked_lab.cloud_link)
    input_file = types.InputFile(
        document, filename=f"{first_not_checked_lab.lab_description}.zip")

    await call.message.delete()
    await call.message.answer_document(input_file, caption=message, reply_markup=await kb.teacher_check_students_labs_kb(group_id=group_id, lab_id=first_not_checked_lab.lab_id))
