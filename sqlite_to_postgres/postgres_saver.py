from typing import Generator
from dataclasses_movies import *
from psycopg2.extensions import connection as _connection
from db_extractor import TABLES


class PostgresSaver:

    def __init__(self, pg_conn: _connection, rows_to_insert: int):
        self.conn = pg_conn
        self.cursor = pg_conn.cursor()
        self.rows_to_insert = rows_to_insert
        self.start = 0

    @staticmethod
    def make_object(row_dict: dict, table: str):
        row_dict.pop('created_at', None)
        row_dict.pop('updated_at', None)
        if table == 'film_work':
            row_dict.pop('creation_date', None)
            row_dict.pop('file_path', None)
            item = Movie(**row_dict)
        elif table == 'genre':
            row_dict.pop('description', None)
            item = Genre(**row_dict)
        elif table == 'person':
            item = Person(**row_dict)
        elif table == 'genre_film_work':
            item = GenreFilmwork(**row_dict)
        else:
            item = PersonFilmwork(**row_dict)
        return item

    def truncate_table(self, table: str):
        self.cursor.execute(f'''
                            TRUNCATE TABLE {table} CASCADE
                            ''')
        self.conn.commit()

    def save_all_data(self, data_by_tables: Generator):
        for i, table in enumerate(data_by_tables):
            self.truncate_table(TABLES[i])
            data_to_load = []
            for j, row_dict in enumerate(table):
                row_count = row_dict['count']
                row_dict.pop('count', None)
                obj = self.make_object(row_dict, TABLES[i])
                attrs = [attr for attr in obj.__dict__ if obj.__dict__[attr]
                         is not None]
                row = tuple([getattr(obj, attr) for attr in attrs])
                data_to_load.append(row)
                if j > 0 and (j % self.rows_to_insert == 0 or j == row_count - 1):
                    str_for_sql = '(' + ('%s, ' * len(row)).strip(', ') + ')'
                    args = ','.join(self.cursor.mogrify(str_for_sql, elem).decode()
                                    for elem in data_to_load)
                    fields = ', '.join(attrs)
                    self.cursor.execute(f"""
                                        INSERT INTO content.{TABLES[i]} ({fields})
                                        VALUES {args}
                                        ON CONFLICT (id) DO NOTHING
                                        """)
                    self.conn.commit()
                    self.start += self.rows_to_insert
                    data_to_load = []

        self.cursor.close()
