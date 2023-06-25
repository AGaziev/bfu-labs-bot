from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards as kb
from utils import states
from utils import Formatter
from managers import GroupManager


async def set_connecting_group_name(call: types.CallbackQuery):
    await call.message.answer("Напишите название группы к которой хотите подключиться",
                              reply_markup=await kb.cancel_kb())
    await call.message.delete()
    await states.Student.connect_to_group.group_name.set()


async def show_student_list_of_group(message: types.Message, state: FSMContext):
    if await GroupManager.is_group_name_exists(name=message.text):
        group_id = await GroupManager.get_group_id_by_name(name=message.text)
        if not await GroupManager.is_student_already_connected(telegram_id=message.from_user.id, group_id=group_id):
            async with state.proxy() as connecting_data:
                connecting_data["group_name"] = message.text
                connecting_data["students"] = \
                    await GroupManager.get_unregistered_users_of_group(group_name=message.text)
                # формируем список можно будет переделать потом красиво и понятно
                await message.answer(Formatter.list_of_students(connecting_data["students"]))
                await message.answer("Выберите из списка введя число перед вашим ФИО",
                                    reply_markup=await kb.cancel_kb())
                await states.Student.connect_to_group.choose_name.set()
    else:
        await message.answer("Такой группы нет, уточните у преподавателя и напишите название еще раз",
                             reply_markup=await kb.cancel_kb())


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
            await message.answer(Formatter.list_of_students(connecting_data["students"]),
                                 reply_markup=await kb.cancel_kb())


async def end_connecting_to_group(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as connecting_data:
        await GroupManager.connect_student_to_group(connecting_data['group_name'],
                                                    connecting_data['student_name'],
                                                    connecting_data['student_id'],
                                                    call.from_user.id)
        await call.message.answer(f"Вы подключены к группе {connecting_data['group_name']}")
        await state.finish()
