import configparser

config = configparser.ConfigParser()
config.read('lang_exch/conf/lang_exc.conf')


LOG_LEVEL = config['logging']['log_level']
LOG_FILE = config['logging']['log_file']
