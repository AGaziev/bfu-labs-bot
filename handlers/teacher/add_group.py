import io

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified
from aiogram.utils.markdown import escape_md

import keyboards
from data import config
import keyboards as kb
from middlewares import rate_limit
from utils import states
from managers import GroupManager


async def set_new_group_name(callback: types.CallbackQuery):
    await callback.message.answer("Напишите название вашей новой группы")
    await callback.message.delete()
    await states.Teacher.add_group.name.set()


async def set_new_group_students(message: types.Message, state: FSMContext):
    if GroupManager.group_name_exists(message.text): # TODO: to validate type (with exist and bad names check)
        await message.answer(f"Такое название занято, используйте другое")
    else:
        await message.answer(f"Название вашей группы: {message.text}\n\n"
                             f"Прикрепите txt файл со списком студентов в этой группе")
        async with state.proxy() as group_data:
            group_data["name"] = message.text
        await states.Teacher.add_group.students.set()


async def correcting_students_list(message: types.Message, state: FSMContext):
    # add file in buffer
    file_in_io = io.BytesIO()
    await message.document.download(destination_file=file_in_io)

    # read file from buffer and split+format
    students = file_in_io.read().decode().split("\r\n")
    students = [stdnt.strip() for stdnt in students if stdnt.strip() != ""]

    async with state.proxy() as group_data:
        group_data["students"] = students
        studentList = '\n'.join(group_data['students'][:5])
        group_name = escape_md(group_data['name'])
        await message.answer(f"Название вашей группы: *{group_name}*\n\n"
                             f"Первые 5 студентов из группы:\n"
                             f"*{studentList}*\n\n"
                             f"Если не сходится попробуйте снова загрузить файл со списком студентов в txt формате",
                             reply_markup=await kb.applying_kb(),
                             parse_mode="MarkdownV2")


async def end_group_add(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as group_data:
        group_data["disk_url"], group_id = GroupManager.create_group(group_data["name"], group_data["students"])
        group_name = escape_md(group_data['name'])
        group_url = escape_md(group_data['disk_url'])
        await callback.message.answer(f"Группа *{group_name}* успешно создана\n"
                                      f"[Ссылка на группу]({group_url})",
                                      reply_markup=await kb.group_kb(group_id),
                                      parse_mode="MarkdownV2")
        await state.finish()