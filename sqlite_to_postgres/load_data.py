import os
import sqlite3
from dotenv import load_dotenv
from contextlib import contextmanager
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from db_extractor import DBExtractor
from postgres_saver import PostgresSaver


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    postgres_saver = PostgresSaver(pg_conn, rows_to_insert=10)
    sqlite_extractor = DBExtractor(connection)

    data_by_tables = sqlite_extractor.extract_movies()
    postgres_saver.save_all_data(data_by_tables)


if __name__ == '__main__':
    load_dotenv()

    @contextmanager
    def conn_context(db_path: str):
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        yield conn
        conn.close()

    dsl = {'dbname': os.environ.get('DB_NAME'),
           'user': os.environ.get('DB_USER'),
           'password': os.environ.get('DB_PASSWORD'),
           'host': os.environ.get('DB_HOST'),
           'port': os.environ.get('DB_PORT')}
    db_path = os.environ.get('DB_PATH')
    with conn_context(db_path) as sqlite_conn, \
            psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
