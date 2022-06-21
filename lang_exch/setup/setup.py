'''Initializes and read configuration file'''

import configparser

from lang_exch.const import confSection, loggingSection, CONF_FILE


config = configparser.ConfigParser()
config.read(CONF_FILE)


