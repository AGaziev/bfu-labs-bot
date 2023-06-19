
from aiogram import types
from aiogram.dispatcher import FSMContext
from middlewares import rate_limit


@rate_limit(limit=5)
async def cancel_operation(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Операция отменена")
    await state.finish()
