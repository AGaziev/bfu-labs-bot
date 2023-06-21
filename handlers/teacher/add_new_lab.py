from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold, hitalic, hlink
from io import BytesIO
from loguru import logger

import keyboards as kb
from middlewares import rate_limit
from utils import states
from managers import GroupManager, CloudDriveManager, database_manager


@rate_limit(limit=3)
async def wait_for_lab_conditions_file(call: types.CallbackQuery, state: FSMContext):
    """Wait for lab rules file"""
    await call.message.edit_text("Отправьте файл с условиями лабораторной работы")
    await states.TeacherState.add_new_lab.set()
    async with state.proxy() as data:
        data['group_name'] = await database_manager.select_group_name_by_group_id(group_id=call.data.split(":")[-1])


async def upload_lab_conditions_file_to_cloud(message: types.Message, state: FSMContext):
    """Upload lab rules file"""
    if not message.document:
        await message.answer("Ошибка, отправьте файл с условиями лабораторной работы")
        return

    filename = message.document.file_name
    io_file = BytesIO()
    await message.document.download(destination=io_file)
    io_file.seek(0)  # set pointer to the beginning of file

    try:
        async with state.proxy() as data:
            CloudDriveManager.add_lab_to_group_folder(group_name=data['group_name'],
                                                      filename=filename,
                                                      file=io_file)
    except Exception as e:
        # TODO: handle specific exceptions
        await message.answer(f"Ошибка загрузки файла: {e}")
        logger.info(e)