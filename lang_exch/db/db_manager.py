'''Routine which helps in data validation and connecting a link to Database'''


from lang_exch.db.db_factory import DBFactory
from lang_exch.models.language import Language
from lang_exch.setup.setup import config
from lang_exch.conf.log.lang_exch_logging import logger


class DatabaseManager():
    '''Module who is responsible for connection between server and database'''

    def __init__(self):
        '''Init method'''
        db_provider = config['database']['provider']
        self._db = DBFactory(db_provider)
        self._db.connect()

    def add_language(self, lang_obj: Language):
        '''
           Validates a language input and then forms a Language
           object and passes this object for actual database operation
        '''
        lang_name = lang_obj.get_language_name()

        if not lang_name.isalpha() or ' ' in lang_name:
            raise Exception(f'{lang_name} is not a valid Language. \
                            Language name must contain all the \
                            characters without space in between')
        if len(lang_name) < 0 or len(lang_name) > 20:
            raise Exception(f'{lang_name} is not a valid Language. \
                            Language length must be between 1 to 20 \
                            characters')
        lang_id = self._db.add_language(lang_name) or None
        return lang_id

    def update_language(self, lang_obj: Language, lang_name):
        '''
           Validates a language input and then forms a Language
           object and passes this object for actual database operation
           to update a language
        '''
        lang_id = lang_obj.get_lang_id()

        logger.info(f'Got a request to update a lang_id: {lang_id} with \
                      new language value: {lang_name}')

        if not lang_name.isalpha() or ' ' in lang_name:
            raise Exception(f'{lang_name} is not a valid Language. \
                            Language name must contain all the \
                            characters without space in between')
        if len(lang_name) < 0 or len(lang_name) > 20:
            raise Exception(f'{lang_name} is not a valid Language. \
                            Language length must be between 1 to 20 \
                            characters')

        self._db.update_language(lang_id, lang_name)

    def delete_language(self, lang_obj: Language):
        '''
           Validates a language input and then forms a Language
           object and passes this object for actual database operation
           to update a language
        '''
        lang_id = lang_obj.get_lang_id()

        logger.info(f'Got a request to delete a langauge with \
                      lang_id: {lang_id}')

        self._db.delete_language(lang_id)

