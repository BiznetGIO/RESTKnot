import psycopg2
import os


def connect():
    try:
        connection = psycopg2.connect(
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            sslmode=os.environ.get("DB_SSL"),
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT"),
        )
        connection.autocommit = False
        return connection
    except Exception as exc:
        raise ValueError(f"{exc}")
