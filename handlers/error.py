import traceback

from aiogram import types
from aiogram.utils.exceptions import TelegramAPIError
from loguru import logger
from data import configuration
from loader import bot


async def send_long_message(chat_id, text, part_size=4096):
    """
    Отправляет длинное сообщение частями.
    :param chat_id: ID чата для отправки сообщения.
    :param text: Текст сообщения для отправки.
    :param part_size: Максимальный размер одной части сообщения.
    """
    for part in range(0, len(text), part_size):
        await bot.send_message(chat_id, text[part:part+part_size])


async def error_handler(update: types.Update, exception: Exception):
    """
    Этот обработчик будет вызываться, когда произойдет ошибка во время обработки обновления.
    """
    # Получаем трейсбек в виде строки
    traceback_string = "".join(traceback.format_exception(None, exception, exception.__traceback__))
    error_message = f"Произошла ошибка: {exception} \nUpdate: {update}"
    traceback_message = f"Трейсбек: {traceback_string}"

    if isinstance(exception, TelegramAPIError):
        logger.exception(error_message)
        # Обработка конкретных ошибок API Telegram может быть здесь
    else:
        logger.exception(error_message)

    # Отправляем сообщение об ошибке администратору
    try:
        await bot.send_message(configuration.admin_log_errors_to, error_message)
        # Отправляем трейсбек отдельным сообщением, используя функцию для длинных сообщений
        await send_long_message(configuration.admin_log_errors_to, traceback_message)
    except Exception as e:
        logger.exception(f"Ошибка при отправке сообщения об ошибке администратору: {e}")

    # Возвращаем True, чтобы сообщить диспетчеру, что ошибка была обработана
    return True