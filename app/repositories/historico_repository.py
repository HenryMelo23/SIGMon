from psycopg2 import errors as pg_errors

from app.database.db import get_connection
from app.models.historico_escolar import HistoricoEscolar
from app.utils.validators import BusinessError

_JOIN = """
    SELECT h.*, d.nome AS disciplina_nome, d.codigo AS disciplina_codigo, u.nome AS estudante_nome
    FROM historico_escolar h
    JOIN disciplinas d ON h.id_disciplina = d.id_disciplina
    JOIN usuarios u ON h.id_estudante = u.id_usuario
"""


class HistoricoRepository:
    def get_by_id(self, id_historico):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(_JOIN + "WHERE h.id_historico = %s", (id_historico,))
            row = cursor.fetchone()
            return HistoricoEscolar(*row) if row else None

    def list_by_estudante(self, id_estudante):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(_JOIN + "WHERE h.id_estudante = %s ORDER BY h.semestre DESC", (id_estudante,))
            return [HistoricoEscolar(*row) for row in cursor.fetchall()]

    def list_pendentes(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(_JOIN + "WHERE h.status = 'PENDENTE' ORDER BY h.data_cadastro")
            return [HistoricoEscolar(*row) for row in cursor.fetchall()]

    def list_by_status(self, status):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(_JOIN + "WHERE h.status = %s ORDER BY h.data_cadastro DESC", (status,))
            return [HistoricoEscolar(*row) for row in cursor.fetchall()]

    def list_aprovadas_by_estudante(self, id_estudante):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                _JOIN + "WHERE h.id_estudante = %s AND h.status = 'APROVADO' ORDER BY h.semestre DESC",
                (id_estudante,)
            )
            return [HistoricoEscolar(*row) for row in cursor.fetchall()]

    def find_ativa_by_estudante_disciplina(self, id_estudante, id_disciplina):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_historico FROM historico_escolar
                   WHERE id_estudante = %s AND id_disciplina = %s
                   AND status IN ('PENDENTE', 'APROVADO')""",
                (id_estudante, id_disciplina)
            )
            return cursor.fetchone() is not None

    def find_aprovada_by_estudante_disciplina(self, id_estudante, id_disciplina):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_historico FROM historico_escolar
                   WHERE id_estudante = %s AND id_disciplina = %s AND status = 'APROVADO'""",
                (id_estudante, id_disciplina)
            )
            return cursor.fetchone() is not None

    def get_documento(self, id_documento):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT conteudo FROM documentos_anexos WHERE id_documento = %s", (id_documento,))
            row = cursor.fetchone()
            return row[0] if row else None

    def save_documento(self, id_usuario, nome_arquivo, conteudo):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO documentos_anexos (id_usuario, nome_arquivo, tipo_documento, mime_type, conteudo)
                   VALUES (%s, %s, 'Historico Escolar', 'application/pdf', %s)
                   RETURNING id_documento""",
                (id_usuario, nome_arquivo, conteudo)
            )
            conn.commit()
            return cursor.fetchone()[0]

    def create(self, payload):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO historico_escolar (id_estudante, id_disciplina, id_documento, mencao, semestre)
                       VALUES (%s, %s, %s, %s, %s)
                       RETURNING id_historico""",
                    (
                        payload["id_estudante"],
                        payload["id_disciplina"],
                        payload["id_documento"],
                        payload["mencao"],
                        payload["semestre"],
                    )
                )
                conn.commit()
                return cursor.fetchone()[0]
        except pg_errors.UniqueViolation:
            raise BusinessError("Você já cadastrou essa disciplina neste semestre.")

    def update(self, id_historico, payload):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE historico_escolar
                   SET mencao = %s, semestre = %s, status = 'PENDENTE', justificativa = NULL
                   WHERE id_historico = %s""",
                (payload["mencao"], payload["semestre"], id_historico)
            )
            if payload.get("id_documento"):
                cursor.execute(
                    "UPDATE historico_escolar SET id_documento = %s WHERE id_historico = %s",
                    (payload["id_documento"], id_historico)
                )
            conn.commit()

    def update_status(self, id_historico, status, justificativa=None):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE historico_escolar SET status = %s, justificativa = %s WHERE id_historico = %s",
                (status, justificativa, id_historico)
            )
            conn.commit()

    def delete(self, id_historico):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM historico_escolar WHERE id_historico = %s", (id_historico,))
            conn.commit()
