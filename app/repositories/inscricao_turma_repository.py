from app.database.db import get_connection
from app.models.inscricao_turma import InscricaoTurma


class InscricaoTurmaRepository:
    def _from_row(self, row):
        return InscricaoTurma(*row) if row else None

    def list_all(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inscricoes_turmas ORDER BY data_inscricao DESC")
            return [InscricaoTurma(*row) for row in cursor.fetchall()]

    def list_by_estudante(self, id_estudante):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM inscricoes_turmas
                   WHERE id_estudante = %s
                   ORDER BY data_inscricao DESC""",
                (id_estudante,),
            )
            return [InscricaoTurma(*row) for row in cursor.fetchall()]

    def find_by_estudante_turma(self, id_estudante, id_turma):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM inscricoes_turmas
                   WHERE id_estudante = %s AND id_turma = %s""",
                (id_estudante, id_turma),
            )
            return self._from_row(cursor.fetchone())

    def find_aprovada(self, id_estudante, id_turma):
        inscricao = self.find_by_estudante_turma(id_estudante, id_turma)
        return inscricao if inscricao and inscricao.status == "APROVADA" else None

    def create(self, payload):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO inscricoes_turmas (id_estudante, id_turma, status)
                   VALUES (%s, %s, 'PENDENTE')
                   RETURNING *""",
                (payload["id_estudante"], payload["id_turma"]),
            )
            conn.commit()
            return self._from_row(cursor.fetchone())

    def update_status(self, id_inscricao, status):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE inscricoes_turmas SET status = %s WHERE id_inscricao = %s RETURNING *",
                (status, id_inscricao),
            )
            conn.commit()
            return self._from_row(cursor.fetchone())
