from loader import bot


def error_handling(exception: Exception, errortext, trace=None):
    bot.send_message(chat_id=292667494,
                     text=str(exception) + "\n" + errortext + "\n" + trace)
