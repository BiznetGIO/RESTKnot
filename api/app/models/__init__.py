import os
from typing import Any, Dict, List, Optional, Tuple, Union

import psycopg
from psycopg.rows import dict_row


def connect() -> Tuple[psycopg.cursor.Cursor, psycopg.Connection]:
    """Connect to database."""
    try:
        # DB_URI must be present
        db_uri = os.environ["DB_URI"]
        connection = psycopg.connect(db_uri)
        cursor = connection.cursor(row_factory=dict_row)
        return cursor, connection
    except Exception as exc:
        raise ValueError(f"{exc}")
