import os
import sqlite3
from contextlib import contextmanager
import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.extensions import connection as _connection
from dotenv import load_dotenv

from sqlite_to_postgres.db_extractor import DBExtractor

TABLES = ['film_work', 'genre', 'person', 'genre_film_work', 'person_film_work']


def compare_counts(sqlite_conn: sqlite3.Connection, pg_conn: _connection):
    sqlite_cursor = sqlite_conn.cursor()
    pg_cursor = pg_conn.cursor()
    for table in TABLES:
        query = '''
                SELECT COUNT(*) as count FROM {};
                '''.format(table)
        sqlite_cursor.execute(query)
        row_count_sqlite = dict(sqlite_cursor.fetchone())['count']
        pg_cursor.execute(query)
        row_count_pg = pg_cursor.fetchone()[0]
        assert row_count_sqlite == row_count_pg


def compare_rows(sqlite_conn: sqlite3.Connection, pg_conn: _connection):
    sqlite_extractor = DBExtractor(sqlite_conn)
    postgres_extractor = DBExtractor(pg_conn)
    tables_sqlite = sqlite_extractor.extract_movies()
    tables_postgres = postgres_extractor.extract_movies()
    for table_sqlite, table_postgres in zip(tables_sqlite, tables_postgres):
        for i, (row1, row2) in enumerate(zip(table_sqlite, table_postgres)):
            row_dict_sqlite, row_dict_pg = dict(row1), dict(row2)
            row_dict_pg.pop('created', None)
            row_dict_pg.pop('modified', None)
            for field in row_dict_pg:
                if row_dict_pg[field] in ('', 0.0):
                    row_dict_pg[field] = None
                assert row_dict_pg[field] == row_dict_sqlite[field]


if __name__ == '__main__':
    load_dotenv()

    @contextmanager
    def conn_context(db_path: str):
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        yield conn
        conn.close()

    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '1234',
           'host': '127.0.0.1', 'port': 5432}
    db_path = os.environ.get('DB_PATH')
    with conn_context(db_path) as sqlite_conn, \
            psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        compare_counts(sqlite_conn, pg_conn)
        compare_rows(sqlite_conn, pg_conn)

