from aiogram import types
from aiogram.dispatcher import FSMContext
import keyboards as kb
from middlewares import rate_limit
from managers import database_manager
from utils import states


@rate_limit(limit=3)
async def show_my_groups(call: types.CallbackQuery, state: FSMContext):
    """Show groups for teacher"""
    groups = await database_manager.select_group_ids_and_names_owned_by_telegram_id(telegram_id=call.from_user.id)
    if not groups:
        await call.message.edit_text("У вас нет групп, создайте новую", reply_markup=await kb.teacher_menu_kb())
        return

    await call.message.edit_text("Отображаю ваши группы", reply_markup=await kb.get_groups_kb(group_names_and_ids=groups, role="teacher"))
    await states.TeacherState.show_my_groups.set()
