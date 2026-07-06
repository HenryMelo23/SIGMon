from app.database.db import get_connection
from app.models.avaliacao_tutoria import AvaliacaoTutoria

_JOIN = """
    SELECT av.*,
           u_monitor.nome   AS monitor_nome,
           d.nome           AS disciplina_nome,
           t.codigo_turma,
           u_estudante.nome AS estudante_nome
    FROM avaliacoes_tutoria av
    JOIN sessoes_tutoria st   ON av.id_sessao     = st.id_sessao
    JOIN agenda_slots ag      ON st.id_slot        = ag.id_slot
    JOIN alocacoes_monitores am ON ag.id_alocacao  = am.id_alocacao
    JOIN usuarios u_monitor   ON am.id_monitor     = u_monitor.id_usuario
    JOIN disciplinas d        ON am.id_disciplina  = d.id_disciplina
    JOIN turmas t             ON am.id_turma       = t.id_turma
    JOIN usuarios u_estudante ON av.id_estudante   = u_estudante.id_usuario
"""


class AvaliacaoRepository:
    def count_all(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM avaliacoes_tutoria")
            return cursor.fetchone()[0]

    def count_recebidas_monitor(self, id_monitor):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT COUNT(*) FROM avaliacoes_tutoria av
                JOIN sessoes_tutoria st ON av.id_sessao = st.id_sessao
                JOIN agenda_slots ag ON st.id_slot = ag.id_slot
                JOIN alocacoes_monitores am ON ag.id_alocacao = am.id_alocacao
                WHERE am.id_monitor = %s
                """,
                (id_monitor,)
            )
            return cursor.fetchone()[0]

    def list_all(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(_JOIN + "ORDER BY av.data_avaliacao DESC")
            return [AvaliacaoTutoria(*row) for row in cursor.fetchall()]

    def list_by_estudante(self, id_estudante):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                _JOIN + "WHERE av.id_estudante = %s ORDER BY av.data_avaliacao DESC",
                (id_estudante,)
            )
            return [AvaliacaoTutoria(*row) for row in cursor.fetchall()]

    def list_recebidas_monitor(self, id_monitor):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                _JOIN + "WHERE am.id_monitor = %s ORDER BY av.data_avaliacao DESC",
                (id_monitor,)
            )
            return [AvaliacaoTutoria(*row) for row in cursor.fetchall()]

    def list_by_professor(self, id_professor):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                _JOIN + "WHERE am.id_professor = %s ORDER BY av.data_avaliacao DESC",
                (id_professor,)
            )
            return [AvaliacaoTutoria(*row) for row in cursor.fetchall()]

    def find_by_sessao_estudante(self, id_sessao, id_estudante):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_avaliacao FROM avaliacoes_tutoria WHERE id_sessao = %s AND id_estudante = %s",
                (id_sessao, id_estudante)
            )
            return cursor.fetchone() is not None

    def list_resumo_monitor(self, id_monitor):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT disciplina, media_nota, total_avaliacoes
                   FROM vw_avaliacoes_monitoria
                   WHERE id_usuario = %s""",
                (id_monitor,)
            )
            return [
                {"disciplina": row[0], "media_nota": row[1], "total_avaliacoes": row[2]}
                for row in cursor.fetchall()
            ]

    def create(self, payload):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO avaliacoes_tutoria (id_sessao, id_estudante, nota, comentario, data_avaliacao)
                   VALUES (%s, %s, %s, %s, %s)
                   RETURNING id_avaliacao""",
                (
                    payload["id_sessao"],
                    payload["id_estudante"],
                    payload["nota"],
                    payload.get("comentario", ""),
                    payload["data_avaliacao"],
                )
            )
            conn.commit()
            return cursor.fetchone()[0]
