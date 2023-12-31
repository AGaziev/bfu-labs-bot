from .database_connector import DatabaseConnector
from loguru import logger


class Updater(DatabaseConnector):
    """
    Class for updating data in database\n
    """

    def __init__(self) -> None:
        super().__init__()
        logger.debug("Updater for database object was initialized")

    async def update_user_is_blocked_field_by_user_id(self, user_id: int, is_blocked: bool) -> bool:
        """
        Updates is_blocked field in user_data table\n

        Args:
            user_id (int): telegram user id to update
            is_blocked (bool): new value of is_blocked field

        Returns:
            bool: True if user was updated successfully, False otherwise
        """
        query = f"""--sql
        UPDATE users
        SET is_blocked = {is_blocked}
        WHERE telegram_id = {user_id};
        """
        result = await self._execute_query(query)
        if result is False:
            logger.error(
                logger.error(f"Error while updating users.is_blocked with {is_blocked} for user_id = {user_id}"))
            return False
        else:
            logger.success(
                f"Updated users.is_blocked with {is_blocked} for user_id = {user_id} successfully")
            return True

    async def update_lab_status(self, lab_id: int, status: str):
        query = f"""--sql
        UPDATE lab_tracker
        SET status_id = (
            SELECT id
            FROM lab_status_type
            WHERE status_name = '{status}'),

            updated_at = NOW()

        WHERE id = {lab_id};
        """
        result = await self._execute_query(query)
        if result is False:
            logger.error(
                logger.error(f"Error while updating labs.status with {status} for lab_id = {lab_id}"))
            return False
        else:
            logger.success(
                f"Updated labs.status with {status} for lab_id = {lab_id} successfully")
            return True
