from .insert import Inserter
from .select import Selector
from .update import Updater


class DbManager(Inserter, Selector, Updater):
    pass
