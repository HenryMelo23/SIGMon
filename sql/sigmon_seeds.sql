-- SIGMon - Dados iniciais para demonstracao
-- Executar APOS sigmon_create.sql
-- Senha de todos os usuarios: 123456

-- ============================================================
-- DEPARTAMENTOS
-- ============================================================

INSERT INTO departamentos (id_departamento, nome, sigla, email) VALUES
(1, 'Departamento de Ciencia da Computacao', 'CIC', 'secretaria@cic.unb.br'),
(2, 'Departamento de Matematica', 'MAT', 'mat@unb.br'),
(3, 'Departamento de Fisica', 'FIS', 'fis@unb.br'),
(4, 'Departamento de Estatistica', 'EST', 'est@unb.br'),
(5, 'Departamento de Engenharia Eletrica', 'ENE', 'ene@unb.br');

SELECT setval('departamentos_id_departamento_seq', 5);

-- ============================================================
-- USUARIOS
-- ============================================================

INSERT INTO usuarios (id_usuario, id_departamento, nome, email, matricula, papel, senha_hash, ativo, data_cadastro) VALUES
(1, 1, 'Ana Beatriz Martins', 'admin@unb.br', 'ADM001', 'ADMINISTRADOR', '123456', TRUE, '2026-01-10'),
(2, 1, 'Pedro Alves', 'pedro@unb.br', '230078934', 'ESTUDANTE', '123456', TRUE, '2026-02-12'),
(3, 1, 'Prof. Caetano Silva', 'professor@unb.br', 'DOC742', 'PROFESSOR', '123456', TRUE, '2026-01-11'),
(4, 1, 'Amanda Souza', 'amanda@unb.br', '231045678', 'ESTUDANTE', '123456', TRUE, '2026-02-02'),
(5, 1, 'Camila Rocha', 'financeiro@unb.br', 'FIN018', 'FINANCEIRO', '123456', TRUE, '2026-01-20'),
(6, 1, 'Rafael Nogueira', 'rafael@unb.br', '211098765', 'MONITOR', '123456', TRUE, '2026-02-08'),
(7, 1, 'Beatriz Oliveira', 'beatriz@unb.br', '220034512', 'ESTUDANTE', '123456', TRUE, '2026-02-10'),
(8, 1, 'Prof. Mariana Costa', 'mariana@unb.br', 'DOC801', 'PROFESSOR', '123456', TRUE, '2026-01-15');

SELECT setval('usuarios_id_usuario_seq', 8);

-- ============================================================
-- DISCIPLINAS
-- ============================================================

INSERT INTO disciplinas (id_disciplina, id_departamento, codigo, nome, creditos) VALUES
(1, 1, 'CIC0097', 'Banco de Dados', 4),
(2, 1, 'CIC0105', 'Estruturas de Dados', 4),
(3, 1, 'CIC0004', 'Algoritmos e Programacao', 4),
(4, 1, 'CIC0210', 'Programacao Orientada a Objetos', 4),
(5, 2, 'MAT0025', 'Calculo 1', 4);

SELECT setval('disciplinas_id_disciplina_seq', 5);

-- ============================================================
-- HORARIOS
-- ============================================================

INSERT INTO horarios (id_horario, codigo, descricao, turno, ativo) VALUES
(1, '246M34', 'Seg/Qua/Sex 10h-11h50', 'M', TRUE),
(2, '35T23', 'Ter/Qui 14h-15h50', 'T', TRUE),
(3, '6M1234', 'Sex 08h-11h50', 'M', TRUE),
(4, '46T45', 'Qua/Sex 16h-17h50', 'T', TRUE),
(5, '35M12', 'Ter/Qui 08h-09h50', 'M', TRUE);

SELECT setval('horarios_id_horario_seq', 5);

-- ============================================================
-- TURMAS
-- ============================================================

INSERT INTO turmas (id_turma, id_disciplina, id_professor, semestre, codigo_turma, id_horario, sala, vagas_monitor) VALUES
(1, 1, 3, '2026.1', 'T01', 1, 'PJC BT 036', 1),
(2, 2, 3, '2026.1', 'T01', 2, 'LAB CIC 02', 1),
(3, 3, 8, '2026.1', 'T01', 3, 'PJC BT 044', 2),
(4, 4, 3, '2026.1', 'T01', 4, 'LAB CIC 01', 1),
(5, 3, 8, '2026.1', 'T02', 5, 'PJC BT 048', 1);

