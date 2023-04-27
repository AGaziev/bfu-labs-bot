from .Throttling import *
from loader import dispatcher


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
