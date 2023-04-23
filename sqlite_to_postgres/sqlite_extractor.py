import sqlite3

TABLES = ['film_work', 'genre', 'person', 'genre_film_work', 'person_film_work']


class SQLiteExtractor:

    def __init__(self, connection: sqlite3.Connection):
        self.cursor = connection.cursor()

    def data_generator(self):
        for row in self.cursor:
            yield dict(row)

    def extract_movies(self):
        for table in TABLES:
            self.cursor.execute('''
            SELECT *, (SELECT COUNT(*) FROM {}) as count FROM {} ORDER BY id;
            '''.format(table, table))
            yield self.data_generator()
