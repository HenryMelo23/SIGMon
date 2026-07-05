-- SIGMon - Views
-- Executar APOS sigmon_create.sql

-- Resumo das avaliacoes por monitor: media de nota e total de sessoes avaliadas por disciplina.
-- Usada na tela de avaliacoes do MONITOR para exibir seu desempenho consolidado.
--
-- Uso:
--   SELECT * FROM vw_avaliacoes_monitoria;
--   SELECT * FROM vw_avaliacoes_monitoria WHERE id_usuario = 6;
CREATE OR REPLACE VIEW vw_avaliacoes_monitoria AS
SELECT
    u.id_usuario,
    u.nome                  AS monitor,
    d.nome                  AS disciplina,
    ROUND(AVG(av.nota), 2)  AS media_nota,
    COUNT(av.id_avaliacao)  AS total_avaliacoes
FROM usuarios u
JOIN alocacoes_monitores am ON am.id_monitor   = u.id_usuario
JOIN disciplinas d          ON d.id_disciplina = am.id_disciplina
JOIN agenda_slots ag        ON ag.id_alocacao  = am.id_alocacao
JOIN sessoes_tutoria st     ON st.id_slot      = ag.id_slot
JOIN avaliacoes_tutoria av  ON av.id_sessao    = st.id_sessao
GROUP BY u.id_usuario, u.nome, d.nome;

GRANT SELECT ON vw_avaliacoes_monitoria TO sigmon_user;