SELECT setval('turmas_id_turma_seq', 5);

-- ============================================================
-- EDITAIS
-- ============================================================

INSERT INTO editais (id_edital, id_departamento, titulo, descricao, semestre, data_inicio, data_fim, nota_minima) VALUES
(1, 1, 'Edital de Monitoria CIC 2026.1', 'Selecao para monitoria remunerada e voluntaria.', '2026.1', '2026-06-01', '2026-07-20', 'MS'),
(2, 1, 'Edital Complementar Banco de Dados', 'Chamada complementar para apoio em laboratorio.', '2026.1', '2026-04-01', '2026-04-30', 'MS'),
(3, 1, 'Edital de Monitoria CIC 2026.2', 'Selecao para o segundo semestre de 2026.', '2026.2', '2026-07-01', '2026-08-10', 'MS'),
(4, 1, 'Edital de Monitoria CIC 2026.1 Extra', 'Chamada extra para disciplinas com alta demanda.', '2026.1', '2026-05-01', '2026-06-15', 'MS'),
(5, 1, 'Edital Algoritmos 2026.1', 'Apoio especifico para a disciplina de Algoritmos.', '2026.1', '2026-06-10', '2026-07-10', 'SS');

SELECT setval('editais_id_edital_seq', 5);

-- ============================================================
-- INSCRICOES_TURMAS
-- Pedro ainda nao esta inscrito em Banco de Dados T01; ele faz isso ao vivo.
-- ============================================================

INSERT INTO inscricoes_turmas (id_inscricao, id_estudante, id_turma, data_inscricao, status) VALUES
(1, 4, 1, '2026-06-01', 'APROVADA'),
(2, 4, 2, '2026-06-01', 'APROVADA'),
(3, 7, 1, '2026-06-02', 'APROVADA'),
(4, 7, 3, '2026-06-03', 'PENDENTE'),
(5, 2, 3, '2026-06-04', 'APROVADA');

SELECT setval('inscricoes_turmas_id_inscricao_seq', 5);

-- ============================================================
-- CANDIDATURAS
-- IDs 10..14 deixam a candidatura feita ao vivo pelo Pedro nascer como id 2.
-- ============================================================

INSERT INTO candidaturas (id_candidatura, id_edital, id_estudante, id_turma, data_inscricao, ira, nota_disciplina, status) VALUES
(10, 1, 6, 1, '2026-06-05', 4.35, 'SS', 'APROVADA'),
(11, 1, 7, 3, '2026-06-07', 4.20, 'MS', 'INSCRITA'),
(12, 3, 6, 3, '2026-07-02', 4.35, 'SS', 'APROVADA'),
(13, 4, 7, 5, '2026-05-10', 4.10, 'MS', 'APROVADA'),
(14, 5, 4, 3, '2026-06-11', 4.50, 'SS', 'APROVADA');

SELECT setval('candidaturas_id_candidatura_seq', 1);

-- ============================================================
-- ALOCACOES_MONITORES
-- Rafael esta ativo em Banco de Dados T01 para os passos de agenda.
-- ============================================================

INSERT INTO alocacoes_monitores (id_alocacao, id_candidatura, id_monitor, id_disciplina, id_turma, id_professor, data_inicio, data_fim, carga_horaria_semanal, status) VALUES
(1, 10, 6, 1, 1, 3, '2026-07-01', '2026-11-30', 12, 'ATIVA'),
(2, 11, 7, 3, 3, 8, '2026-07-01', '2026-11-30', 8, 'SUSPENSA'),
(3, 12, 6, 3, 3, 8, '2026-08-01', '2026-12-15', 10, 'ATIVA'),
(4, 13, 7, 5, 5, 8, '2026-06-01', '2026-10-31', 8, 'ATIVA'),
(5, 14, 4, 3, 3, 8, '2026-07-01', '2026-11-30', 12, 'ENCERRADA');

SELECT setval('alocacoes_monitores_id_alocacao_seq', 5);

