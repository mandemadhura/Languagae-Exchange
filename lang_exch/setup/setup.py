'''Initializes and read configuration file'''

import configparser

from lang_exch.const import CONF_FILE

try:
    config = configparser.ConfigParser()
    config.read(CONF_FILE)
except IOError as err:
    config = None
    raise Exception(f"Failed to read config file: {CONF_FILE}: {err}")