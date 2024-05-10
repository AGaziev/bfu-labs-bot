from aiogram.utils.exceptions import TelegramAPIError


async def set_commands(dp):
    from aiogram import types

    await dp.bot.set_my_commands(
        commands=[
            types.BotCommand(
                command='/menu',
                description='menu'),
        ])


async def on_startup(dp):
    import handlers
    import middlewares
    from loguru import logger
    import time

    middlewares.setup(dp)
    await set_commands(dp)
    handlers.setup(dp)

    @dp.errors_handler()
    async def error_handler(update: types.Update, exception: Exception):
        """
        Этот обработчик будет вызываться, когда произойдет ошибка во время обработки обновления.
        """
        if isinstance(exception, TelegramAPIError):
            logger.exception(f'Telegram API Error: {exception} \nUpdate: {update}')
            # Обработка конкретных ошибок API Telegram может быть здесь
        else:
            logger.exception(f'Update: {update} \n{exception}')

        # Возвращаем True, чтобы сообщить диспетчеру, что ошибка была обработана
        return True

    logger.add(f'logs/{time.strftime("%Y-%m-%d__%H-%M")}.log',
               level='DEBUG', rotation='500 MB', compression='zip')
    logger.success("[BOT STARTED SUCCESSFULLY]")

if __name__ == "__main__":
    # Launch
    from aiogram import executor, types
    from loader import dispatcher

    executor.start_polling(dispatcher, skip_updates=True,
                           on_startup=on_startup)