-- ============================================================
-- DADOS_BANCARIOS
-- ============================================================

INSERT INTO dados_bancarios (id_dado_bancario, id_usuario, banco, agencia, conta, tipo_conta, chave_pix, atualizado_em) VALUES
(1, 6, 'Banco do Brasil', '3602-1', '128934-5', 'CORRENTE', 'rafael@aluno.unb.br', '2026-05-02'),
(2, 7, 'Caixa Economica', '0421-8', '993421-0', 'POUPANCA', 'beatriz@aluno.unb.br', '2026-05-03'),
(3, 4, 'Bradesco', '1234-5', '567890-1', 'CORRENTE', 'amanda@aluno.unb.br', '2026-05-04'),
(4, 2, 'Itau', '9876-3', '112233-4', 'CORRENTE', 'pedro@aluno.unb.br', '2026-05-05'),
(5, 5, 'Nubank', '0001-9', '445566-7', 'CORRENTE', 'camila.financeiro@unb.br', '2026-05-06');

SELECT setval('dados_bancarios_id_dado_bancario_seq', 5);

-- ============================================================
-- DOCUMENTOS_ANEXOS
-- ============================================================

INSERT INTO documentos_anexos (id_documento, id_usuario, id_edital, id_candidatura, nome_arquivo, tipo_documento, mime_type, conteudo, data_upload) VALUES
(1, 6, 1, 10, 'historico_rafael.pdf', 'Historico Escolar', 'application/pdf', decode('255044462d312e34', 'hex'), '2026-06-05'),
(2, 7, 1, 11, 'historico_beatriz.pdf', 'Historico Escolar', 'application/pdf', decode('255044462d312e34', 'hex'), '2026-06-07'),
(3, 4, 5, 14, 'historico_amanda.pdf', 'Historico Escolar', 'application/pdf', decode('255044462d312e34', 'hex'), '2026-06-11'),
(4, 1, 1, NULL, 'edital_cic_2026_1.pdf', 'Edital Publicado', 'application/pdf', decode('255044462d312e34', 'hex'), '2026-06-01'),
(5, 2, NULL, NULL, 'historico_pedro_base.pdf', 'Historico Escolar', 'application/pdf', decode('255044462d312e34', 'hex'), '2026-01-15'),
(6, 6, NULL, NULL, 'historico_rafael_escolar.pdf', 'Historico Escolar', 'application/pdf', decode('255044462d312e34', 'hex'), '2026-01-10'),
(7, 7, NULL, NULL, 'historico_beatriz_escolar.pdf', 'Historico Escolar', 'application/pdf', decode('255044462d312e34', 'hex'), '2026-01-12'),
(8, 4, NULL, NULL, 'historico_amanda_escolar.pdf', 'Historico Escolar', 'application/pdf', decode('255044462d312e34', 'hex'), '2026-01-10'),
(9, 8, NULL, NULL, 'historico_mariana_escolar.pdf', 'Historico Escolar', 'application/pdf', decode('255044462d312e34', 'hex'), '2026-01-10');

SELECT setval('documentos_anexos_id_documento_seq', 9);

-- ============================================================
-- HISTORICO_ESCOLAR
-- Pedro ainda nao tem ED aprovado; ele cadastra ao vivo com SS + PDF.
-- ============================================================

INSERT INTO historico_escolar (id_historico, id_estudante, id_disciplina, id_documento, mencao, semestre, status, data_cadastro) VALUES
(1, 6, 1, 6, 'SS', '2025.1', 'APROVADO', '2026-01-10'),
(2, 6, 2, 6, 'MS', '2025.1', 'APROVADO', '2026-01-10'),
(3, 7, 2, 7, 'SS', '2025.1', 'APROVADO', '2026-01-12'),
(4, 4, 1, 8, 'SS', '2025.1', 'APROVADO', '2026-01-10'),
(5, 4, 3, 8, 'SS', '2025.1', 'APROVADO', '2026-01-10'),
(6, 7, 5, 7, 'MS', '2025.2', 'APROVADO', '2026-01-15'),
(7, 4, 2, 8, 'MM', '2025.2', 'PENDENTE', '2026-06-01'),
(8, 2, 1, 5, 'MS', '2025.2', 'APROVADO', '2026-01-15');

