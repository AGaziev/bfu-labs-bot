from io import BytesIO

from aiogram import types
from aiogram.dispatcher import FSMContext
import keyboards as kb
from middlewares import rate_limit
from aiogram.utils.markdown import hbold
from managers import GroupManager
from utils import states, Formatter
from managers import LabManager
from loguru import logger


async def show_undone_labs_for_post(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    # call.data sample: "group:1:student"
    group_id = callback_data["group_id"]
    group_name = await GroupManager.get_group_name_by_id(group_id)
    lab_stats = await LabManager.get_student_lab_stats(group_id, call.from_user.id)
    not_done_lab_names_with_number = {}
    if lab_stats:
        for lab in lab_stats.not_done:
            lab.cloud_link = await LabManager.get_lab_link_by_path(lab.cloud_link)
            not_done_lab_names_with_number[lab.number] = lab.description
    await call.message.edit_text(f"Какую лабораторную сдаем?\n"
                                 f"Введи число перед названием\n"
                                 f"{Formatter.list_lab_for_post(lab_stats.not_done)}",
                                 parse_mode=types.ParseMode.HTML,
                                 reply_markup=await kb.cancel_kb())
    await state.update_data(group_id=group_id)
    await state.update_data(group_name=group_name)
    await state.update_data(lab_names=not_done_lab_names_with_number or None)
    await states.Student.post_lab.show_undone_labs_for_post.set()


async def choose_lab(message: types.Message, state: FSMContext):
    # FIXME: add state or etc.
    # PROBLEM: if user send file before choosing lab, throws KeyError: 'lab_number'
    async with state.proxy() as posting_data:
        try:
            lab_number = int(message.text)
            name = posting_data['lab_names'][lab_number]
            posting_data['lab_name'] = name
            posting_data['lab_number'] = lab_number
            await message.answer(f"Вы собираетесь сдать лабораторную\n"
                                 f"{hbold(name)}\n"
                                 f"Если нет, то напишите еще раз число\n"
                                 f"Если да, то отправьте файл лабораторной",
                                 parse_mode=types.ParseMode.HTML)
        except (ValueError, KeyError):
            await message.answer("Такого номера нет, напишите еще раз число",
                                 reply_markup=await kb.cancel_kb())


async def wait_for_lab_file(message: types.Message, state: FSMContext):
    await states.Student.post_lab.upload_lab_file.set()
    try:
        io_file = BytesIO()
        await message.document.download(destination_file=io_file)
        io_file.seek(0)  # set pointer to the beginning of file
    except Exception as err:
        logger.error(f"Error while downloading file: {err}")
        await message.answer("Произошла ошибка при загрузке файла, попробуйте еще раз")
        return
    else:
        await state.update_data(io_file=io_file)
        await state.update_data(file_extension=message.document.file_name.split(".")[-1])
        async with state.proxy() as posting_data:
            lab_file = types.InputFile(
                io_file, filename=message.document.file_name)
            await message.answer_document(
                lab_file,
                caption=f"Вы собираетесь сдать лабораторную номер {posting_data['lab_number']}\n"
                        f"{hbold(posting_data['lab_name'])}\n"
                        f"Название файла: {hbold(lab_file.filename)}\n"
                        f"Если не тот файл, пришлите снова",
                reply_markup=await kb.confirmation_kb(),
                parse_mode=types.ParseMode.HTML
            )


async def end_posting_lab(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_caption(f"{call.message.caption}\n{hbold('Успешно подтверждено!')}",
                                    reply_markup=None,
                                    parse_mode=types.ParseMode.HTML)
    async with state.proxy() as posting_data:
        await GroupManager.post_lab_from_student(group_name=posting_data['group_name'],
                                                 telegram_id=call.from_user.id,
                                                 lab_number=posting_data['lab_number'],
                                                 lab_file=posting_data['io_file'],
                                                 file_extension=posting_data['file_extension'])
        await call.message.answer("Ваша лабораторная у преподавателя!")
    await state.finish()
