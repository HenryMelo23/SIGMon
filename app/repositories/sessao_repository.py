from app.database.db import get_connection
from app.models.sessao_tutoria import SessaoTutoria


class SessaoRepository:
    def _from_row(self, row):
        return SessaoTutoria(*row) if row else None

    def list_all(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sessoes_tutoria ORDER BY data_registro DESC, id_sessao DESC")
            return [SessaoTutoria(*row) for row in cursor.fetchall()]

    def list_by_estudante(self, id_estudante):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM sessoes_tutoria
                   WHERE id_estudante = %s
                   ORDER BY data_registro DESC, id_sessao DESC""",
                (id_estudante,),
            )
            return [SessaoTutoria(*row) for row in cursor.fetchall()]

    def get_by_id(self, id_sessao):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sessoes_tutoria WHERE id_sessao = %s", (id_sessao,))
            return self._from_row(cursor.fetchone())

    def create(self, payload):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO sessoes_tutoria
                   (id_slot, id_estudante, assunto, observacoes, realizada, data_registro)
                   VALUES (%s, %s, %s, %s, %s, %s)
                   RETURNING *""",
                (
                    payload["id_slot"],
                    payload["id_estudante"],
                    payload["assunto"],
                    payload["observacoes"],
                    payload["realizada"],
                    payload["data_registro"],
                ),
            )
            conn.commit()
            return self._from_row(cursor.fetchone())

    def update(self, id_sessao, payload):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE sessoes_tutoria SET realizada = %s WHERE id_sessao = %s RETURNING *",
                (payload["realizada"], id_sessao),
            )
            conn.commit()
            return self._from_row(cursor.fetchone())

    def count_nao_realizadas(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sessoes_tutoria WHERE realizada = FALSE")
            return cursor.fetchone()[0]
