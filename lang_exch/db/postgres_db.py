'''Module for Postgres Database routines'''

import configparser
import psycopg2

from lang_exch.db.database import Database
from lang_exch.models.language import Language
from lang_exch.conf.log.lang_exch_logging import logger
from lang_exch.const import dataBaseSection


class PostgresDB(Database):
    '''Connects and communicates to postgres database'''

    def __init__(self, **kwargs):
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

        try:
            self._db_name = db_conf_dict[dataBaseSection.DB_PROVIDER_KEY.value]
            self._host = db_conf_dict[dataBaseSection.DB_HOST_KEY.value]
            self._port = db_conf_dict[dataBaseSection.DB_PORT_KEY.value]
            self._username = db_conf_dict[dataBaseSection.DB_USERNAME_KEY.value]
            self._password = db_conf_dict[dataBaseSection.DB_PASSWORD_KEY.value]
            self._database = db_conf_dict[dataBaseSection.DB_DATABASE_KEY.value]
            super().__init__(self._host, self._port, self._username, self._password)
            logger.debug(f'POSTGRES: Received database connection paremeters: Host: {self._host} \
                Port: {self._port} Uname: {self._username} Pwd: {self._password} \
                    Database: {self._database}')
        except (configparser.NoSectionError, configparser.NoOptionError) as conf_err:
            logger.error(f"POSTGRES: Failed to read from config file: {conf_err}")
            raise Exception(f"failed to read from config file: {conf_err}")
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
        try:
            self.__pg_conn_obj = psycopg2.connect(
                        host=self._host,
                        user=self._username,
                        password=self._password,
                        database=self._database,
                        port=self._port)
        except psycopg2.OperationalError as err:
            logger.error(f"POSTGRES: Failed to connect to postgres database")
            raise
        logger.debug(f"POSTGRES: Connected to postgres database: {self.__pg_conn_obj}")

    def add_language(self, lang_obj: Language) -> None:
        '''A new table entry will be added for a new language

        Args:
            lang_onj: object of type Language

        Returns:
            None
        '''
        language_id = None
        lang = lang_obj.get_language_name()

        try:
            # Use in-memory cursor object for fast read write access
            # This will create as well as open the cursor
            cursor_obj = self.__pg_conn_obj.cursor()

            logger.info(f'POSTGRES: Querying database to insert a new language:{lang} to a postgres db')

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
            logger.info(f'POSTGRES: New language:{lang} successfully added in the Database: {language_id}')
        except (psycopg2.OperationalError, psycopg2.ProgrammingError) as err:
            logger.error(f"POSTGRES: psycopg error: {err}")
            raise Exception(f"psycopg error: {err}")
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
        try:
            cursor_obj = self.__pg_conn_obj.cursor()

            logger.info(f'POSTGRES: Querying database to update a language with ID:{lang_id} with new lang: {new_lang}\
                to a postgres db')

            cursor_obj.execute("""
            UPDATE lang_exch.languages SET lang_name = %(str)s
            WHERE lang_id = %(int)s;
            """,
            {'str': new_lang, 'int': lang_id})

            self.__pg_conn_obj.commit()
            cursor_obj.close()
            logger.info(f'POSTGRES: language successfully updated with {new_lang} in the Database')
        except (psycopg2.OperationalError, psycopg2.ProgrammingError) as err:
            logger.error(f"POSTGRES: psycopg error: {err}")
            raise Exception(f"psycopg error: {err}")

    def delete_language(self, lang_obj: Language) -> None:
        '''An entry for the requested language will be deleted

        Args:
            lang_obj: An object of type Language

        Returns:
            None
        '''
        lang_id = lang_obj.get_lang_id()

        try:
            cursor_obj = self.__pg_conn_obj.cursor()
            logger.info(f'POSTGRES: Querying database to delete a language with ID:{lang_id} to a postgres db')
        
            cursor_obj.execute("""
            DELETE FROM lang_exch.languages
            WHERE lang_id = %(int)s;
            """,
            {'int': lang_id})

            self.__pg_conn_obj.commit()
            cursor_obj.close()
            logger.info('POSTGRES: language successfully deleted from the Database')
        except (psycopg2.OperationalError, psycopg2.ProgrammingError) as err:
            logger.error(f"POSTGRES: psycopg error: {err}")
            raise Exception(f"psycopg error: {err}")

    def get_language(self, lang_id: int) -> str:
        '''Returns a language record for a given id

        args:
            lang_id: id of a language whose record is needed

        returns:
            None
        '''
        try:
            cursor_obj = self.__pg_conn_obj.cursor()
            logger.info(f'POSTGRES: Querying database to get language details for ID:{lang_id} to a postgres db')
    
            cursor_obj.execute("""
            SELECT * FROM lang_exch.languages
            WHERE lang_id = %(int)s;
            """,
            {'int': lang_id})

            lang_name = cursor_obj.fetchone()[1]
            cursor_obj.close()
            logger.info('POSTGRES: language details successfully fetched from the Database')
        except (psycopg2.OperationalError, psycopg2.ProgrammingError) as err:
            logger.error(f"POSTGRES: psycopg error: {err}")
            raise Exception(f"psycopg error: {err}")
        return lang_name

    def get_languages(self) -> None:
        '''Returns all the language records

        args:
            None

        returns:
            None
        '''
        try:
            cursor_obj = self.__pg_conn_obj.cursor()

            logger.info(f'POSTGRES: Querying database to get details for all languages to a postgres db')

            cursor_obj.execute("""
            SELECT * FROM lang_exch.languages;
            """)

            row = cursor_obj.fetchall()
            id_name_map = {}
            for fields in row:
                logger.info(f'Corresponding language for all language get query:')
                id_name_map[fields[0]] = fields[1].strip()
            cursor_obj.close()
            logger.info('POSTGRES: language details successfully fetched from the Database')
        except (psycopg2.OperationalError, psycopg2.ProgrammingError) as err:
            logger.error(f"POSTGRES: psycopg error: {err}")
            raise Exception(f"psycopg error: {err}")
        return id_name_map

