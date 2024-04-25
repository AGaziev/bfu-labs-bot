import io

from aiogram import types
from aiogram.dispatcher import FSMContext
import keyboards as kb
from middlewares import rate_limit
from utils import states
from managers import GroupManager

@rate_limit(limit=3)
async def show_my_groups(call: types.CallbackQuery, state: FSMContext):
    """Show groups for student"""
    groups = GroupManager.get_groups_for_student(call.from_user.id)
    if not groups:
        await call.message.answer("У вас нет групп, подключитесь к какой-нибудь", reply_markup=await kb.student_menu_kb())
        return

    await call.message.edit_text("Отображаю ваши группы", reply_markup=await kb.get_groups_kb(group_names_and_ids=groups,
                                                                                              role="student"))
    await states.Student.show_groups.set()
