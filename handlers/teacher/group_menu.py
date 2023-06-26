from aiogram import types
from aiogram.dispatcher import FSMContext
import keyboards as kb
from middlewares import rate_limit
from aiogram.utils.markdown import hbold, hitalic
from managers import database_manager, GroupManager
from utils import states


async def teacher_group_menu(call: types.CallbackQuery, state: FSMContext):
    # call.data sample: "group:1:teacher"
    group_id = call.data.split(":")[1]
    group_name = await database_manager.select_group_name_by_group_id(group_id=group_id)
    group_info = await GroupManager.get_group_info(group_id=group_id, group_name=group_name)

    def percent_hitalic(x: int, y: int) -> str:
        percent = f"{round(x/y*100, 2)}%" if y else "0%"
        return hitalic(percent)

    await call.message.edit_text(f"Вы выбрали группу\n{hbold(group_name)}\n\n"
                                 f"📊   Статистика:\n"
                                 f"👥   Всего студентов в группе: {hbold(group_info.students_at_all)}\n"
                                 f"✅   Зарегистрировано: {hbold(group_info.registered_members_count or 0)} — {percent_hitalic(group_info.registered_members_count, group_info.students_at_all)}\n"
                                 f"❌   Не зарегистрировано: {hbold(group_info.unregistered_members_count or 0)} — {percent_hitalic(group_info.unregistered_members_count, group_info.students_at_all)}\n\n"
                                 f"📝   Выдано лабораторных работ: {hbold(group_info.lab_condition_files_count or 0)}\n"
                                 f"📥   Сдано на проверку: {hbold(group_info.labs_at_all or 0)}\n"
                                 f"👀   Ожидают проверки: {hbold(group_info.not_checked_labs_count or 0)} — {percent_hitalic(group_info.not_checked_labs_count, group_info.labs_at_all)}\n"
                                 f"🏆   Сданы: {hbold(group_info.passed_labs_count or 0)} — {percent_hitalic(group_info.passed_labs_count, group_info.labs_at_all)}\n"
                                 f"👎   Не сданы: {hbold(group_info.rejected_labs_count or 0)} — {percent_hitalic(group_info.rejected_labs_count, group_info.labs_at_all)}\n",
                                 reply_markup=await kb.teacher_group_menu_kb(group_id=group_id),
                                 parse_mode=types.ParseMode.HTML)
    await state.update_data(group_name=group_name)
    await state.update_data(group_id=group_id)
    await states.TeacherState.group_menu.set()
