'''Module for Any of the Database routines'''

from abc import ABCMeta, abstractmethod
from models.language import Language


class Database(metaclass=ABCMeta):
    '''Abstract base class for any database communication'''

    def __init__(self, host, port, username, password):
        '''Init method'''
        self._host = host
        self._port = port
        self._username = username
        self._password = password

    @abstractmethod
    def connect(self):
        '''
        connects to database and returns a connection object
        '''
        raise NotImplementedError('Derived class must implement this')

    @abstractmethod
    def close(self):
        '''
        closes the connection with databse
        '''
        raise NotImplementedError('Derived class must implement this')

    @abstractmethod
    def is_open(self):
        '''
        Returns true if connection with database is open
        '''
        raise NotImplementedError('Derived class must implement this')

    def get_host(self):
        '''
        Returns the hostname used while connecting to database
        '''
        return self._host

    def get_port(self):
        '''
        Returns the port used while connecting to database
        '''
        return self._port

    def get_username(self):
        '''
        Returns the username used while connecting to database
        '''
        return self._username

    def get_password(self):
        '''
        Returns the password used while connecting to database
        '''
        return self._password

    @abstractmethod
    def get_languages(self) -> None:
        '''
        Returns all the information for every
        language present in the database
        '''
        raise NotImplementedError('Derived class must implement this')

    @abstractmethod
    def get_language(self, lang_id: int) -> None:
        '''
        Returns all the information for a given
        language present in the database
        '''
        raise NotImplementedError('Derived class must implement this')

    @abstractmethod
    def add_language(self, lang_obj: Language) -> None:
        '''Inserts a new language into the database'''
        raise NotImplementedError('Derived class must implement this')

    @abstractmethod
    def delete_language(self, lang_obj: Language) -> None:
        '''Deletes an existing language from the database'''
        raise NotImplementedError('Derived class must implement this')

    @abstractmethod
    def update_language(self, lang_obj: Language, new_lang: str) -> None:
        '''Updates an existing language from the database'''
        raise NotImplementedError('Derived class must implement this')
