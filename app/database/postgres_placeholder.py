"""
Ponto planejado para conexão futura com PostgreSQL.

Quando o banco real for conectado, este módulo pode inicializar SQLAlchemy,
psycopg2, pool de conexões, migrations e repositories concretos.
"""


def get_connection():
    raise NotImplementedError("A persistência real será adicionada em fase posterior.")
