from aiogram import types
from aiogram.dispatcher import FSMContext
import keyboards as kb
from middlewares import rate_limit
from aiogram.utils.markdown import hbold
from managers import database_manager
from utils import states, Formatter
from managers import LabManager


async def student_group_menu(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    # call.data sample: "group:1:student"
    group_id = callback_data["group_id"]
    lab_stats = LabManager.get_student_lab_stats(group_id, call.from_user.id)
    group_name = await database_manager.select_group_name_by_group_id(group_id=group_id)
    await call.message.edit_text(f"{hbold(group_name)}\n"
                                 f"{Formatter.group_menu_lab_stats(lab_stats)}",
                                 reply_markup=await kb.student_group_menu_kb(group_id=group_id),
                                 parse_mode=types.ParseMode.HTML)
    await state.update_data(group_name=group_name)
    await states.Student.group_menu.set()


async def show_not_done_labs_files(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        labs_files = await LabManager.get_student_undone_labs_files(data["group_id"], call.from_user.id)
        labs_input = []
        for file in labs_files:
            file.seek(0)
            inputLab = types.InputFile(file)
            labs_input.append(types.InputMediaDocument(inputLab))
        print(labs_input)
        await call.message.answer_media_group(types.MediaGroup(labs_input))
