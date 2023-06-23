from io import BytesIO

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold, hitalic, hlink
import keyboards as kb
from middlewares import rate_limit
from utils import states
from managers import GroupManager, database_manager
from utils.parsers import TxtParser


@rate_limit(limit=3)
async def set_new_group_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Напишите название вашей новой группы", reply_markup=await kb.cancel_kb())
    await states.TeacherState.add_group.name.set()


@rate_limit(limit=3)
async def set_new_group_students(message: types.Message, state: FSMContext):
    # TODO: to validate type (with exist and bad names check)
    group_name = message.text.upper()
    owner_credentials = await database_manager.select_teacher_credentials_by_telegram_id(telegram_id=message.from_user.id)
    repository_name = f"{group_name}_{owner_credentials.firstname}_{owner_credentials.lastname}"
    if owner_credentials.patronymic:
        repository_name += f"_{owner_credentials.patronymic}"

    if await GroupManager.group_name_exists(repository_name):
        await message.answer(f"Название {hbold(repository_name)} уже занято, попробуйте другое",
                             reply_markup=await kb.cancel_kb(), parse_mode=types.ParseMode.HTML, )
    else:
        await message.answer(f"Название вашей группы: {hbold(repository_name)}\n\n"
                             f"Прикрепите txt файл со списком студентов в этой группе",
                             reply_markup=await kb.cancel_kb(), parse_mode=types.ParseMode.HTML)
        async with state.proxy() as group_data:
            group_data["name"] = repository_name
        await states.TeacherState.add_group.students.set()


@rate_limit(limit=3)
async def correcting_students_list(message: types.Message, state: FSMContext):
    # add file in buffer
    file_in_io = BytesIO()
    await message.document.download(destination_file=file_in_io)

    match message.document.file_name.split(".")[-1]:
        case "txt":
            students = TxtParser.get_all_lines(file_in_io)
        # TODO: add csv, xlsx parsers
        # case "csv":
        #     ...
        # case "xlsx":
        #     ...
        case _:
            await message.answer("Неверный формат файла, попробуйте снова", reply_markup=await kb.cancel_kb())
            return

    async with state.proxy() as group_data:
        group_data["students"] = students
        first_five_students = '\n'.join(group_data['students'][:5])
        group_name = group_data['name']
        await message.answer(f"Название вашей группы: {hbold(group_name)}\n\n"
                             f"Первые 5 студентов из группы:\n"
                             f"{hitalic(first_five_students)}\n\n"
                             f"Если не сходится попробуйте снова загрузить файл со списком студентов в txt формате",
                             reply_markup=await kb.confirmation_kb(),
                             parse_mode="HTML")


async def end_group_add(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as group_data:
        group_data["cloud_drive_url"], group_id = await GroupManager.create_group(
            group_data["name"], group_data["students"], callback.from_user.id)
        group_name = group_data['name']
        group_url = group_data['cloud_drive_url']
        await callback.message.answer(f"Группа {hbold(group_name)} успешно создана\n"
                                      f"{hlink('Ссылка на группу', group_url)}",
                                      reply_markup=await kb.group_kb(group_id),
                                      parse_mode="HTML")
        await database_manager.insert_many_members_into_education_group(group_id=group_id, members=group_data["students"])
        await state.finish()
