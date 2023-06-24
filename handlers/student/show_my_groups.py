import io

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified
from aiogram.utils.markdown import escape_md

import keyboards
from data import config
import keyboards as kb
from middlewares import rate_limit
from utils import states
from managers import GroupManager

@rate_limit(limit=3)
async def show_my_groups(call: types.CallbackQuery, state: FSMContext):
    """Show groups for student"""
    groups = await GroupManager.get_groups_for_student(call.from_user.id)
    print(groups)
    if not groups:
        await call.message.answer("У вас нет групп, подключитесь к какой-нибудь", reply_markup=await kb.student_menu_kb())
        return

    await call.message.edit_text("Отображаю ваши группы", reply_markup=await kb.get_groups_kb(group_names_and_ids=groups,
                                                                                              type="student"))
