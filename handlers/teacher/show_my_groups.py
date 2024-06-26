from aiogram import types
from aiogram.dispatcher import FSMContext
import keyboards as kb
from managers import GroupManager
from managers.db import DatabaseManager
from middlewares import rate_limit
from utils import states


@rate_limit(limit=3)
async def show_my_groups(call: types.CallbackQuery):
    """Show groups for teacher"""
    groups = GroupManager.get_groups_for_teacher(telegram_id=call.from_user.id)
    if not groups:
        await call.message.edit_text("У вас нет групп, создайте новую",
                                     reply_markup=await kb.teacher_menu_kb(show_all_groups_button=False))
        return

    await call.message.edit_text("Отображаю ваши группы",
                                 reply_markup=await kb.get_groups_kb(group_names_and_ids=groups, role="teacher"))
    await states.TeacherState.show_my_groups.set()
