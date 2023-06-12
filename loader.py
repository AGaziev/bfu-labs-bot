from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config

bot = Bot(token=config.bot_token)
storage = MemoryStorage()
dispatcher = Dispatcher(bot, storage=storage)