SELECT setval('historico_escolar_id_historico_seq', 8);

-- ============================================================
-- AGENDA_SLOTS
-- Slots 1 e 2 ja foram avaliados por Amanda; slot 3 fica disponivel
-- para Pedro reservar ao vivo com Rafael.
-- ============================================================

INSERT INTO agenda_slots (id_slot, id_alocacao, data_slot, hora_inicio, hora_fim, local_atendimento, modalidade, reservado) VALUES
(1, 1, '2026-07-07', '14:00', '15:00', 'Laboratorio CIC 02', 'PRESENCIAL', TRUE),
(2, 1, '2026-07-08', '09:00', '10:00', 'Google Meet', 'ONLINE', TRUE),
(3, 1, '2026-07-12', '16:00', '17:00', 'Laboratorio CIC 02', 'PRESENCIAL', FALSE),
(4, 3, '2026-07-11', '14:00', '15:00', 'Laboratorio CIC 03', 'HIBRIDA', TRUE),
(5, 4, '2026-07-13', '10:00', '11:00', 'Microsoft Teams', 'ONLINE', TRUE),
(6, 3, '2026-07-14', '15:00', '16:00', 'Laboratorio CIC 03', 'PRESENCIAL', TRUE);

SELECT setval('agenda_slots_id_slot_seq', 6);

-- ============================================================
-- SESSOES_TUTORIA
-- ============================================================

INSERT INTO sessoes_tutoria (id_sessao, id_slot, id_estudante, assunto, observacoes, realizada, data_registro) VALUES
(1, 1, 4, 'Modelagem ER', 'Duvidas sobre cardinalidade e normalizacao.', TRUE, '2026-07-07'),
(2, 2, 4, 'SQL Joins', 'Atendimento concluido com exercicios praticos.', TRUE, '2026-07-08'),
(3, 4, 7, 'Algoritmos de Busca', 'Busca linear e binaria com exemplos.', TRUE, '2026-07-11'),
(4, 5, 2, 'Calculo de limites', 'Duvidas iniciais.', TRUE, '2026-07-13'),
(5, 6, 7, 'Subconsultas', 'Exercicios de revisao.', TRUE, '2026-07-14');

SELECT setval('sessoes_tutoria_id_sessao_seq', 5);

-- ============================================================
-- REGISTROS_FREQUENCIA
-- ============================================================

INSERT INTO registros_frequencia (id_frequencia, id_alocacao, data_atividade, horas, descricao, validado, id_professor_validador) VALUES
(1, 1, '2026-07-07', 2.0, 'Atendimento sobre modelagem ER e normalizacao.', TRUE, 3),
(2, 1, '2026-07-08', 1.5, 'Preparacao de material de apoio para SQL.', TRUE, 3),
(3, 3, '2026-07-09', 2.0, 'Atendimento sobre algoritmos.', TRUE, 8),
(4, 4, '2026-07-10', 1.0, 'Revisao de exercicios.', FALSE, NULL),
(5, 3, '2026-07-11', 2.5, 'Preparacao de lista de exercicios.', FALSE, NULL);

SELECT setval('registros_frequencia_id_frequencia_seq', 5);

-- ============================================================
-- AVALIACOES_TUTORIA
-- Amanda ja avaliou Rafael em duas sessoes de BD; a avaliacao ao vivo
-- do Pedro deve elevar o total da view para 3.
-- ============================================================

INSERT INTO avaliacoes_tutoria (id_avaliacao, id_sessao, id_estudante, nota, comentario, data_avaliacao) VALUES
(1, 1, 4, 5, 'Atendimento muito claro e objetivo.', '2026-07-07'),
(2, 2, 4, 4, 'Boa explicacao sobre SQL Joins.', '2026-07-08'),
(3, 5, 7, 5, 'Exemplos ajudaram bastante.', '2026-07-08'),
(4, 3, 7, 4, 'Aguardando conclusao da sessao.', '2026-07-09'),
(5, 4, 2, 4, 'Aproveitei bem a sessao.', '2026-07-13');

SELECT setval('avaliacoes_tutoria_id_avaliacao_seq', 5);
