'''Module for retrieveing a Language data'''


from lang_exch.conf.log.lang_exch_logging import logger


class Language:
    '''Represent a single language'''

    def __init__(self, lang_name=None, lang_id=None):
        '''Init method'''
        self._lang_id = lang_id
        self._lang_name = lang_name

    def get_language_name(self):
        '''returns language name'''
        return self._lang_name

    def get_lang_id(self):
        '''returns unique id assosciated with language'''
        return self._lang_id
