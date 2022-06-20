import logging
import os
from lang_exch.setup.setup import LOG_FILE, LOG_LEVEL, LOG_PATH

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
