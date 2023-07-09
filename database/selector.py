from .database_connector import DatabaseConnector
from loguru import logger
from typing import Any
import utils.models as models
from utils.enums import Blocked
from datetime import datetime


class Selector(DatabaseConnector):
    """
    Class for selecting data from database\n
    """

    def __init__(self) -> None:
        super().__init__()
        logger.debug("Selector for database object was initialized")

    async def select_one_row_from_table(self, table_name: str, column_name: str, value: str) -> Any:
        """
        Selects one row from table by column name and value\n
        USE IT ONLY IF THIS CLASS HAS NO METHOD FOR YOUR QUERY\n

        Args:
            table_name (str): name of table to select from
            column_name (str): name of column to select from
            value (str): value of column to select from

        Returns:
            Any: resutracker of query execution
        """
        query = f"""--sql
        SELECT * FROM {table_name}
        WHERE {column_name} = '{value}';
        """
        resutracker = await self._execute_query_with_returning_one_row(query)
        if resutracker is False:
            logger.error(
                f"Error while selecting from {table_name} with {column_name} = {value}")
            return None
        else:
            logger.success(f"Selected from {table_name} successfully")
            return resutracker[0]

    async def select_all_rows_from_table(self, table_name: str, column_name: str, value: str) -> Any:
        """
        Selects all rows from table by column name and value\n
        USE IT ONLY IF THIS CLASS HAS NO METHOD FOR YOUR QUERY\n

        Args:
            table_name (str): name of table to select from
            column_name (str): name of column to select from
            value (str): value of column to select from

        Returns:
            Any: resutracker of query execution
        """
        query = f"""--sql
        SELECT * FROM {table_name}
        WHERE {column_name} = '{value}';
        """
        resutracker = await self._execute_query(query)
        if resutracker is False:
            logger.error(
                f"Error while selecting from {table_name} with {column_name} = {value}")
            return None
        else:
            logger.success(f"Selected from {table_name} successfully")
            return resutracker

    async def check_is_user_exist(self, user_id: int) -> bool:
        """
        Check if user exists in database in table users\n
        """
        query = f"""--sql
        SELECT EXISTS(SELECT 1 FROM users WHERE telegram_id = {user_id});
        """
        resutracker = await self._execute_query_with_returning_one_row(query)
        if resutracker is False:
            logger.error(
                f"Error while checking if user exists; user_id = {user_id}")
            return False
        else:
            logger.success(
                f"Checked if user exists successfully; user_id = {user_id}")
            return resutracker[0]

    async def select_group_id_by_group_name(self, group_name: str) -> int | None:
        query = f"""--sql
        SELECT id FROM education_group
        WHERE group_name = '{group_name}';
        """
        resutracker = await self._execute_query_with_returning_one_row(query)
        if resutracker is False:
            logger.error(
                f"Error while selecting from education_group with group_name = {group_name}")
            return None
        else:
            logger.success(
                f"Selected group_id from education_group successfully; group_name = {group_name} with id = {resutracker[0]}")
            return resutracker[0]

    async def select_group_name_by_group_id(self, group_id: int) -> str | None:
        query = f"""--sql
        SELECT group_name FROM education_group
        WHERE id = {group_id};
        """
        resutracker = await self._execute_query_with_returning_one_row(query)
        if resutracker is False:
            logger.error(
                f"Error while selecting from education_group with group_id = {group_id}")
            return None
        else:
            logger.success(
                f"Selected group_name from education_group successfully; group_id = {group_id} with name = {resutracker[0]}")
            return resutracker[0]

    async def select_group_owner_id_by_group_id(self, group_id: int) -> int | None:
        query = f"""--sql
        SELECT owner_id FROM education_group
        WHERE id = {group_id};
        """
        resutracker = await self._execute_query_with_returning_one_row(query)
        if resutracker is False:
            logger.error(
                f"Error while selecting from education_group with group_id = {group_id}")
            return None
        else:
            logger.success(
                f"Selected group_owner_id from education_group successfully; group_id = {group_id} with id = {resutracker[0]}")
            return resutracker[0]

    async def check_is_user_teacher(self, user_id: int) -> bool:
        """
        Returns:
            bool: bool value if user_id (telegram_id column) in teacher table
        """
        query = f"""--sql
        SELECT EXISTS(SELECT 1 FROM teacher WHERE telegram_id = {user_id});
        """
        resutracker = await self._execute_query_with_returning_one_row(query)
        if resutracker is False:
            logger.error(
                f"Error while checking if user is teacher; user_id = {user_id}")
            return False
        else:
            logger.success(
                f"Checked if user is teacher successfully; user_id = {user_id}")
            return resutracker[0]

    async def select_registered_members_from_group(self, group_id: int, is_blocked: Blocked) -> tuple[int, ...]:
        query = f"""--sql
        SELECT telegram_id FROM registered_members
        WHERE member_id IN (SELECT member_id FROM education_group_members
        WHERE group_id = {group_id})
        AND telegram_id IN (SELECT telegram_id FROM users
        WHERE is_blocked IN ({is_blocked.value}));
        """

        resutracker = await self._execute_query(query)
        if resutracker is False:
            logger.error(
                f"Error while selecting registered members from group; group_id = {group_id}")
            return tuple()
        else:
            logger.success(
                f"Selected registered members from group successfully; group_id = {group_id}")
            return tuple([iterable[0] for iterable in resutracker])

    async def _select_group_owner_by_group_id(self, group_id: int) -> tuple[str]:
        """
        Returns:
            list[str]: list of group owner first_name, last_name, patronymic
        """
        query = f"""--sql
        SELECT first_name, last_name, patronymic FROM teacher
        WHERE telegram_id = (SELECT owner_id FROM education_group
        WHERE id = {group_id});
        """

        resutracker = await self._execute_query_with_returning_one_row(query)
        if resutracker is False:
            logger.error(
                f"Error while selecting group owner by group_id; group_id = {group_id}")
            raise AttributeError(
                f"Group owner not found; group_id = {group_id}")
        else:
            logger.success(
                f"Selected group owner by group_id successfully; group_id = {group_id}; owner = {resutracker}")
            return resutracker[0], resutracker[1], resutracker[2] if len(resutracker) == 3 else None

    async def _select_owner_username_by_group_id(self, group_id: int) -> str:
        query = f"""--sql
        SELECT username FROM users
        WHERE telegram_id = (SELECT owner_id FROM education_group
        WHERE id = {group_id});
        """

        resutracker = await self._execute_query_with_returning_one_row(query)
        if resutracker is False:
            logger.error(
                f"Error while selecting owner username by group_id; group_id = {group_id}")
            raise AttributeError(
                f"Owner username not found; group_id = {group_id}")
        else:
            logger.success(
                f"Selected owner username by group_id successfully; group_id = {group_id}; username = {resutracker[0]}")
            return resutracker[0]

    async def select_teacher_by_group_id(self, group_id: int) -> models.Teacher:
        """
        Returns:
            Teacher: Teacher object, representing teacher of group with field names:
                first_name, last_name, patronymic, username
        """
        teacher = models.Teacher()
        teacher.firstname, teacher.lastname, teacher.patronymic = await self._select_group_owner_by_group_id(
            group_id)
        teacher.username = await self._select_owner_username_by_group_id(
            group_id)
        return teacher

    async def select_group_name_by_group_id(self, group_id: int) -> str | None:
        query = f"""--sql
        SELECT group_name FROM education_group
        WHERE id = {group_id};
        """
        resutracker = await self._execute_query_with_returning_one_row(query)
        if resutracker is False:
            logger.error(
                f"Error while selecting group_name by group_id; group_id = {group_id}")
            return None
        else:
            logger.success(
                f"Selected group_name by group_id successfully; group_id = {group_id}; group_name = {resutracker[0]}")
            return resutracker[0]

    async def select_member_firstname_and_lastname_by_telegram_id_and_group_id(self, telegram_id: int, group_id: int) -> tuple[str, str] | None:
        query = f"""--sql
        SELECT first_name, last_name FROM education_group_members
        WHERE member_id = (SELECT member_id FROM registered_members
        WHERE user_id = {telegram_id})
        AND group_id = {group_id};
        """
        resutracker = await self._execute_query_with_returning_one_row(query)
        if resutracker is False:
            logger.error(
                f"Error while selecting member firstname and lastname by telegram_id and group_id; telegram_id = {telegram_id}; group_id = {group_id}")
            return None
        else:
            logger.success(
                f"Selected member firstname and lastname by telegram_id and group_id successfully; telegram_id = {telegram_id}; group_id = {group_id}; firstname = {resutracker[0]}; lastname = {resutracker[1]}")
            return resutracker

    async def select_teacher_credentials_by_telegram_id(self, telegram_id: int) -> models.Teacher:
        """
        Returns:
            Teacher: Teacher object, representing teacher with field names:
                first_name, last_name, patronymic, WITHOUT username
        """
        query = f"""--sql
        SELECT first_name, last_name, patronymic FROM teacher
        WHERE telegram_id = {telegram_id};
        """
        resutracker = await self._execute_query_with_returning_one_row(query)
        if resutracker is False:
            logger.error(
                f"Error while selecting teacher credentials by telegram_id; telegram_id = {telegram_id}")
            raise AttributeError(
                f"Teacher credentials not found; telegram_id = {telegram_id}")
        else:
            logger.success(
                f"Selected teacher credentials by telegram_id successfully; telegram_id = {telegram_id}; credentials = {resutracker}")
            teacher = models.Teacher()
            teacher.firstname, teacher.lastname, teacher.patronymic = resutracker
            return teacher

    async def select_group_ids_and_names_owned_by_telegram_id(self, telegram_id: int) -> list[tuple[int, str]]:
        query = f"""--sql
        SELECT id, group_name FROM education_group
        WHERE owner_id = {telegram_id};
        """
        resutracker = await self._execute_query(query)
        if resutracker is False:
            logger.error(
                f"Error while selecting group ids and names owned by telegram_id; telegram_id = {telegram_id}")
            raise AttributeError(
                f"Groups not found; telegram_id = {telegram_id}")
        else:
            logger.success(
                f"Selected group ids and names owned by telegram_id successfully; telegram_id = {telegram_id}; groups = {resutracker}")
            return resutracker

    async def select_telegram_id_by_username(self, username: str) -> int | None:
        query = f"""--sql
        SELECT telegram_id FROM users
        WHERE username = '{username}';
        """
        resutracker = await self._execute_query_with_returning_one_row(query)
        if resutracker in (False, None):
            logger.error(
                f"Error while selecting telegram_id by username; username = {username}")
            return None
        else:
            logger.success(
                f"Selected telegram_id by username successfully; username = {username}; telegram_id = {resutracker[0]}")
            return resutracker[0]

    async def select_student_groups_names_with_id(self, telegram_id: int) -> list[tuple[int, str]]:
        query = f"""--sql
        SELECT group_id, eg.group_name FROM registered_members rm
        LEFT JOIN education_group_members egm ON rm.member_id = egm.member_id
        LEFT JOIN education_group eg ON egm.group_id = eg.id
        WHERE telegram_id={telegram_id};
        """
        resutracker = await self._execute_query(query)
        if resutracker is False:
            logger.error(
                f"Error while selecting user groups with id; telegram_id = {telegram_id}")
            return []
        else:
            logger.success(
                f"Selected user groups with id successfully; telegram_id = {telegram_id}; resutracker = {resutracker}")
            return resutracker

    async def check_is_group_exists_by_group_name(self, group_name: str) -> bool:
        query = f"""--sql
        SELECT EXISTS(SELECT * FROM education_group
        WHERE group_name = '{group_name}');
        """
        resutracker = await self._execute_query_with_returning_one_row(query)
        if resutracker is False:
            logger.error(
                f"Error while checking is group exists by group_name; group_name = {group_name}")
            return False
        else:
            logger.success(
                f"Checked is group exists by group_name successfully; group_name = {group_name}; resutracker = {resutracker[0]}")
            return resutracker[0]

    async def select_unregistered_users_from_group(self, group_name: str) -> list[tuple[int, str]] | None:
        group_id = await self.select_group_id_by_group_name(group_name)

        query = f"""--sql
        SELECT education_group_members.member_id as id, credentials
        FROM education_group_members
        LEFT JOIN registered_members
            ON education_group_members.member_id = registered_members.member_id
        WHERE group_id = {group_id} AND telegram_id IS NULL
        """
        resutracker = await self._execute_query(query)
        if resutracker is False:
            logger.error(
                f"Error while selecting unregistered members from group; group_name = {group_name}")
            return None
        else:
            logger.success(
                f"Selected unregistered members from group successfully; group_name = {group_name}; resutracker = {resutracker}")
            return resutracker

    async def select_students_labs_with_status_in_group(self, group_id: str, telegram_id: int) -> list[tuple[int, int, str, str]] | None:
        query = f"""--sql
        SELECT lb.id as id,
               lb.lab_number as number,
               lb.lab_description as descr,
               lb.cloud_link as path, -- TODO: REFACTOR AFTER CHANGING NAME OF COLUMN 
               coalesce((SELECT status_name
                         FROM lab_status_type
                         WHERE id=tracker.status_id),
                         'Не сдано') as status -- Если status_id null (не сдано) получаем "Не сдано"
        FROM lab_registry lb
        LEFT JOIN lab_tracker tracker ON lb.id = tracker.lab_id
        WHERE group_id = {group_id}
        AND member_id = (SELECT member_id
                         FROM registered_members
                         WHERE group_id = {group_id} AND telegram_id = {telegram_id})
        """
        resutracker = await self._execute_query(query)
        if resutracker is False:
            logger.error(
                f"Error while selecting student's labs with status in group; group_name = {group_id}, telegram_id={telegram_id}")
            return None
        else:
            logger.success(
                f"Selected student's labs with status in group successfully; group_name = {group_id}, telegram_id={telegram_id}; resutracker = {resutracker}")
            return resutracker

    async def select_undone_group_labs_for_student(self, group_id: str, telegram_id: int) -> list[tuple[int, int, str, str, int, datetime]] | None:
        query = f"""--sql
        SELECT *
        FROM lab_registry
        WHERE group_id = {group_id}
        AND id NOT IN (SELECT lab_id
                       FROM lab_tracker
                       WHERE group_id = {group_id}
                       AND member_id IN (SELECT member_id
                                        FROM registered_members
                                        WHERE telegram_id = {telegram_id}
                                        AND group_id = {group_id}))
        """
        resutracker = await self._execute_query(query)
        if resutracker is False:
            logger.error(
                f"Error while selecting undone group's labs for student; group_id = {group_id}, telegram_id={telegram_id}")
            return None
        else:
            logger.success(
                f"Selected undone group's labs for student successfully; group_id = {group_id}, telegram_id={telegram_id}; resutracker = {resutracker}")
            return resutracker

    async def select_lab_condition_files_from_group(self, group_id: int) -> list[tuple[int, str, str]]:
        """selects lab id, lab description (file name) and cloud link to file by group_id
        Args:
            group_id (int): group id in database

        Returns:
            list[tuple[int,str,str]]: list[tuple[lab_id:int, lab_description:str, cloud_link:str]]
        """
        query = f"""--sql
        SELECT id, lab_description, cloud_link
        FROM lab_registry
        WHERE group_id = {group_id}
        """
        resutracker = await self._execute_query(query)
        if resutracker is False:
            logger.error(
                f"Error while selecting lab condition files from group; group_id = {group_id}")
            return []
        else:
            logger.success(
                f"Selected lab condition files from group successfully; group_id = {group_id}; resutracker = {resutracker}")
            return resutracker

    async def select_labs_with_status_count_from_group(self, group_id: int, status: str) -> int:
        """selects count of labs with status from group

            Args:
                group_id (int): group id in database
                status (str): status name in table lab_status_type

            Returns:
                int: count of labs with status from group
        """
        query = f"""--sql
        SELECT COUNT(*)
        FROM lab_tracker
        WHERE member_id IN (SELECT member_id
                            FROM education_group_members
                            WHERE group_id = {group_id})
        AND status_id = (SELECT id
                        FROM lab_status_type
                        WHERE status_name = '{status}');
        """
        resutracker = await self._execute_query_with_returning_one_row(query)
        if resutracker is False:
            logger.error(
                f"Error while selecting passed labs count from group; group_id = {group_id}")
            return 0
        else:
            logger.success(
                f"Selected passed labs count from group successfully; group_id = {group_id}; resutracker = {resutracker[0]}")
            return resutracker[0]

    async def select_all_labs_count_from_group(self, group_id: int) -> int:
        query = f"""--sql
        SELECT COUNT(*)
        FROM lab_tracker
        WHERE member_id IN (SELECT member_id
                            FROM education_group_members
                            WHERE group_id = {group_id});
        """
        resutracker = await self._execute_query_with_returning_one_row(query)
        if resutracker is False:
            logger.error(
                f"Error while selecting all labs count from group; group_id = {group_id}")
            return 0
        else:
            logger.success(
                f"Selected all labs count from group successfully; group_id = {group_id}; resutracker = {resutracker[0]}")
            return resutracker[0]

    async def select_first_unchecked_lab_in_group(self, group_id: int) -> models.LaboratoryWork:
        """selects first not checked lab in group

        Args:
            group_id (int): group id in database

        Returns:
            models.LaboratoryWork: laboratory work model
        """
        query = f"""--sql
        SELECT tracker.id,
                registry.lab_number,
                registry.lab_description,
                registry.cloud_link,
                egm.credentials
        FROM lab_tracker tracker
        LEFT JOIN lab_registry registry ON tracker.lab_id = registry.id
        LEFT JOIN education_group_members egm ON tracker.member_id = egm.member_id
        WHERE egm.group_id = {group_id}
        AND tracker.status_id = (SELECT id
                            FROM lab_status_type
                            WHERE status_name = 'Не проверено')
        ORDER BY tracker.id ASC
        LIMIT 1;
        """

        result = await self._execute_query(query)
        if result is False:
            logger.error(
                f"Error while selecting first not checked lab in group; group_id = {group_id}")
            return models.LaboratoryWork()
        else:
            logger.success(
                f"Selected first not checked lab in group successfully; group_id = {group_id}; result = {result}")
            lab = models.LaboratoryWork()
            lab.id_ = result[0]['id']
            lab.number = result[0]['lab_number']
            lab.description = result[0]['lab_description']
            lab.cloud_link = result[0]['cloud_link']
            lab.member_credentials = result[0]['credentials']
            return lab

    async def select_next_unchecked_lab_in_group(self, group_id: int, current_lab_id: int) -> models.LaboratoryWork:
        """selects next unchecked lab in group

        Args:
            group_id (int): group id in database
            current_lab_id (int): current lab id in database

        Returns:
            models.LaboratoryWork: laboratory work model
        """
        query = f"""--sql
        SELECT tracker.id,
                registry.lab_number,
                registry.lab_description,
                registry.cloud_link,
                egm.credentials
        FROM lab_tracker tracker
        LEFT JOIN lab_registry registry ON tracker.lab_id = registry.id
        LEFT JOIN education_group_members egm ON tracker.member_id = egm.member_id
        WHERE egm.group_id = {group_id}
        AND tracker.status_id = (SELECT id
                            FROM lab_status_type
                            WHERE status_name = 'Не проверено')
        AND tracker.id > {current_lab_id}
        ORDER BY tracker.id ASC
        LIMIT 1;
        """

        result = await self._execute_query(query)
        if result is False:
            logger.error(
                f"Error while selecting next unchecked lab in group; group_id = {group_id}, current_lab_id = {current_lab_id}")
            return models.LaboratoryWork()
        else:
            logger.success(
                f"Selected next unchecked lab in group successfully; group_id = {group_id}, current_lab_id = {current_lab_id}; result = {result}")
            lab = models.LaboratoryWork()
            lab.id_ = result[0]['id']
            lab.number = result[0]['lab_number']
            lab.description = result[0]['lab_description']
            lab.cloud_link = result[0]['cloud_link']
            lab.member_credentials = result[0]['credentials']
            return lab

    async def select_previous_unchecked_lab_in_group(self, group_id: int, current_lab_id: int) -> models.LaboratoryWork:
        """selects previous unchecked lab in group

        Args:
            group_id (int): group id in database
            current_lab_id (int): current lab id in database

        Returns:
            models.LaboratoryWork: laboratory work model
        """
        query = f"""--sql
        SELECT tracker.id,
                registry.lab_number,
                registry.lab_description,
                registry.cloud_link,
                egm.credentials
        FROM lab_tracker tracker
        LEFT JOIN lab_registry registry ON tracker.lab_id = registry.id
        LEFT JOIN education_group_members egm ON tracker.member_id = egm.member_id
        WHERE egm.group_id = {group_id}
        AND tracker.status_id = (SELECT id
                            FROM lab_status_type
                            WHERE status_name = 'Не проверено')
        AND tracker.id < {current_lab_id}
        ORDER BY tracker.id ASC
        LIMIT 1;
        """

        result = await self._execute_query(query)
        if result is False:
            logger.error(
                f"Error while selecting previous unchecked lab in group; group_id = {group_id}, current_lab_id = {current_lab_id}")
            return models.LaboratoryWork()
        else:
            logger.success(
                f"Selected previous unchecked lab in group successfully; group_id = {group_id}, current_lab_id = {current_lab_id}; result = {result}")
            lab = models.LaboratoryWork()
            lab.id_ = result[0]['id']
            lab.number = result[0]['lab_number']
            lab.description = result[0]['lab_description']
            lab.cloud_link = result[0]['cloud_link']
            lab.member_credentials = result[0]['credentials']
            return lab

    async def is_exist_next_unchecked_lab_in_group(self, lab_id: int) -> bool:
        """checks if next unchecked lab exists in group

        Args:
            lab_id (int): current lab id in database

        Returns:
            bool: True if exists, False if not
        """
        query = f"""--sql
            SELECT EXISTS(
                SELECT tracker.id
                FROM lab_tracker tracker
                LEFT JOIN lab_registry registry ON tracker.lab_id = registry.id
                LEFT JOIN education_group_members egm ON tracker.member_id = egm.member_id
                WHERE egm.group_id = (
                    SELECT egm.group_id
                    FROM  education_group_members egm
                    WHERE egm.member_id = (
                        SELECT tracker.member_id
                        FROM lab_tracker tracker
                        WHERE tracker.id = {lab_id}
                    )
                )
                AND tracker.status_id = (
                    SELECT lst.id
                    FROM lab_status_type lst
                    WHERE lst.status_name = 'Не проверено'
                )
                AND tracker.id > {lab_id}
                ORDER BY tracker.id ASC
                LIMIT 1
            );
        """

        result = await self._execute_query_with_returning_one_row(query)
        if result is False:
            logger.error(
                f"Error while checking if next unchecked lab exists in group; lab_id = {lab_id}")
            return False
        else:
            logger.success(
                f"Checked if next unchecked lab exists in group successfully; lab_id = {lab_id}; result = {result[0]}")
            return result[0]

    async def is_exist_previous_unchecked_lab_in_group(self, lab_id: int) -> bool:
        """checks if previous unchecked lab exists in group

        Args:
            lab_id (int): current lab id in database

        Returns:
            bool: True if exists, False if not
        """
        query = f"""--sql
            SELECT EXISTS(
                SELECT tracker.id
                FROM lab_tracker tracker
                LEFT JOIN lab_registry registry ON tracker.lab_id = registry.id
                LEFT JOIN education_group_members egm ON tracker.member_id = egm.member_id
                WHERE egm.group_id = (
                    SELECT egm.group_id
                    FROM  education_group_members egm
                    WHERE egm.member_id = (
                        SELECT tracker.member_id
                        FROM lab_tracker tracker
                        WHERE tracker.id = {lab_id}
                    )
                )
                AND tracker.status_id = (
                    SELECT lst.id
                    FROM lab_status_type lst
                    WHERE lst.status_name = 'Не проверено'
                )
                AND tracker.id < {lab_id}
                ORDER BY tracker.id ASC
                LIMIT 1
            );
        """

        result = await self._execute_query_with_returning_one_row(query)
        if result is False:
            logger.error(
                f"Error while checking if previous unchecked lab exists in group; lab_id = {lab_id}")
            return False
        else:
            logger.success(
                f"Checked if previous unchecked lab exists in group successfully; lab_id = {lab_id}; result = {result[0]}")
            return result[0]

    async def select_student_credentials(self, telegram_id: int, group_name: str) -> str:
        """selects student credentials

        Args:
            telegram_id (int): telegram id of student
            group_name (str): group name

        Returns:
            str: student credentials
        """
        query = f"""--sql
        SELECT credentials
        FROM education_group_members
        WHERE group_id = (SELECT id
                        FROM education_group
                        WHERE group_name = '{group_name}')
        AND member_id IN (SELECT member_id
                        FROM registered_members
                        WHERE telegram_id = {telegram_id});
        """

        result = await self._execute_query_with_returning_one_row(query)
        if result is False:
            logger.error(
                f"Error while selecting student credentials; telegram_id = {telegram_id}, group_name = {group_name}")
            return ""
        else:
            logger.success(
                f"Selected student credentials successfully; telegram_id = {telegram_id}, group_name = {group_name}; result = {result[0]}")
            return result[0]

    async def select_lab_name_and_id_by_number(self, group_name, lab_number) -> tuple[str, int]:
        """selects lab name by number

        Args:
            group_name (str): group name
            lab_number (int): lab number

        Returns:
            str: lab name
        """
        query = f"""--sql
        SELECT lab_description, id
        FROM lab_registry
        WHERE lab_number = {lab_number}
        AND group_id = (SELECT id
                        FROM education_group
                        WHERE group_name = '{group_name}');
        """

        result = await self._execute_query_with_returning_one_row(query)
        if result is False:
            logger.error(
                f"Error while selecting lab name by number; group_name = {group_name}, lab_number = {lab_number}")
            return "", 0
        else:
            logger.success(
                f"Selected lab name by number successfully; group_name = {group_name}, lab_number = {lab_number}; result = {result[0]}{result[1]}")
            return result[0], result[1]

    async def select_lab_stats_by_whole_group(self, group_id) -> tuple[str, bool, int, datetime.date, int]:
        query = f"""--sql
        SELECT credentials as name,
               coalesce(telegram_id, 0) as is_registered,
               lab_number as number,
               lt.created_at as date,
               status_id as status
        FROM education_group_members egm
        LEFT JOIN registered_members rm on egm.member_id = rm.member_id
        FULL JOIN lab_tracker lt on rm.member_id = lt.member_id
        LEFT JOIN lab_registry lr on lt.lab_id = lr.id
        WHERE egm.group_id = {group_id};
        """

        result = await self._execute_query(query)
        if result is False:
            logger.error(
                f"Error while selecting lab stats by whole group; group_id = {group_id}")
            return None
        else:
            logger.success(
                f"Selected lab stats by whole group successfully; group_id = {group_id}; result = {result}")
            return result

    async def select_added_labs_count_for_group(self, group_id) -> int:
        query = f"""--sql
        SELECT COUNT(*) as count
        FROM lab_registry
        WHERE group_id={group_id}
        """

        result = await self._execute_query_with_returning_one_row(query)
        if result is False:
            logger.error(
                f"Error while selecting added labs count for group; group_id = {group_id}")
            return None
        else:
            logger.success(
                f"Selected added labs count for group successfully; group_id = {group_id}; result = {result}")
            return result

    async def select_lab_and_owner_telegram_id_by_lab_id(self, lab_id: int) -> tuple[models.LaboratoryWork, int] | tuple[None, None]:
        query = f"""--sql
        SELECT tracker.lab_id,
            lr.lab_number,
            lr.lab_description,
            tracker.cloud_link,
            egm.credentials,
            users.telegram_id
        FROM lab_registry lr
        LEFT JOIN lab_tracker tracker ON lr.id = tracker.lab_id
        LEFT JOIN education_group_members egm ON tracker.member_id = egm.member_id
        LEFT JOIN registered_members rm ON egm.member_id = rm.member_id
        LEFT JOIN users ON rm.telegram_id = users.telegram_id
        WHERE lr.id = {lab_id};
        """

        result = await self._execute_query_with_returning_one_row(query)
        if result is False:
            logger.error(
                f"Error while selecting lab and owner telegram_id by lab_id; lab_id = {lab_id}")
            return None, None
        else:
            logger.success(
                f"Selected lab and owner telegram_id by lab_id successfully; lab_id = {lab_id}; result = {result}")
            lab = models.LaboratoryWork()
            lab.number = result['lab_number']
            lab.description = result['lab_description']
            lab.cloud_link = result['cloud_link']
            lab.member_credentials = result['credentials']
            return lab, result['telegram_id']
