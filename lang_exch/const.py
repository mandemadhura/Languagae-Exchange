from enum import Enum

CONF_FILE = "lang_exch/conf/lang_exc.conf"

class confSection(Enum):
    LOGGING_SECTION = "logging"
    STORAGE_SECTION = "storage"
    DATABASE_SECTION = "database"
    SERVER_SECTION = "server"

class dataBaseSection(Enum):
    DB_PROVIDER_KEY = "provider"
    DB_DATABASE_KEY = "database"
    DB_HOST_KEY = "host"
    DB_PORT_KEY = "port"
    DB_USERNAME_KEY = "username"
    DB_PASSWORD_KEY = "password"

class loggingSection(Enum):
    LOG_FILE_KEY = "log_file"
    LOG_LEVEL_KEY = "log_level"
    
class serverSection(Enum):
    SERVER_IP_KEY = "ip"
    SERVER_PORT_KEY = "port"
    DB_HOST_KEY = "host"
    DB_PORT_KEY = "port"
    DB_USERNAME_KEY = "username"
    DB_PASSWORD_KEY = "password"
