'''Module for Postgres Database routines'''

import psycopg2

from lang_exch.db.database import Database
from lang_exch.models.language import Language
from lang_exch.conf.log.lang_exch_logging import logger
from lang_exch.const import dataBaseSection


class PostgresDB(Database):
    '''Connects and communicates to postgres database'''

    def __init__(self, **kwargs): #host: str, username: str, database: str, port: int=5432, password: str=None):
        '''Init method
        Args:
            host: hostname to connect to database
            username: database username
            database: database name
            port: port for connection
            password: database password

        Returns:
            PostgresDB()
        '''
        for args_val in kwargs.values():
            db_conf_dict = args_val

        self._db_name = db_conf_dict[dataBaseSection.DB_PROVIDER_KEY.value]
        self._host = db_conf_dict[dataBaseSection.DB_HOST_KEY.value]
        self._port = db_conf_dict[dataBaseSection.DB_PORT_KEY.value]
        self._username = db_conf_dict[dataBaseSection.DB_USERNAME_KEY.value]
        self._password = db_conf_dict[dataBaseSection.DB_PASSWORD_KEY.value]
        self._database = db_conf_dict[dataBaseSection.DB_DATABASE_KEY.value]
        super().__init__(self._host, self._port, self._username, self._password)
        print(f'{self._host} {self._port} {self._username} {self._password} {self._database}')
        self.__pg_conn_obj = None

    def close(self) -> None:
        '''closes connection with postgres
        Args:
            None

        Returns:
            None
        '''

    def is_open(self) -> bool:
        '''Returns True if connection with postgres
        database is open

        Args:
            None

        Returns:
            None
        '''

    def connect(self) -> None:
        '''establishes a connection to postgres

        Args:
            None

        Returns:
            None
        '''
        self.__pg_conn_obj = psycopg2.connect(
                    host=self._host,
                    user=self._username,
                    password=self._password,
                    database=self._database,
                    port=self._port)

    def add_language(self, lang_obj: Language) -> None:
        '''A new table entry will be added for a new language

        Args:
            lang_onj: object of type Language

        Returns:
            None
        '''
        language_id = None
        lang = lang_obj.get_language_name()

        # Use in-memory cursor object for fast read write access
        # This will create as well as open the cursor
        cursor_obj = self.__pg_conn_obj.cursor()

        # TODO: how to get table name and how to get column name.
        # For now, its hardcoded
        cursor_obj.execute("""
        INSERT INTO lang_exch.languages (lang_name)
        VALUES (%(str)s) RETURNING lang_id;
        """,
        {'str': lang})

        language_id = cursor_obj.fetchone()[0]

        # commit the transaction in order to flush the
        # in-memory cursor buffer
        self.__pg_conn_obj.commit()
        cursor_obj.close()
        logger.info(f'New language:{lang} successfully added in the Database: {language_id}')
        return language_id

    def update_language(self, lang_obj: Language, new_lang: str) -> None:
        '''An entry will be updated for the existing language

        Args:
            lang_obj: object of type Language
            new_lang: A new language name

        Returns:
            None
        '''
        lang_id = lang_obj.get_lang_id()

        cursor_obj = self.__pg_conn_obj.cursor()

        cursor_obj.execute("""
        UPDATE lang_exch.languages SET lang_name = %(str)s
        WHERE lang_id = %(int)s;
        """,
        {'str': new_lang, 'int': lang_id})

        self.__pg_conn_obj.commit()
        cursor_obj.close()
        logger.info(f'language successfully updated with {new_lang} in the Database')

    def delete_language(self, lang_obj: Language) -> None:
        '''An entry for the requested language will be deleted

        Args:
            lang_obj: An object of type Language

        Returns:
            None
        '''
        lang_id = lang_obj.get_lang_id()

        cursor_obj = self.__pg_conn_obj.cursor()

        cursor_obj.execute("""
        DELETE FROM lang_exch.languages
        WHERE lang_id = %(int)s;
        """,
        {'int': lang_id})

        self.__pg_conn_obj.commit()
        cursor_obj.close()
        logger.info('language successfully deleted from the Database')

    def get_language(self, lang_id: int) -> str:
        '''Returns a language record for a given id

        args:
            lang_id: id of a language whose record is needed

        returns:
            None
        '''
        cursor_obj = self.__pg_conn_obj.cursor()

        cursor_obj.execute("""
        SELECT * FROM lang_exch.languages
        WHERE lang_id = %(int)s;
        """,
        {'int': lang_id})

        lang_name = cursor_obj.fetchone()[1]
        cursor_obj.close()
        return lang_name

    def get_languages(self) -> None:
        '''Returns all the language records

        args:
            None

        returns:
            None
        '''

        cursor_obj = self.__pg_conn_obj.cursor()

        cursor_obj.execute("""
        SELECT * FROM lang_exch.languages;
        """)

        row = cursor_obj.fetchall()
        id_name_map = {}
        for fields in row:
            logger.info(f'Corresponding language for all language get query:')
            id_name_map[fields[0]] = fields[1].strip()
        cursor_obj.close()
        return id_name_map

#pd = PostgresDB('localhost', 'le_user', 'lang_exch')
#pd.connect()
#l = Language('Germn', 14)
## pd.add_language(l)
## pd.update_language(l, 'German')
## pd.delete_language(l)
## pd.get_language(1)
#pd.get_languages()
