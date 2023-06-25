from aiogram import types
from aiogram.dispatcher import FSMContext
import keyboards as kb
from middlewares import rate_limit
from aiogram.utils.markdown import hbold
from managers import database_manager
from utils import states


async def teacher_group_menu(call: types.CallbackQuery, state: FSMContext):
    # call.data sample: "group:1:teacher"
    group_name = await database_manager.select_group_name_by_group_id(group_id=call.data.split(":")[1])
    await call.message.edit_text(f"Вы выбрали группу\n{hbold(group_name)}",
                                 reply_markup=await kb.teacher_group_menu_kb(group_id=call.data.split(":")[1]),
                                 parse_mode=types.ParseMode.HTML)
    await state.update_data(group_name=group_name)
    await states.TeacherState.group_menu.set()
