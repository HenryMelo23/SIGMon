from app.database.db import get_connection
from app.models.candidatura import Candidatura


class CandidaturaRepository:
    def _from_row(self, row):
        return Candidatura(*row) if row else None

    def list_all(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM candidaturas ORDER BY id_candidatura")
            return [Candidatura(*row) for row in cursor.fetchall()]

    def list_by_estudante(self, id_estudante):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM candidaturas WHERE id_estudante = %s ORDER BY data_inscricao DESC",
                (id_estudante,),
            )
            return [Candidatura(*row) for row in cursor.fetchall()]

    def get_by_id(self, id_candidatura):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM candidaturas WHERE id_candidatura = %s", (id_candidatura,))
            return self._from_row(cursor.fetchone())

    def find_by_edital_estudante(self, id_edital, id_estudante):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM candidaturas
                   WHERE id_edital = %s AND id_estudante = %s
                   ORDER BY id_candidatura DESC
                   LIMIT 1""",
                (id_edital, id_estudante),
            )
            return self._from_row(cursor.fetchone())

    def create(self, payload):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO candidaturas
                   (id_edital, id_estudante, id_turma, data_inscricao, ira, nota_disciplina, status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)
                   RETURNING *""",
                (
                    payload["id_edital"],
                    payload["id_estudante"],
                    payload["id_turma"],
                    payload["data_inscricao"],
                    payload["ira"],
                    payload["nota_disciplina"],
                    payload["status"],
                ),
            )
            conn.commit()
            return self._from_row(cursor.fetchone())

    def update(self, id_candidatura, payload):
        if "status" not in payload:
            raise ValueError("Somente atualizacao de status e suportada para candidaturas.")
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE candidaturas SET status = %s WHERE id_candidatura = %s RETURNING *",
                (payload["status"], id_candidatura),
            )
            conn.commit()
            return self._from_row(cursor.fetchone())

    def count_pendentes(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM candidaturas WHERE status IN ('INSCRITA', 'EM_ANALISE')")
            return cursor.fetchone()[0]
