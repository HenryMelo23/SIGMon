from app.database.db import get_connection
from app.models.sessao_tutoria import SessaoTutoria


class SessaoRepository:
    def count_nao_realizadas(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sessoes_tutoria WHERE realizada = FALSE")
            return cursor.fetchone()[0]

    def list_all(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sessoes_tutoria ORDER BY data_registro DESC")
            return [SessaoTutoria(*row) for row in cursor.fetchall()]

    def list_by_estudante(self, id_estudante):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM sessoes_tutoria WHERE id_estudante = %s ORDER BY data_registro DESC",
                (id_estudante,)
            )
            return [SessaoTutoria(*row) for row in cursor.fetchall()]

    def list_como_monitor(self, id_monitor):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT st.* FROM sessoes_tutoria st
                   JOIN agenda_slots ag ON st.id_slot = ag.id_slot
                   JOIN alocacoes_monitores am ON ag.id_alocacao = am.id_alocacao
                   WHERE am.id_monitor = %s
                   ORDER BY st.data_registro DESC""",
                (id_monitor,)
            )
            return [SessaoTutoria(*row) for row in cursor.fetchall()]

    def create(self, payload):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO sessoes_tutoria (id_slot, id_estudante, assunto, realizada, data_registro)
                   VALUES (%s, %s, %s, %s, %s)
                   RETURNING id_sessao""",
                (
                    payload["id_slot"],
                    payload["id_estudante"],
                    payload["assunto"],
                    payload.get("realizada", False),
                    payload["data_registro"],
                )
            )
            conn.commit()
            return cursor.fetchone()[0]

    def update(self, id_sessao, payload):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE sessoes_tutoria SET realizada = %s WHERE id_sessao = %s",
                (payload["realizada"], id_sessao)
            )
            conn.commit()
        