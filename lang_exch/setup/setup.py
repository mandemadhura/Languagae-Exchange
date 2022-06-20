import configparser
from lang_exch.const import confSection, loggingSection, CONF_FILE

config = configparser.ConfigParser()
config.read(CONF_FILE)


LOG_LEVEL = config[confSection.LOGGING_SECTION.value][loggingSection.LOG_LEVEL_KEY.value]
LOG_FILE = config[confSection.LOGGING_SECTION.value][loggingSection.LOG_FILE_KEY.value]
LOG_PATH = config[confSection.LOGGING_SECTION.value][loggingSection.LOG_PATH_KEY.value]