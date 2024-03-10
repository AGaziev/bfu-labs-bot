from loader import bot


async def error_handling(exception: Exception, errortext, trace=None):
    await bot.send_message(chat_id=292667494,
                     text=str(exception) + "\n" + errortext + "\n" + (trace if trace else ""))
