from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified
from aiogram.utils.markdown import hbold, hitalic, hlink
import keyboards as kb
from middlewares import rate_limit
from utils import states
from managers import GroupManager, database_manager


@rate_limit(limit=3)
async def show_my_groups(call: types.CallbackQuery, state: FSMContext):
    """Show groups for teacher"""
    groups = await database_manager.select_group_ids_and_names_owned_by_telegram_id(telegram_id=call.from_user.id)
    if not groups:
        await call.message.answer("У вас нет групп, создайте новую", reply_markup=await kb.teacher_kb())
        return

    await call.message.edit_text("Отображаю ваши группы", reply_markup=await kb.get_groups_kb(group_names_and_ids=groups))
