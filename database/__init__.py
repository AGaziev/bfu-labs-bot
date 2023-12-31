from loguru import logger
try:
    from _legacy.inserter import Inserter
    from _legacy.selector import Selector
    from _legacy.updater import Updater
    from _legacy.deleter import Deleter
except ImportError:
    logger.error(
        "Error while importing inserter.py, selector.py, updater.py or deleter.py")

try:
    from _legacy.creator import Creator
    from _legacy.filler import Filler
except ImportError:
    logger.error("Error while importing inserter.py or filler.py")
