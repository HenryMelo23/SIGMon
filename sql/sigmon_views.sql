-- SIGMon - Views
-- Executar APOS sigmon_create.sql

-- Lista todos os monitores com alocacao ativa, a disciplina e a carga horaria.
CREATE OR REPLACE VIEW vw_monitores_ativos AS
SELECT
    u.id_usuario,
    u.nome,
    u.email,
    d.nome                  AS disciplina,
    a.data_inicio,
    a.data_fim,
    a.carga_horaria_semanal,
    a.status
FROM usuarios u
JOIN alocacoes_monitores a ON a.id_monitor = u.id_usuario
JOIN disciplinas d         ON d.id_disciplina = a.id_disciplina
WHERE u.ativo = TRUE
  AND a.status = 'ATIVA';

-- Consolida horas validadas por monitor e dados bancarios para o setor financeiro.
CREATE OR REPLACE VIEW vw_financeiro_frequencias_validadas AS
SELECT
    u.id_usuario,
    u.nome                      AS monitor,
    db.banco,
    db.agencia,
    db.conta,
    db.tipo_conta,
    db.chave_pix,
    SUM(rf.horas)               AS total_horas_validadas,
    COUNT(rf.id_frequencia)     AS total_registros
FROM usuarios u
JOIN alocacoes_monitores am  ON am.id_monitor   = u.id_usuario AND am.status = 'ATIVA'
JOIN registros_frequencia rf ON rf.id_alocacao  = am.id_alocacao AND rf.validado = TRUE
LEFT JOIN dados_bancarios db ON db.id_usuario   = u.id_usuario
GROUP BY u.id_usuario, u.nome, db.banco, db.agencia, db.conta, db.tipo_conta, db.chave_pix;

-- Resumo das avaliacoes por monitor: media de nota e total de sessoes avaliadas.
CREATE OR REPLACE VIEW vw_avaliacoes_monitoria AS
SELECT
    u.id_usuario,
    u.nome                  AS monitor,
    d.nome                  AS disciplina,
    ROUND(AVG(av.nota), 2)  AS media_nota,
    COUNT(av.id_avaliacao)  AS total_avaliacoes
FROM usuarios u
JOIN alocacoes_monitores am ON am.id_monitor    = u.id_usuario
JOIN disciplinas d          ON d.id_disciplina  = am.id_disciplina
JOIN agenda_slots ag        ON ag.id_alocacao   = am.id_alocacao
JOIN sessoes_tutoria st     ON st.id_slot       = ag.id_slot
JOIN avaliacoes_tutoria av  ON av.id_sessao     = st.id_sessao
GROUP BY u.id_usuario, u.nome, d.nome;
