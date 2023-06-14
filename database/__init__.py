from loguru import logger
try:
    from .creator import configure_database_tables
except ImportError:
    logger.error("Error while importing creator.py")
