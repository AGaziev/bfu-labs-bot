"""Finite state machine states module
    """

from aiogram.dispatcher.filters.state import State, StatesGroup


class registrator(StatesGroup):
    name = State()
