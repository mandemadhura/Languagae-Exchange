import logging
import os
from lang_exch.setup.setup import LOG_FILE, LOG_LEVEL

logger = logging.getLogger('language-exchange')

log_level_mapping = {
    "INFO": logging.INFO
}

# DEBUG < INFO < WARNING < ERROR < CRITICAL
# Defualt root logger level is WARNING.
# So, if not set, level above warning will not be logged
logger.setLevel(logging.DEBUG)

print(f">>>>>>>>>>>>>>>>>>>>>> {type(LOG_FILE)}")
f = "/var/log/lang_exch.log"
handler = logging.FileHandler(os.path.abspath(LOG_FILE))

# From INFO onwards, logs will be populated
handler.setLevel(log_level_mapping[LOG_LEVEL])

formatter = logging.Formatter('%(name)s: %(levelname)s: %(asctime)s: %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
