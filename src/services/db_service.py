from functools import lru_cache
from contextlib import closing

import psycopg2
from psycopg2.extras import RealDictCursor

from config import config
from schemas.api import DataItem


class DbService:

    def __init__(self):
        self._dsn = {
            "dbname": config.DB_NAME,
            "user": config.DB_USER,
            "password": config.DB_PASSWORD,
            "host": config.DB_HOST,
            "port": int(config.DB_PORT),
        }

    def get_data_list(self, limit=None, offset=0) -> list[DataItem]:
        sql_script = """
        SELECT review, target FROM public.filtered_data
        {};
        """
        limit_offset_condition = ""
        if limit:
            limit_offset_condition = f"LIMIT {limit} OFFSET {offset}"
        rendered_sql_script = sql_script.format(limit_offset_condition)
        with closing(psycopg2.connect(**self._dsn, cursor_factory=RealDictCursor)) as pg_conn, pg_conn.cursor() as cur:
            cur.execute(rendered_sql_script)
            return [DataItem(review=res["review"], target=res["target"]) for res in cur.fetchall()]


@lru_cache
def get_db_service():
    return DbService()
