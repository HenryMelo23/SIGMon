-- SIGMon - Procedures
-- Executar APOS sigmon_create.sql

-- ============================================================
-- PROCEDURE 1: aprova candidatura, transforma o estudante em monitor
-- e cria a alocacao ativa em uma transacao.
-- Uso: CALL aprovar_candidatura_e_alocar(id_candidatura, id_professor);
-- ============================================================

CREATE OR REPLACE PROCEDURE aprovar_candidatura_e_alocar(
    p_candidatura_id INTEGER,
    p_id_professor   INTEGER
)
LANGUAGE plpgsql AS $$
DECLARE
    v_candidatura candidaturas%ROWTYPE;
    v_turma turmas%ROWTYPE;
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

    SELECT * INTO v_turma
    FROM turmas
    WHERE id_turma = v_candidatura.id_turma;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Turma % nao encontrada', v_candidatura.id_turma;
    END IF;

    UPDATE candidaturas
    SET status = 'APROVADA'
    WHERE id_candidatura = p_candidatura_id;

    UPDATE usuarios
    SET papel = 'MONITOR'
    WHERE id_usuario = v_candidatura.id_estudante
      AND papel <> 'MONITOR';

    INSERT INTO alocacoes_monitores (
        id_candidatura,
        id_monitor,
        id_disciplina,
        id_turma,
        id_professor,
        data_inicio,
        data_fim,
        carga_horaria_semanal,
        status
    ) VALUES (
        p_candidatura_id,
        v_candidatura.id_estudante,
        v_turma.id_disciplina,
        v_turma.id_turma,
        p_id_professor,
        CURRENT_DATE,
        CURRENT_DATE + 120,
        12,
        'ATIVA'
    );

    INSERT INTO auditoria (id_usuario, acao, entidade, detalhes)
    VALUES (
        p_id_professor,
        'APROVAR_CANDIDATURA',
        'candidaturas',
        'Candidatura ' || p_candidatura_id || ' aprovada e alocacao criada para usuario ' || v_candidatura.id_estudante
    );
END;
$$;

-- ============================================================
-- PROCEDURE 2: valida em lote os registros de frequencia de uma alocacao
-- Uso: CALL validar_frequencias_alocacao(id_alocacao, id_professor);
-- ============================================================

CREATE OR REPLACE PROCEDURE validar_frequencias_alocacao(
    p_id_alocacao  INTEGER,
    p_id_professor INTEGER
)
LANGUAGE plpgsql AS $$
DECLARE
    v_total INTEGER;
BEGIN
    UPDATE registros_frequencia
    SET validado = TRUE,
        id_professor_validador = p_id_professor
    WHERE id_alocacao = p_id_alocacao
      AND validado = FALSE;

    GET DIAGNOSTICS v_total = ROW_COUNT;

    INSERT INTO auditoria (id_usuario, acao, entidade, detalhes)
    VALUES (
        p_id_professor,
        'VALIDAR_FREQUENCIAS',
        'registros_frequencia',
        v_total || ' registros da alocacao ' || p_id_alocacao || ' validados'
    );
END;
$$;
