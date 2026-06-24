import os
from psycopg2 import pool
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dsn=os.getenv("DATABASE_URL")
)

@contextmanager
def get_connection():
    conn = connection_pool.getconn()
    try:
        yield conn # pausa para a chamada do with conn dentro dos repository
    finally:
         connection_pool.putconn(conn) # devolve a conexão para o pool