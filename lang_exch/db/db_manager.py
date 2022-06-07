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
        lang_id = self._db.add_language(Language(lang_name)) or None
        return lang_id

    def update_language(self, lang_id: int, lang_name: str):
        '''
        validates a language input and then forms a Language 
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
        self._db.update_language(Language(lang_id=lang_id), lang_name)

    def delete_language(self, lang_id: int):
        '''
        Forms a Language object and passes this object for actual database 
        delete operation
        '''
        self._db.delete_language(Language(lang_id=lang_id))

    def get_a_language(self, lang_id: int):
        '''
        Forms a language object and passes this object for actual database
        get operation
        '''
        return self._db.get_language(lang_id) or None

    def get_languages(self):
        '''
        Forms a language object and passes this object for actual database
        fetch operation
        '''
        return self._db.get_languages()
