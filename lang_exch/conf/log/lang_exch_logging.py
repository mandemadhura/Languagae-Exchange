import logging

logger = logging.getLogger('language-exchange')

# DEBUG < INFO < WARNING < ERROR < CRITICAL
# Defualt root logger level is WARNING.
# So, if not set, level above warning will not be logged
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('/var/log/lang_exch.log')

# From INFO onwards, logs will be populated
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(name)s: %(levelname)s: %(asctime)s: %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
