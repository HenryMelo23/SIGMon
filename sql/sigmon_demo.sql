-- SIGMon - Scripts para demonstracao na apresentacao
-- Executar no psql ou DBeaver APOS as seeds e os scripts procedure/view/trigger
--
-- Ordem na apresentacao:
--   1. Pedro se candidata ao vivo no sistema -> candidatura id=2 criada
--   2. Rodar BLOCO A (procedure)  -> candidatura aprovada, Pedro vira MONITOR
--   3. Rodar BLOCO B (trigger)    -> auditoria mostra MUDANCA_PAPEL automatica
--   4. Abrir sistema como Carlos  -> rodar BLOCO C (view) / mostrar na tela

-- ============================================================
-- BLOCO A: PROCEDURE aprovar_candidatura_e_alocar
-- ============================================================

-- Passo 1: estado antes da aprovacao
SELECT id_candidatura, id_estudante, id_turma, status
FROM candidaturas
WHERE id_candidatura = 2;

SELECT id_usuario, nome, papel
FROM usuarios
WHERE id_usuario = 5;

-- Passo 2: chamar a procedure (id_aprovador=3 = Prof. Caetano)
--          O sistema chama isso internamente; aqui mostramos a chamada direta
CALL public.aprovar_candidatura_e_alocar(2, 3);

-- Passo 3: estado depois
SELECT id_candidatura, id_estudante, id_turma, status
FROM candidaturas
WHERE id_candidatura = 2;

-- Pedro (id=5) deve aparecer agora como MONITOR
SELECT id_usuario, nome, papel
FROM usuarios
WHERE id_usuario = 5;

SELECT id_alocacao, id_monitor, id_disciplina, id_turma, status
FROM alocacoes_monitores
WHERE id_candidatura = 2;

-- ============================================================
-- BLOCO B: TRIGGER trg_auditoria_mudanca_papel
-- ============================================================

-- O trigger disparou automaticamente quando a procedure alterou o papel do Pedro.
-- Nao e necessario chamar nada — so mostrar o resultado:

SELECT id_auditoria, id_usuario, acao, entidade, detalhes, criado_em
FROM auditoria
ORDER BY criado_em DESC
LIMIT 5;

-- Para mostrar o trigger de forma isolada (sem procedure), pode-se fazer:
-- UPDATE usuarios SET papel = 'ESTUDANTE' WHERE id_usuario = 5;
-- UPDATE usuarios SET papel = 'MONITOR'   WHERE id_usuario = 5;
-- SELECT * FROM auditoria ORDER BY criado_em DESC LIMIT 2;

-- ============================================================
-- BLOCO C: VIEW vw_avaliacoes_monitoria
-- ============================================================

-- Mostra o desempenho de todos os monitores (disponivel para o admin ou internamente)
SELECT id_usuario, monitor, disciplina, media_nota, total_avaliacoes
FROM vw_avaliacoes_monitoria;

-- Filtrando apenas o Rafael Mendes (id=4) — o mesmo dado exibido no sistema
SELECT id_usuario, monitor, disciplina, media_nota, total_avaliacoes
FROM vw_avaliacoes_monitoria
WHERE id_usuario = 4;
