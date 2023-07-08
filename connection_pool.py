import os
from contextlib import contextmanager

from psycopg2.pool import SimpleConnectionPool
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()
database_url = os.environ["DATABASE_URL"]

pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dsn=database_url,
    connection_factory=psycopg2.extras.RealDictConnection,  # have cursors return dictionaries
)

@contextmanager
def get_connection():
    connection = pool.getconn()
    try:
        yield connection
    finally:  # remember finally blocks always run.
        pool.putconn(connection)

def setup_schema(connection):
    with connection.cursor() as cursor:
        with open("schema.sql") as f:
            cursor.execute(f.read())
    connection.commit()

def reset_database(connection):
    with connection.cursor() as cursor:
        with open("reset.sql") as f:
            cursor.execute(f.read())
        with open("schema.sql") as f:
            cursor.execute(f.read())
    connection.commit()