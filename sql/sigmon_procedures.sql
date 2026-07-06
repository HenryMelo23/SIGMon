-- SIGMon - Procedures
-- Executar APOS sigmon_create.sql

-- ============================================================
-- PROCEDURE: aprova candidatura e cria alocacao em uma transacao
--
-- Centraliza no banco todos os passos de aprovacao:
--   1. Aprova a candidatura
--   2. Cancela outras candidaturas do estudante no mesmo semestre
--   3. Muda o papel do estudante para MONITOR
--   4. Cria ou reativa a alocacao
--   5. Registra auditoria
--
-- As validacoes de negocio (vagas, edital aberto, etc) ficam no Python.
-- Esta procedure garante que os passos de escrita ocorram atomicamente.
--
-- Uso:
--   CALL aprovar_candidatura_e_alocar(id_candidatura, id_aprovador);
--
-- Exemplo com seeds:
--   CALL aprovar_candidatura_e_alocar(3, 2);
-- ============================================================

CREATE OR REPLACE PROCEDURE aprovar_candidatura_e_alocar(
    p_candidatura_id INTEGER,
    p_id_aprovador   INTEGER
)
LANGUAGE plpgsql AS $$
DECLARE
    v_candidatura   candidaturas%ROWTYPE;
    v_id_disciplina INTEGER;
    v_id_professor  INTEGER;
    v_carga         INTEGER;
    v_data_inicio   DATE;
    v_data_fim      DATE;
    v_semestre      VARCHAR(10);
BEGIN
    SELECT * INTO v_candidatura
    FROM candidaturas
    WHERE id_candidatura = p_candidatura_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Candidatura % nao encontrada', p_candidatura_id;
    END IF;

    IF v_candidatura.status NOT IN ('INSCRITA', 'EM_ANALISE') THEN
        RAISE EXCEPTION 'Candidatura % nao pode ser aprovada. Status atual: %',
            p_candidatura_id, v_candidatura.status;
    END IF;

    SELECT t.id_disciplina, t.id_professor, t.carga_horaria_semanal
    INTO v_id_disciplina, v_id_professor, v_carga
    FROM turmas t
    WHERE t.id_turma = v_candidatura.id_turma;

    SELECT e.data_inicio_monitoria, e.data_fim_monitoria, e.semestre
    INTO v_data_inicio, v_data_fim, v_semestre
    FROM editais e
    WHERE e.id_edital = v_candidatura.id_edital;

    UPDATE candidaturas
    SET status = 'APROVADA'
    WHERE id_candidatura = p_candidatura_id;

    UPDATE candidaturas c
    SET status = 'CANCELADA'
    FROM editais e
    WHERE c.id_edital = e.id_edital
      AND c.id_estudante = v_candidatura.id_estudante
      AND e.semestre = v_semestre
      AND c.id_candidatura != p_candidatura_id
      AND c.status IN ('INSCRITA', 'EM_ANALISE');

    UPDATE usuarios
    SET papel = 'MONITOR'
    WHERE id_usuario = v_candidatura.id_estudante;

    IF EXISTS (SELECT 1 FROM alocacoes_monitores WHERE id_candidatura = p_candidatura_id) THEN
        UPDATE alocacoes_monitores
        SET status = 'ATIVA'
        WHERE id_candidatura = p_candidatura_id;
    ELSE
        INSERT INTO alocacoes_monitores (
            id_candidatura, id_monitor, id_disciplina, id_turma,
            id_professor, data_inicio, data_fim, carga_horaria_semanal, status
        ) VALUES (
            p_candidatura_id,
            v_candidatura.id_estudante,
            v_id_disciplina,
            v_candidatura.id_turma,
            v_id_professor,
            v_data_inicio,
            v_data_fim,
            v_carga,
            'ATIVA'
        );
    END IF;

    INSERT INTO auditoria (id_usuario, acao, entidade, detalhes)
    VALUES (
        p_id_aprovador,
        'APROVAR_CANDIDATURA',
        'candidaturas',
        'Candidatura ' || p_candidatura_id || ' aprovada. Monitor: ' || v_candidatura.id_estudante
    );
END;
$$;
