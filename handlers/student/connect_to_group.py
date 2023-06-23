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


async def set_connecting_group_name(call: types.CallbackQuery):
    await call.message.answer("Напишите название группы к которой хотите подключиться")
    await call.message.delete()
    await states.Student.connect_to_group.group_name.set()


async def show_student_list_of_group(message: types.Message, state: FSMContext):
    if await GroupManager.is_group_name_exists(name=message.text):
        async with state.proxy() as connecting_data:
            # GroupManager.get_unregistered_users_of_group(group_id=test)
            # TODO достаем список студентов этой группы + их id (НЕПОДКЛЮЧЕННЫХ ЕЩЕ)
            connecting_data["students"] = {
                112: "Газиев Алан",
                413: "Вебер Дмитрий",
                125: "Ягубков Даниил"
            }
            # формируем список можно будет переделать потом красиво и понятно
            # {id}. {name surname}
            await message.answer("\n".join([f"{i}. {s}" for i, s in connecting_data["students"].items()]))
            await message.answer("Выберите из списка введя число перед вашим ФИО")
            await states.Student.connect_to_group.choose_name.set()
    else:
        await message.answer("Такой группы нет, уточните у преподавателя и напишите название еще раз")


async def choosing_student(message: types.Message, state: FSMContext):
    async with state.proxy() as connecting_data:
        try:
            student_id = int(message.text)
            name = connecting_data['students'][student_id]
            connecting_data['student_name'] = name
            connecting_data['student_id'] = student_id
            await message.answer(f"Вы {name}?\n"
                                 f"Если нет, то напишите еще раз число", reply_markup=await kb.confirmation_kb())
        except (ValueError, KeyError):
            await message.answer("Такого номера нет, напишите еще раз число")


async def end_connecting_to_group(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as connecting_data:
        GroupManager.connect_student_to_group(connecting_data['student_name'], connecting_data['student_id'])
        await call.message.answer(f"Вы подключены к группе {connecting_data['group_name']}")
