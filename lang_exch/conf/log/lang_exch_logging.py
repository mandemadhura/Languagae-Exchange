import logging
import os

from lang_exch.const import confSection, loggingSection
from lang_exch.setup.setup import config

try:
    LOG_LEVEL = config[confSection.LOGGING_SECTION.value][loggingSection.LOG_LEVEL_KEY.value]
    LOG_FILE = config[confSection.LOGGING_SECTION.value][loggingSection.LOG_FILE_KEY.value]
    LOG_PATH = config[confSection.LOGGING_SECTION.value][loggingSection.LOG_PATH_KEY.value]
except KeyError as k_err:
    raise Exception(f"Failed to parse the key from config: {k_err}")

logger = logging.getLogger('language-exchange')

log_level_mapping = {
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "WARNING": logging.WARNING,
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR
}

# DEBUG < INFO < WARNING < ERROR < CRITICAL
# Defualt root logger level is WARNING.
# So, if not set, level above warning will not be logged
logger.setLevel(log_level_mapping['DEBUG'])

log_file = os.path.join(LOG_PATH, LOG_FILE)
handler = logging.FileHandler(os.path.abspath(log_file))

# From INFO onwards, logs will be populated
handler.setLevel(log_level_mapping[LOG_LEVEL])

log_format = '%(asctime)s %(name)s [%(process)d]: %(levelname)s %(message)s'
formatter = logging.Formatter(log_format, "%Y-%m-%d %H:%M:%S")  
handler.setFormatter(formatter)

logger.addHandler(handler)
