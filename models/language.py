class Language:
    '''Represenst a single language'''

    def __init__(lang_id=None, lang_name):
        self._lang_id = lang_id
        self._lang_name = lang_name

    def get_language_name():
        '''returns language name'''
        return self._lang_name

    def get_lang_id():
        '''returns unique id assosciated with language'''
        return self._lang_id
