from app.database.db import get_connection
from app.models.candidatura import Candidatura

_JOIN = """
    SELECT c.*, u.nome AS estudante_nome, t.codigo_turma, d.nome AS disciplina_nome
    FROM candidaturas c
    JOIN usuarios u ON c.id_estudante = u.id_usuario
    JOIN turmas t ON c.id_turma = t.id_turma
    JOIN disciplinas d ON t.id_disciplina = d.id_disciplina
    JOIN editais e ON c.id_edital = e.id_edital
"""


class CandidaturaRepository:
    def count_pendentes(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM candidaturas WHERE status IN ('INSCRITA', 'EM_ANALISE')")
            return cursor.fetchone()[0]
    
    def find_aprovada_semestre(self, id_estudante, semestre):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT c.id_candidatura FROM candidaturas c
                JOIN editais e ON c.id_edital = e.id_edital
                WHERE c.id_estudante = %s
                AND e.semestre = %s
                AND c.status = 'APROVADA'
                """,
              (id_estudante, semestre)
          )
            return cursor.fetchone() is not None
        
    
    def find_by_edital_estudante_turma(self, id_edital, id_estudante, id_turma):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id_candidatura FROM candidaturas
                WHERE id_edital = %s AND id_estudante = %s AND id_turma = %s
                """,
              (id_edital, id_estudante, id_turma)
          )
            return cursor.fetchone() is not None 
    
    
    def list_semestres(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT DISTINCT e.semestre FROM editais e
                JOIN candidaturas c ON c.id_edital = e.id_edital
                ORDER BY e.semestre DESC
                """
            )
            return [row[0] for row in cursor.fetchall()]

    def list_all(self, semestre=None, status=None):
        with get_connection() as conn:
            cursor = conn.cursor()
            conditions = []
            params = []
            if semestre:
                conditions.append("e.semestre = %s")
                params.append(semestre)
            if status:
                conditions.append("c.status = %s")
                params.append(status)
            where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
            cursor.execute(f"{_JOIN}{where} ORDER BY c.data_inscricao DESC", params)
            return [Candidatura(*row) for row in cursor.fetchall()]

    def list_by_estudante(self, id_estudante, semestre=None, status=None):
        with get_connection() as conn:
            cursor = conn.cursor()
            conditions = ["c.id_estudante = %s"]
            params = [id_estudante]
            if semestre:
                conditions.append("e.semestre = %s")
                params.append(semestre)
            if status:
                conditions.append("c.status = %s")
                params.append(status)
            where = "WHERE " + " AND ".join(conditions)
            cursor.execute(f"{_JOIN}{where} ORDER BY c.data_inscricao DESC", params)
            return [Candidatura(*row) for row in cursor.fetchall()]

    def list_by_professor(self, id_professor, semestre=None, status=None):
        with get_connection() as conn:
            cursor = conn.cursor()
            conditions = ["t.id_professor = %s"]
            params = [id_professor]
            if semestre:
                conditions.append("e.semestre = %s")
                params.append(semestre)
            if status:
                conditions.append("c.status = %s")
                params.append(status)
            where = "WHERE " + " AND ".join(conditions)
            cursor.execute(f"{_JOIN}{where} ORDER BY c.data_inscricao DESC", params)
            return [Candidatura(*row) for row in cursor.fetchall()]

    def count_aprovadas_turma(self, id_turma, semestre):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT COUNT(*) FROM candidaturas c
                JOIN editais e ON c.id_edital = e.id_edital
                WHERE c.id_turma = %s AND c.status = 'APROVADA' AND e.semestre = %s
                """,
                (id_turma, semestre)
            )
            return cursor.fetchone()[0]

    def cancel_outras(self, id_estudante, semestre, exceto_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE candidaturas c
                SET status = 'CANCELADA'
                FROM editais e
                WHERE c.id_edital = e.id_edital
                  AND c.id_estudante = %s
                  AND e.semestre = %s
                  AND c.id_candidatura != %s
                  AND c.status IN ('INSCRITA', 'EM_ANALISE')
                """,
                (id_estudante, semestre, exceto_id)
            )
            conn.commit()

    def update_status(self, id_candidatura, status):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE candidaturas SET status = %s WHERE id_candidatura = %s",
                (status, id_candidatura)
            )
            conn.commit()

    def get_by_id(self, id_candidatura):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(_JOIN + "WHERE c.id_candidatura = %s", (id_candidatura,))
            row = cursor.fetchone()
            return Candidatura(*row) if row else None

    def create(self, payload):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO candidaturas(id_edital, id_estudante, id_turma, data_inscricao, ira, nota_disciplina, status)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                RETURNING *
                """, 
                (
                    payload["id_edital"],
                    payload["id_estudante"],
                    payload["id_turma"],
                    payload["data_inscricao"],
                    payload["ira"],
                    payload["nota_disciplina"],
                    payload["status"],     
                )
            )
            conn.commit()
            row = cursor.fetchone()
            return Candidatura(*row)