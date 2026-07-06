from app.database.db import get_connection
from app.models.turma import Turma


class TurmaRepository:
    def get_by_id(self, id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT t.*, d.nome AS disciplina_nome, u.nome AS professor_nome, h.codigo AS horario_codigo
                FROM turmas t
                JOIN disciplinas d ON t.id_disciplina = d.id_disciplina
                JOIN usuarios u ON t.id_professor = u.id_usuario
                LEFT JOIN horarios h ON t.id_horario = h.id_horario
                WHERE t.id_turma = %s
                """,
                (id,),
            )
            row = cursor.fetchone()
            if row:
                return Turma(*row)
            return None

    def tem_alocacoes(self, id_turma):
      with get_connection() as conn:
          cursor = conn.cursor()
          cursor.execute("SELECT COUNT(*) FROM alocacoes_monitores WHERE id_turma = %s", (id_turma,))
          return cursor.fetchone()[0] > 0
    
    
    def find_duplicata(self, id_disciplina, semestre, codigo_turma):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM turmas
                   WHERE id_disciplina = %s
                   AND semestre = %s AND codigo_turma = %s""",
                (id_disciplina, semestre, codigo_turma)
            )
            row = cursor.fetchone()
            return Turma(*row) if row else None

    def find_conflito_horario(self, id_professor, semestre, id_horario):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM turmas
                   WHERE id_professor = %s AND semestre = %s AND id_horario = %s""",
                (id_professor, semestre, id_horario)
            )
            row = cursor.fetchone()
            return Turma(*row) if row else None

    def list_by_professor(self, id_professor, semestre=None):
        with get_connection() as conn:
            cursor = conn.cursor()
            if semestre:
                cursor.execute(
                    """
                    SELECT t.*, d.nome AS disciplina_nome, u.nome AS professor_nome, h.codigo AS horario_codigo
                    FROM turmas t
                    JOIN disciplinas d ON t.id_disciplina = d.id_disciplina
                    JOIN usuarios u ON t.id_professor = u.id_usuario
                    LEFT JOIN horarios h ON t.id_horario = h.id_horario
                    WHERE t.id_professor = %s AND t.semestre = %s
                    """,
                    (id_professor, semestre)
                )
            else:
                cursor.execute(
                    """
                    SELECT t.*, d.nome AS disciplina_nome, u.nome AS professor_nome, h.codigo AS horario_codigo
                    FROM turmas t
                    JOIN disciplinas d ON t.id_disciplina = d.id_disciplina
                    JOIN usuarios u ON t.id_professor = u.id_usuario
                    LEFT JOIN horarios h ON t.id_horario = h.id_horario
                    WHERE t.id_professor = %s
                    """,
                    (id_professor,)
                )
            rows = cursor.fetchall()
            return [Turma(*row) for row in rows]

    def list_semestres(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT semestre FROM turmas ORDER BY semestre DESC")
            rows = cursor.fetchall()
            return [row[0] for row in rows]

    def list_all(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT t.*, d.nome AS disciplina_nome, u.nome AS professor_nome, h.codigo AS horario_codigo
                FROM turmas t
                JOIN disciplinas d ON t.id_disciplina = d.id_disciplina
                JOIN usuarios u ON t.id_professor = u.id_usuario
                LEFT JOIN horarios h ON t.id_horario = h.id_horario
                """
            )
            rows = cursor.fetchall()
            return [Turma(*row) for row in rows]

    def list_by_semestre(self, semestre):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT t.*, d.nome AS disciplina_nome, u.nome AS professor_nome, h.codigo AS horario_codigo
                FROM turmas t
                JOIN disciplinas d ON t.id_disciplina = d.id_disciplina
                JOIN usuarios u ON t.id_professor = u.id_usuario
                LEFT JOIN horarios h ON t.id_horario = h.id_horario
                WHERE t.semestre = %s
                """,
                (semestre,)
            )
            rows = cursor.fetchall()
            return [Turma(*row) for row in rows]

    def create(self, payload):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO turmas (id_disciplina, id_professor, semestre, codigo_turma, id_horario, sala, vagas_monitor)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)
                   RETURNING *""",
                (
                    payload["id_disciplina"],
                    payload["id_professor"],
                    payload["semestre"],
                    payload["codigo_turma"],
                    payload["id_horario"],
                    payload["sala"],
                    payload["vagas_monitor"],
                )
            )
            conn.commit()
            row = cursor.fetchone()
            return Turma(*row)

    def update(self, id_turma, payload):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE turmas
                SET id_disciplina=%s, id_professor=%s, semestre=%s, codigo_turma=%s, id_horario=%s, sala=%s, vagas_monitor=%s
                WHERE id_turma=%s
                RETURNING *
                """,
                (
                    payload["id_disciplina"],
                    payload["id_professor"],
                    payload["semestre"],
                    payload["codigo_turma"],
                    payload["id_horario"],
                    payload["sala"],
                    payload["vagas_monitor"],
                    id_turma
                )
            )
            conn.commit()
            row = cursor.fetchone()
            return Turma(*row)

    def delete(self, id_turma):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM turmas WHERE id_turma=%s", (id_turma,))
            conn.commit()
