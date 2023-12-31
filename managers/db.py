from openpyxl.pivot.cache import GroupMembers
from psycopg2 import IntegrityError

from database.inserter import Creator
from utils.models import *
from handlers.error import error_handling

class DatabaseManager(Creator):
    pass