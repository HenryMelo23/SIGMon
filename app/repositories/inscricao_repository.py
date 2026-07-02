from psycopg2 import errors as pg_errors

from app.database.db import get_connection
from app.models.inscricao_turma import InscricaoTurma
from app.utils.validators import BusinessError

_JOIN = """
    SELECT i.*, u.nome AS estudante_nome, t.codigo_turma, d.nome AS disciplina_nome, t.semestre
    FROM inscricoes_turmas i
    JOIN usuarios u ON i.id_estudante = u.id_usuario
    JOIN turmas t ON i.id_turma = t.id_turma
    JOIN disciplinas d ON t.id_disciplina = d.id_disciplina
"""


class InscricaoRepository:
    def get_by_id(self, id_inscricao):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(_JOIN + "WHERE i.id_inscricao = %s", (id_inscricao,))
            row = cursor.fetchone()
            return InscricaoTurma(*row) if row else None

    def list_by_estudante(self, id_estudante):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                _JOIN + "WHERE i.id_estudante = %s ORDER BY t.semestre DESC, d.nome",
                (id_estudante,)
            )
            return [InscricaoTurma(*row) for row in cursor.fetchall()]

    def list_pendentes(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(_JOIN + "WHERE i.status = 'PENDENTE' ORDER BY i.data_cadastro")
            return [InscricaoTurma(*row) for row in cursor.fetchall()]

    def list_by_status(self, status):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                _JOIN + "WHERE i.status = %s ORDER BY i.data_cadastro DESC",
                (status,)
            )
            return [InscricaoTurma(*row) for row in cursor.fetchall()]

    def find_ativa_by_estudante_turma(self, id_estudante, id_turma):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_inscricao FROM inscricoes_turmas
                   WHERE id_estudante = %s AND id_turma = %s
                   AND status IN ('PENDENTE', 'APROVADA')""",
                (id_estudante, id_turma)
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
                   VALUES (%s, %s, 'Comprovante de Matrícula', 'application/pdf', %s)
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
                    """INSERT INTO inscricoes_turmas (id_estudante, id_turma, id_documento)
                       VALUES (%s, %s, %s)
                       RETURNING id_inscricao""",
                    (payload["id_estudante"], payload["id_turma"], payload["id_documento"])
                )
                conn.commit()
                return cursor.fetchone()[0]
        except pg_errors.UniqueViolation:
            raise BusinessError("Você já possui uma inscrição ativa nessa turma.")

    def update_status(self, id_inscricao, status, justificativa=None):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE inscricoes_turmas SET status = %s, justificativa = %s WHERE id_inscricao = %s",
                (status, justificativa, id_inscricao)
            )
            conn.commit()

    def delete(self, id_inscricao):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM inscricoes_turmas WHERE id_inscricao = %s", (id_inscricao,))
            conn.commit()
