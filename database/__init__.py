from loguru import logger
try:
    from .inserter import Inserter
    from .selector import Selector
    from .updater import Updater
    from .deleter import Deleter
except ImportError:
    logger.error(
        "Error while importing inserter.py, selector.py, updater.py or deleter.py")

try:
    from .creator import Creator
    from .filler import Filler
except ImportError:
    logger.error("Error while importing creator.py or filler.py")
