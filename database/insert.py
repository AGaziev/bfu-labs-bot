from data.config import db_connection_parameters as params
import psycopg2 as pg
from loguru import logger


class Inserter:
    def __init__(self) -> None:
        self.conn = pg.connect(**params)
        self.cursor = self.conn.cursor()
        self.conn.autocommit = True

    def insert_user(self, user_id: int, username: str, is_admin: bool = False, is_teacher: bool = False) -> bool:
        """Inserting user to database"""
        try:
            self.cursor.execute(
                """INSERT INTO user_data (user_id, username, is_admin, is_teacher)
                VALUES (%s, %s, %s, %s)""",
                (user_id, username, is_admin, is_teacher))
            logger.success(
                f'User [{username}] inserted into table [user_data]')
            return True

        except pg.Error as e:
            logger.error(f'{e}, user [{username}] not inserted')
            return False
