-- SIGMon - Procedures
-- Executar APOS sigmon_create.sql

-- ============================================================
-- PROCEDURE 1: aprova candidatura e cria alocacao em uma transacao
-- Uso: CALL aprovar_candidatura_e_alocar(id_cand, data_ini, data_fim, carga, id_prof);
-- ============================================================

CREATE OR REPLACE PROCEDURE aprovar_candidatura_e_alocar(
    p_candidatura_id      INTEGER,
    p_data_inicio         DATE,
    p_data_fim            DATE,
    p_carga_horaria       INTEGER,
    p_id_professor        INTEGER
)
LANGUAGE plpgsql AS $$
DECLARE
    v_candidatura candidaturas%ROWTYPE;
    v_disciplina_id INTEGER;
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

    SELECT id_departamento INTO v_disciplina_id
    FROM editais
    WHERE id_edital = v_candidatura.id_edital;

    UPDATE candidaturas
    SET status = 'APROVADA'
    WHERE id_candidatura = p_candidatura_id;

    INSERT INTO alocacoes_monitores (
        id_candidatura,
        id_monitor,
        id_disciplina,
        id_professor,
        data_inicio,
        data_fim,
        carga_horaria_semanal,
        status
    ) VALUES (
        p_candidatura_id,
        v_candidatura.id_estudante,
        v_disciplina_id,
        p_id_professor,
        p_data_inicio,
        p_data_fim,
        p_carga_horaria,
        'ATIVA'
    );

    INSERT INTO auditoria (id_usuario, acao, entidade, detalhes)
    VALUES (
        p_id_professor,
        'APROVAR_CANDIDATURA',
        'candidaturas',
        'Candidatura ' || p_candidatura_id || ' aprovada. Alocacao criada para monitor ' || v_candidatura.id_estudante
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
