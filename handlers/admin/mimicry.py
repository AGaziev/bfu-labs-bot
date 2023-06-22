# in this module we don't need to use is_admin wrapper because no one can call this handlers except admin
# because of the callback query handler


from aiogram import types

import keyboards as kb
from middlewares import rate_limit


@rate_limit(limit=3)
async def mimic_a_student(call: types.CallbackQuery):
    await call.message.edit_text(
        "Вы выбрали режим имитации студента")
    await call.message.edit_reply_markup(reply_markup=await kb.student_menu_kb(telegram_id=call.from_user.id))


@rate_limit(limit=3)
async def mimic_a_teacher(call: types.CallbackQuery):
    await call.message.edit_text(
        "Вы выбрали режим имитации преподавателя")
    await call.message.edit_reply_markup(reply_markup=await kb.teacher_menu_kb())
