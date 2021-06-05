from lang_exch.db.db_factory import DBFactory
from lang_exch.models.language import Language
from lang_exch.setup.setup import config


class DatabaseManager():

    def __init__(self):
        db_provider = config['database']['provider']
        self._db = DBFactory(db_provider)
        self._db.connect()

    def add_language(self, lang_name: str):
        '''
           Validates a language input and then forms a Language
           object and passes this object for actual database operation
        '''
        if not lang_name.isalpha() or ' ' in lang_name:
            raise Exception(f'{lang_name} is not a valid Language. \
                            Language name must contain all the \
                            characters without space in between')
        if len(lang_name) < 0 or len(lang_name) > 20:
            raise Exception(f'{lang_name} is not a valid Language. \
                            Language length must be between 1 to 20 \
                            characters')
        self._db.add_language(Language(lang_name))


