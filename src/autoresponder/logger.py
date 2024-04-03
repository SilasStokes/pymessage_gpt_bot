import logging
from src.runtime_environment import LOGGER_FILE, RUNNING_AS_EXECUTABLE

if RUNNING_AS_EXECUTABLE:
    logging.basicConfig(level=logging.DEBUG, filename=LOGGER_FILE)
    logger = logging.getLogger(__name__)
else:
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
