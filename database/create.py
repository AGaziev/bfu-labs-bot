from data.config import db_connection_parameters as params
import psycopg2 as pg
from loguru import logger


class Creator:
    def __init__(self) -> None:
        try:
            self.conn = pg.connect(**params)
            logger.info('Creator connected to database')

        except pg.Error as e:
            # connect to postgres database and create database for project
            logger.error(f'{e}, trying to create database')
            self.conn = pg.connect(
                user=params['user'],
                password=params['password'],
                host=params['host'],
                port=params['port'],
                database='postgres')
            self.cursor = self.conn.cursor()
            self._create_database()
            self.conn.close()

        finally:
            self.conn = pg.connect(**params)
            self.cursor = self.conn.cursor()
            self.conn.autocommit = True

    def _create_database(self) -> None:
        """Creating database with name from config.py"""
        try:
            self.cursor.execute(f'CREATE DATABASE {params["database"]}')
            self.conn.commit()
            logger.success(f'Database [{params["database"]}] created')

        except pg.Error as e:
            logger.error(f'{e}, database not created')

    def _create_table_user(self) -> None:
        """Creating table user, where will be stored all users\n
        Fields:\n
        user_id <int> - telegram user id\n
        username <str> - telegram username\n
        is_admin <bool> - is user admin\n
        is_teacher <bool> - is user teacher\n
        """
        try:
            self.cursor.execute(
                """CREATE TABLE user_data (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL UNIQUE,
                    username VARCHAR(255),
                    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
                    is_teacher BOOLEAN NOT NULL DEFAULT FALSE
                )""")
            logger.success('Table [user] created')

        except pg.Error as e:
            logger.error(f'{e}, table [user] not created')

    def _create_table_study_direction(self) -> None:
        """Creating table study_direction, where will be stored all study directions\n
        Fields:\n
        id <int> - direction id\n
        description <str> - direction description\n
        """
        try:
            self.cursor.execute(
                """CREATE TABLE study_direction (
                    id SERIAL PRIMARY KEY,
                    description VARCHAR(255) NOT NULL UNIQUE
                )""")
            logger.success('Table [study_direction] created')
        except pg.Error as e:
            logger.error(f'{e}, table [study_direction] not created')

    def _create_table_student(self) -> None:
        """Creating table student, where will be stored all students\n
        Fields:\n
        user_id <int> - telegram user id\n
        username <str> - telegram username\n
        direction_id <int> - direction id\n
        is_registered <bool> - is student registered\n
        created_at <timestamp> - when student info was created\n
        updated_at <timestamp> - when student info was updated\n
        """
        try:
            self.cursor.execute(
                """CREATE TABLE student (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL UNIQUE,
                    username VARCHAR(255),
                    direction_id SMALLINT,
                    is_registered BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user_data (user_id),
                    FOREIGN KEY (direction_id) REFERENCES study_direction (id)
                )""")
            logger.success('Table [student] created')

        except pg.Error as e:
            logger.error(f'{e}, table [student] not created')

    def _create_table_teacher(self) -> None:
        """Creating table teacher, where will be stored all teachers\n
        Fields:\n
        id <int> - teacher id\n
        user_id <int> - telegram user id\n
        firstname <str> - teacher's firstname\n
        lastname <str> - teacher's lastname\n
        course_description <str> - course description\n
        """
        try:
            self.cursor.execute(
                """CREATE TABLE teacher (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL UNIQUE,
                    firstname VARCHAR(255),
                    lastname VARCHAR(255),
                    course_description VARCHAR(255),
                    FOREIGN KEY (user_id) REFERENCES user_data (user_id)
                )""")
            logger.success('Table [teacher] created')

        except pg.Error as e:
            logger.error(f'{e}, table [teacher] not created')

    def _create_table_student_to_teacher(self) -> None:
        """Creating many to many table student_to_teacher, where will be stored all students and teachers\n
        Fields:\n
        teacher_id <int> - teacher's id\n
        student_id <int> - student's id\n
        """
        try:
            self.cursor.execute(
                """CREATE TABLE student_to_teacher (
                    id SERIAL PRIMARY KEY,
                    teacher_id INTEGER NOT NULL,
                    student_id INTEGER NOT NULL,
                    FOREIGN KEY (teacher_id) REFERENCES teacher (id),
                    FOREIGN KEY (student_id) REFERENCES student (id)
                )""")
            logger.success('Table [student_to_teacher] created')

        except pg.Error as e:
            logger.error(f'{e}, table [student_to_teacher] not created')

    def _create_table_lab_registry(self) -> None:
        """Creating table lab_registry, where will be stored all labs\n
        Fields:\n
        id <int> - lab id\n
        lab_owner_id <int> - id of teacher, who created lab\n
        lab_number <int> - lab number\n
        lab_description <str> - lab description\n
        """
        try:
            self.cursor.execute(
                """CREATE TABLE lab_registry (
                    id SERIAL PRIMARY KEY,
                    lab_owner_id INTEGER NOT NULL,
                    lab_number SMALLINT NOT NULL,
                    lab_description VARCHAR(255),
                    FOREIGN KEY (lab_owner_id) REFERENCES teacher (id)
                )""")
            logger.success('Table [lab_registry] created')

        except pg.Error as e:
            logger.error(f'{e}, table [lab_registry] not created')

    def _create_table_lab_tracker(self) -> None:
        """Creating table lab_tracker, where will be stored all labs\n
        Fields:\n
        id <int> - id of record\n
        student_id <int> - student's id\n
        lab_id <int> - lab id\n
        lab_status <str> - lab status\n
        """
        try:
            self.cursor.execute(
                """CREATE TABLE lab_tracker (
                    id SERIAL PRIMARY KEY,
                    student_id INTEGER NOT NULL,
                    lab_id SMALLINT NOT NULL,
                    lab_status VARCHAR(255),
                    FOREIGN KEY (student_id) REFERENCES student (id)
                )""")
            logger.success('Table [lab_tracker] created')

        except pg.Error as e:
            logger.error(f'{e}, table [lab_tracker] not created')

    def configure_tables(self) -> None:
        """Creating all tables"""
        self._create_table_user()
        self._create_table_study_direction()
        self._create_table_student()
        self._create_table_teacher()
        self._create_table_student_to_teacher()
        self._create_table_lab_registry()
        self._create_table_lab_tracker()
        logger.success('All tables created')

    def _drop_table(self, table_name: str) -> None:
        """Dropping table by name"""
        try:
            self.cursor.execute(f'DROP TABLE {table_name}')
            logger.warning(f'Table [{table_name}] dropped')

        except pg.Error as e:
            logger.error(f'{e}, table [{table_name}] not dropped')

    def _drop_all_tables(self) -> None:
        """Dropping all tables"""
        self._drop_table(table_name='student_to_teacher')
        self._drop_table(table_name='lab_tracker')
        self._drop_table(table_name='lab_registry')
        self._drop_table(table_name='teacher')
        self._drop_table(table_name='student')
        self._drop_table(table_name='study_direction')
        self._drop_table(table_name='user_data')
        logger.warning('All tables dropped')

    def reconfigure_tables(self) -> None:
        """Dropping all tables and creating them again"""
        self._drop_all_tables()
        self.configure_tables()


if __name__ == "__main__":
    Creator().reconfigure_tables()
