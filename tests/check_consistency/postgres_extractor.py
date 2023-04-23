from typing import Generator
from psycopg2.extensions import connection as _connection
from test_db import TABLES


class PostgresExtractor:

    def __init__(self, pg_conn: _connection):
        self.cursor = pg_conn.cursor()

    def data_generator(self) -> Generator:
        for row in self.cursor:
            yield dict(row)

    def extract_movies(self) -> Generator:
        for table in TABLES:
            self.cursor.execute('''
            SELECT * FROM {} ORDER BY id;
            '''.format(table, table))
            yield self.data_generator()
