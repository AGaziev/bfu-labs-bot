from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import configuration

bot = Bot(token=configuration.bot_token)
storage = MemoryStorage()
dispatcher = Dispatcher(bot, storage=storage)
