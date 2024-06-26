import asyncio

from aiogram.utils.exceptions import BotBlocked
from aiogram.utils.markdown import hitalic, hbold, hcode
from loguru import logger

import keyboards as kb
from loader import bot
from managers.db import DatabaseManager
from utils.models import Teacher


class Mailer:
    def __init__(self) -> None:

        self._bot = bot
        self._messages_per_second_limit = 30
        logger.debug("Mailer object was initialized")

    async def _send_message(self, user_id: int, message: str, url_to_lab: str) -> None:
        """Sends message to user"""
        try:
            await self._bot.send_message(user_id, message,
                                         reply_markup=await kb.cloud_link_to_lab_kb(
                                             url=url_to_lab),
                                         parse_mode="HTML")

        except BotBlocked:
            logger.error(f"User {user_id} blocked bot")
            DatabaseManager.update_user_is_blocked_field_by_user_id(
                user_id=user_id, is_blocked=True)

        else:
            logger.debug(
                f"Message {message:50}... was sent to user:[{user_id}]")

    async def send_notification_to_education_group(self, group_id: int, description: str, link_to_lab: str) -> bool:
        """Sends message to education group

        Args:
            group_id (int): group id to send message
            description (str): user's description, it can be deadline or something else
            link_to_lab (str): link to lab on cloud storage
        """
        group = DatabaseManager.get_group_by_id(group_id)
        students_to_send_notification = DatabaseManager.select_all_members_from_group(group)
        teacher = DatabaseManager.get_teacher_by_group_id(group_id)

        if not len(students_to_send_notification):
            logger.warning(
                f"No users to send notification, add some; group_id = {group.name}")
            return False
        else:
            active_students = filter(lambda student: student.user, students_to_send_notification)
        message = self._create_notification_message(teacher=teacher, description=description,
                                                    link_to_lab=link_to_lab, group_id=group_id)

        await self._start_mailing(users_to_send_notification=list(active_students), message=message,
                                  url_to_lab=link_to_lab)
        return True

    @staticmethod
    def _create_notification_message(teacher: Teacher, description: str, link_to_lab: str, group_id: int) -> str:
        """Creates notification message for user

        Args:
            teacher (Teacher): teacher object
            description (str): user's description, it can be deadline or something else
            link_to_lab (str): link to lab on cloud storage

        Returns:
            str: notification message
        """
        group_name = DatabaseManager.get_group_by_id(group_id=group_id).name
        teacher_credentials_part = f'''Преподаватель {hitalic(teacher.first_name)} {hitalic(teacher.last_name)} {hitalic(teacher.patronymic if teacher.patronymic else '')}\n'''
        description_part = f'''добавил новую лабораторную работу "{hcode(description)}"\n'''
        group_name_part = f'''для группы {hbold(group_name)}\n\n'''

        message = teacher_credentials_part + description_part + group_name_part
        return message

    async def _start_mailing(self, users_to_send_notification, message: str,
                             url_to_lab: str) -> None:
        """Starts mailing to users

        Args:
            users_to_send_notification (list): list of users to send notification
            message (str): message to send
        """
        logger.warning("Mailing was started")
        messages_before_sleep = 0
        for groupMember in users_to_send_notification:
            if messages_before_sleep == self._messages_per_second_limit:
                await asyncio.sleep(1)
                messages_before_sleep = 0

            await self._send_message(user_id=groupMember.user, message=message, url_to_lab=url_to_lab)
            messages_before_sleep += 1
        logger.success("Mailing was finished successfully")
