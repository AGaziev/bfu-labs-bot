from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold, hlink
from io import BytesIO
from loguru import logger

import keyboards as kb
from middlewares import rate_limit
from utils import states
from managers import GroupManager, CloudManager, database_manager


@rate_limit(limit=3)
async def wait_for_lab_conditions_file(call: types.CallbackQuery, state: FSMContext):
    """Wait for lab rules file"""
    await call.message.edit_text("Отправьте файл с условиями лабораторной работы",
                                 reply_markup=await kb.cancel_kb())
    await states.TeacherState.add_lab.upload_lab_file.set()

async def ask_for_filename_to_change(message: types.Message, state: FSMContext):
    """Ask for filename to change it"""
    try:
        io_file = BytesIO()
        await message.document.download(destination_file=io_file)
        io_file.seek(0)  # set pointer to the beginning of file
    except Exception as err:
        # TODOL: handle specific exceptions
        logger.error(f"Error while downloading file: {err}")
        await message.answer("Произошла ошибка при загрузке файла, попробуйте еще раз")
        return
    else:
        await state.update_data(filename=message.document.file_name)
        await state.update_data(file_extension=message.document.file_name.split(".")[-1])
        await state.update_data(io_file=io_file)
        await message.answer(f"Файл {hbold(message.document.file_name)} получен.\nВас устраивает имя файла?",
                             reply_markup=await kb.yes_no_kb(),
                             parse_mode=types.ParseMode.HTML)
        await states.TeacherState.add_lab.ask_for_filename_to_change.set()


async def wait_for_new_filename(call: types.CallbackQuery, state: FSMContext):
    """Change filename"""
    await call.message.edit_text("Введите новое имя файла",
                                 reply_markup=await kb.changed_mind_kb())
    await states.TeacherState.add_lab.wait_for_new_filename.set()


async def change_filename(message:types.Message, state: FSMContext):
    """Change filename"""
    async with state.proxy() as data:
        file_extension = data["file_extension"]

    await state.update_data(filename=message.text+"."+file_extension)
    await message.answer(f"Имя файла изменено на {hbold(message.text+'.'+file_extension)}\nОно вас устраивает?",
                         reply_markup=await kb.yes_no_kb(),
                         parse_mode=types.ParseMode.HTML)
    await states.TeacherState.add_lab.ask_for_filename_to_change.set()

async def upload_file_to_cloud_drive(call:types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        io_file = data["io_file"]
        filename = data["filename"]
        group_name = data["group_name"]

    await call.message.edit_text(f"Загружаю файл {hbold(filename)} на облачный диск",
                                 reply_markup= None,
                                 parse_mode=types.ParseMode.HTML)

    lab_path = CloudManager.add_lab_to_group_folder(group_name=group_name, lab_path_or_file=io_file, lab_name=filename)
    lab_url = CloudManager.get_public_link_by_destination_path(destination_path=lab_path)
    group_id = await database_manager.select_group_id_by_group_name(group_name=group_name)

    await call.message.answer(f"Файл {hbold(filename)} успешно загружен на облачный диск\n{hlink('Ссылка на файл', url=lab_url)}",
                              parse_mode=types.ParseMode.HTML)

    await GroupManager.add_lab_to_db_and_notify_students(group_id=group_id,
                                                         lab_name=filename.split('.')[0] if '.' in filename else filename,
                                                         lab_link=lab_url,
                                                         lab_path=lab_path)
