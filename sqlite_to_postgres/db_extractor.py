import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection

TABLES = ['film_work', 'genre', 'person', 'genre_film_work', 'person_film_work']


class DBExtractor:

    def __init__(self, connection: sqlite3.Connection | _connection):
        self.conn = connection
        self.cursor = connection.cursor()

    def data_generator(self):
        for row in self.cursor:
            yield dict(row)

    def extract_movies(self):
        for table in TABLES:
            if isinstance(self.conn, sqlite3.Connection):
                query = '''
                        SELECT *, (SELECT COUNT(*) FROM {}) as count FROM {} ORDER BY id;
                        '''.format(table, table)
            elif isinstance(self.conn, psycopg2.extensions.connection):
                query = '''
                        SELECT * FROM {} ORDER BY id;
                        '''.format(table)
            self.cursor.execute(query)
            yield self.data_generator()
