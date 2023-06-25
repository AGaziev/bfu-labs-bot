from loguru import logger
from loader import bot
from aiogram.utils.exceptions import BotBlocked
from utils.models import Teacher
from utils.enums import Blocked
from aiogram.utils.markdown import hitalic, hlink
import asyncio


class Mailer:
    def __init__(self) -> None:
        from managers import DatabaseManager
        self._database_manager = DatabaseManager()
        self._bot = bot
        self._messages_per_second_limit = 30
        logger.debug("Mailer object was initialized")

    async def _send_message(self, user_id: int, message: str) -> None:
        """Sends message to user"""
        try:
            await self._bot.send_message(user_id, message)

        except BotBlocked:
            logger.error(f"User {user_id} blocked bot")
            await self._database_manager.update_user_is_blocked_field_by_user_id(
                user_id=user_id, is_blocked=True)

        else:
            logger.debug(
                f"Message {message:50}... was sent to user:[{user_id}]")

    async def _send_notification_to_education_group(self, group_id: int, description: str, link_to_lab: str) -> bool:
        """Sends message to education group

        Args:
            group_id (int): group id to send message
            description (str): user's description, it can be deadline or something else
            link_to_lab (str): link to lab on cloud storage
        """
        users_to_send_notification = await self._database_manager.select_registered_members_from_group(
            group_id=group_id, is_blocked=Blocked.FALSE)
        teacher = await self._database_manager.select_teacher_by_group_id(group_id=group_id)

        if not users_to_send_notification:
            logger.error(
                f"Error while selecting registered members from group; group_id = {group_id}")
            return False

        message = await self._create_notification_message(teacher=teacher, description=description,
                                                          link_to_lab=link_to_lab, group_id=group_id)

        await self._start_mailing(users_to_send_notification=users_to_send_notification, message=message)
        return True

    async def _create_notification_message(self, teacher: Teacher, description: str, link_to_lab: str, group_id: int) -> str:
        """Creates notification message for user

        Args:
            teacher (Teacher): teacher object
            description (str): user's description, it can be deadline or something else
            link_to_lab (str): link to lab on cloud storage

        Returns:
            str: notification message
        """
        group_name = await self._database_manager.select_group_name_by_group_id(group_id=group_id)
        teacher_credentials_part = f'''Преподаватель {hitalic(teacher.firstname, teacher.lastname, teacher.patronymic if teacher.patronymic else '')}\n'''
        group_name_part = f'''добавил новую лабораторную работу для группы "{group_name}"\n'''
        link_to_lab_part = f'''{hlink("ССЫЛКА", link_to_lab)} на лабораторную работу'''
        description_part = f'''\n\n Cообщение от преподавателя:\n{description}''' if description else ''

        message = teacher_credentials_part + group_name_part + \
            link_to_lab_part + description_part
        return message

    async def _start_mailing(self, users_to_send_notification: tuple[int], message: str) -> None:
        """Starts mailing to users

        Args:
            users_to_send_notification (list): list of users to send notification
            message (str): message to send
        """
        messages_before_sleep = 0
        for user_id in users_to_send_notification:
            if messages_before_sleep == self._messages_per_second_limit:
                await asyncio.sleep(1)
                messages_before_sleep = 0

            await self._send_message(user_id=user_id, message=message)
            messages_before_sleep += 1
        logger.success("Mailing was finished successfully")
