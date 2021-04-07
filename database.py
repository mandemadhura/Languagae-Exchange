import abc


class Database(metaclass=abc.ABCMeta):

    def __init__(self, host, port, username, password):
        '''Init method'''
        self._host = host
        self._port = port
        self._username = username
        self._password = password

    def connect():
        # connect to db
        # returns a connection
        pass

    def close():
        # close the connection
        pass

    def is_open():
        # returns true if connection
	    # is open
        pass

    def get_host():
        return self._host

    def get_port():
        return self._port

    def get_username():
        return self._username

    def get_password():
        return self._password

    def get_languages(self):
        pass

    def get_language(self, lang_id):
        pass

    def add_language(self, lang_object):
        '''Inserts a new language'''
        pass

    def delete_language(self, lang_object):
        '''Deletes an existing language'''
        pass

    def update_language(self, lang_object):
        '''Updates an existing language'''
        pass


