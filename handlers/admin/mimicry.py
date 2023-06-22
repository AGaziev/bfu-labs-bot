# in this module we don't need to use is_admin wrapper because no one can call this handlers except admin
# because of the callback query handler


from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards as kb
from middlewares import rate_limit

from utils.states import TeacherState, Student


@rate_limit(limit=3)
async def mimic_a_student(call: types.CallbackQuery, state: FSMContext):
    if state:
        await state.finish()

    await call.message.edit_text(
        "Вы выбрали режим имитации студента")
    await call.message.edit_reply_markup(reply_markup=await kb.student_menu_kb(telegram_id=call.from_user.id))
    await Student.start.set()


@rate_limit(limit=3)
async def mimic_a_teacher(call: types.CallbackQuery, state: FSMContext):
    if state:
        await state.finish()

    await call.message.edit_text(
        "Вы выбрали режим имитации преподавателя")
    await call.message.edit_reply_markup(reply_markup=await kb.teacher_menu_kb())
    await TeacherState.start.set()
