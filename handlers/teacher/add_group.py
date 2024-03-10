from io import BytesIO

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold, hitalic, hlink
import keyboards as kb
from managers.db import DatabaseManager
from middlewares import rate_limit
from utils import states
from managers import GroupManager
from utils.parsers import TxtParser
from utils.samples_gerenator import SamplesGenerator


@rate_limit(limit=3)
async def set_new_group_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Напишите название вашей новой группы", reply_markup=await kb.cancel_kb())
    await states.TeacherState.add_group.name.set()


@rate_limit(limit=3)
async def set_new_group_students(message: types.Message, state: FSMContext, user_id: int = None):
    # TODO: to validate type (with exist and bad names check)
    group_name = message.text.upper().replace(' ', '_')
    owner_credentials = DatabaseManager.select_teacher_credentials_by_telegram_id(telegram_id=message.from_user.id)
    repository_name = f"{group_name}_{owner_credentials.first_name}_{owner_credentials.last_name}"
    if owner_credentials.patronymic:
        repository_name += f"_{owner_credentials.patronymic}"

    if GroupManager.is_group_name_exists(repository_name):
        await message.answer(f"Название {hbold(repository_name)} уже занято, попробуйте другое",
                             reply_markup=await kb.cancel_kb(), parse_mode=types.ParseMode.HTML, )
    else:
        await message.answer(f"Название вашей группы: {hbold(repository_name)}\n\n"
                             f"Прикрепите txt файл со списком студентов в этой группе",
                             reply_markup=await kb.sample_files_with_cancel_button_kb(), parse_mode=types.ParseMode.HTML)
        async with state.proxy() as group_data:
            group_data["name"] = repository_name
        await states.TeacherState.add_group.students.set()


@rate_limit(limit=3)
async def send_file_sample(call: types.CallbackQuery, state: FSMContext):
    extension = call.data.split(":")[-1]
    match extension:
        case "txt":
            file_ = SamplesGenerator.get_students_list_txt_example()
        case "csv":
            file_ = SamplesGenerator.get_students_list_csv_example()
        case "xlsx":
            file_ = SamplesGenerator.get_students_list_xlsx_example()
        case _:
            await call.message.edit_text("Неверный формат файла, попробуйте снова", reply_markup=await kb.cancel_kb())
            return

    input_file = types.InputFile(
        file_, filename=f"sample.{extension}")

    await call.message.answer_document(document=input_file,
                                       caption=f"Пример {hbold(extension.upper())} файла со списком студентов",
                                       parse_mode=types.ParseMode.HTML)


@rate_limit(limit=3)
async def correcting_students_list(message: types.Message, state: FSMContext):
    # add file in buffer
    file_in_io = BytesIO()
    await message.document.download(destination_file=file_in_io)

    match message.document.file_name.split(".")[-1]:
        case "txt":
            students = TxtParser.get_all_lines(file_in_io)
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
                             f"Все верно?",
                             reply_markup=await kb.yes_no_kb(),
                             parse_mode="HTML")
        await states.TeacherState.add_group.confirm.set()


async def change_stundents_list_to_new_file(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Прикрепите txt файл со списком студентов в этой группе",
                                     reply_markup=await kb.cancel_kb(), parse_mode=types.ParseMode.HTML)
    await states.TeacherState.add_group.students.set()


async def end_group_add(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as group_data:
        group_data["cloud_drive_url"], group_id = await GroupManager.create_group(
            group_data["name"], group_data["students"], call.from_user.id)
        group_name = group_data['name']
        group_url = group_data['cloud_drive_url']
        await call.message.answer(f"Группа {hbold(group_name)} успешно создана\n"
                                  f"{hlink('Ссылка на группу', group_url)}",
                                  reply_markup=await kb.teacher_group_menu_kb(group_id),
                                  parse_mode="HTML")
        await state.finish()
        await states.TeacherState.group_menu.set() #FIXME ??
