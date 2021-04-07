import psycopg2

from database import Database
from models.language import Language

class PostgresDB(Database):
    '''Connects and communicates to postgres database'''

    def __init__(self, host, username, database, port=5432, password=None):
        '''Init method'''
        super(PostgresDB, self).__init__(host, port, username, password)
        self._db_name = database
        self.pg_conn_obj = None

    def connect(self):
        '''establishes a connection to postgres'''
        self.pg_conn_obj = psycopg2.connect(
                    host=self._host,
                    user=self._username,
                    password=self._password,
                    port=self._port)

    def add_language(self, lang_obj):
        '''A new table entry will be added for a new language'''
        lang = lang_obj.get_language_name()

        # Use in-memory cursor object for fast read write access
        # This will create as well as open the cursor
        cursor_obj = self.pg_conn_obj.cursor()

        # TODO: how to get table name and how to get column name.
        # For now, its hardcoded
        cursor_obj.execute("""
        INSERT INTO lang_exch.languages (lang_name)
        VALUES (%(str)s);
        """,
        {'str': lang})

        # commit the transaction in order to flush the
        # in-memory cursor buffer
        self.pg_conn_obj.commit()
        cursor_obj.close()

    def update_language(self, lang_obj, new_lang):
        '''An entry will be updated for the existing language'''
        lang_id = lang_obj.get_lang_id()

        cursor_obj = self.pg_conn_obj.cursor()

        cursor_obj.execute("""
        UPDATE lang_exch.languages SET lang_name = %(str)s
        WHERE lang_id = %(int)s;
        """,
        {'str': new_lang, 'int': lang_id})

        self.pg_conn_obj.commit()
        cursor_obj.close()

    def delete_language(self, lang_obj):
        '''An entry for the requested language will be deleted'''
        lang_id = lang_obj.get_lang_id()

        cursor_obj = self.pg_conn_obj.cursor()

        cursor_obj.execute("""
        DELETE FROM lang_exch.languages
        WHERE lang_id = %(int)s;
        """,
        {'int': lang_id})

        self.pg_conn_obj.commit()
        cursor_obj.close()

    def get_language(self, lang_id):
        '''Returns a language record for a given id'''

        cursor_obj = self.pg_conn_obj.cursor()

        cursor_obj.execute("""
        SELECT * FROM lang_exch.languages
        WHERE lang_id = %(int)s;
        """,
        {'int': lang_id})

        row = cursor_obj.fetchone()
        while row:
            print(row)
            row = cursor_obj.fetchone()

        cursor_obj.close()

    def get_languages(self):
        '''Returns all the language records'''

        cursor_obj = self.pg_conn_obj.cursor()

        cursor_obj.execute("""
        SELECT * FROM lang_exch.languages;
        """)

        row = cursor_obj.fetchone()
        while row:
            print(row)
            row = cursor_obj.fetchone()

        cursor_obj.close()

pd = PostgresDB('localhost', 'le_user', 'lang_exch')
pd.connect()
l = Language('Germn', 13)
#pd.add_language(l)
# pd.update_language(l, 'German')
# pd.delete_language(l)
# pd.get_language(1)
pd.get_languages()
