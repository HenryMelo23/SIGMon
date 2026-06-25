-- SIGMon - Dados iniciais (seeds)
-- Executar APOS sigmon_create.sql
-- Cada tabela tem no minimo 5 registros (requisito do projeto)
-- Senhas em texto simples para desenvolvimento. Usar hash em producao.

-- ============================================================
-- DEPARTAMENTOS (5 registros)
-- ============================================================

INSERT INTO departamentos (id_departamento, nome, sigla, email) VALUES
(1, 'Departamento de Ciencia da Computacao', 'CIC',  'secretaria@cic.unb.br'),
(2, 'Departamento de Matematica',             'MAT',  'mat@unb.br'),
(3, 'Departamento de Fisica',                 'FIS',  'fis@unb.br'),
(4, 'Departamento de Estatistica',            'EST',  'est@unb.br'),
(5, 'Departamento de Engenharia Eletrica',    'ENE',  'ene@unb.br');

SELECT setval('departamentos_id_departamento_seq', 5);

-- ============================================================
-- USUARIOS (8 registros)
-- ============================================================

INSERT INTO usuarios (id_usuario, id_departamento, nome, email, matricula, papel, senha_hash, ativo, data_cadastro) VALUES
(1, 1, 'Ana Beatriz Martins',     'admin@unb.br',       'ADM001',    'ADMINISTRADOR', '123456', TRUE,  '2026-01-10'),
(2, 1, 'Prof. Rafael Nogueira',   'professor@unb.br',   'DOC742',    'PROFESSOR',     '123456', TRUE,  '2026-01-11'),
(3, 1, 'Prof. Mariana Costa',     'mariana@unb.br',     'DOC801',    'PROFESSOR',     '123456', TRUE,  '2026-01-15'),
(4, 1, 'Luisa Carvalho',          'estudante@unb.br',   '231045678', 'ESTUDANTE',     '123456', TRUE,  '2026-02-02'),
(5, 1, 'Camila Rocha',            'financeiro@unb.br',  'FIN018',    'FINANCEIRO',    '123456', TRUE,  '2026-01-20'),
(6, 1, 'Mateus Henrique Lima',    'monitor@unb.br',     '211098765', 'MONITOR',       '123456', TRUE,  '2026-02-08'),
(7, 1, 'Beatriz Oliveira',        'beatriz@unb.br',     '220034512', 'ESTUDANTE',     '123456', TRUE,  '2026-02-10'),
(8, 1, 'Pedro Alves',             'pedro@unb.br',       '230078934', 'ESTUDANTE',     '123456', TRUE,  '2026-02-12');

SELECT setval('usuarios_id_usuario_seq', 8);

-- ============================================================
-- DISCIPLINAS (5 registros)
-- ============================================================

INSERT INTO disciplinas (id_disciplina, id_departamento, codigo, nome, creditos) VALUES
(1, 1, 'CIC0097', 'Banco de Dados',                    4),
(2, 1, 'CIC0105', 'Estruturas de Dados',               4),
(3, 1, 'CIC0004', 'Algoritmos e Programacao',          4),
(4, 1, 'CIC0210', 'Programacao Orientada a Objetos',   4),
(5, 2, 'MAT0025', 'Calculo 1',                         4);

SELECT setval('disciplinas_id_disciplina_seq', 5);

-- ============================================================
-- HORARIOS (5 registros)
-- ============================================================

INSERT INTO horarios (id_horario, codigo, descricao, turno, ativo) VALUES
(1, '246M34', 'Seg/Qua/Sex 10h-11h50', 'M', TRUE),
(2, '35T23',  'Ter/Qui 14h-15h50',     'T', TRUE),
(3, '6M1234', 'Sex 08h-11h50',         'M', TRUE),
(4, '46T45',  'Qua/Sex 16h-17h50',     'T', TRUE),
(5, '35M12',  'Ter/Qui 08h-09h50',     'M', TRUE);

SELECT setval('horarios_id_horario_seq', 5);

-- ============================================================
-- TURMAS (5 registros)
-- ============================================================

INSERT INTO turmas (id_turma, id_disciplina, id_professor, semestre, codigo_turma, tipo_turma, id_horario, sala, vagas_monitor) VALUES
(1, 1, 2, '2026.1', 'A', 'TEORICA', 1, 'PJC BT 036', 1),
(2, 2, 2, '2026.1', 'B', 'PRATICA', 2, 'LAB CIC 02', 1),
(3, 3, 3, '2026.1', 'C', 'TEORICA', 3, 'PJC BT 044', 2),
(4, 4, 2, '2026.1', 'A', 'PRATICA', 4, 'LAB CIC 01', 1),
(5, 5, 3, '2026.1', 'A', 'TEORICA', 5, 'MAT IB 007', 1);

SELECT setval('turmas_id_turma_seq', 5);

-- ============================================================
-- EDITAIS (5 registros)
-- ============================================================

INSERT INTO editais (id_edital, id_departamento, titulo, descricao, data_inicio, data_fim, quantidade_vagas, nota_minima) VALUES
(1, 1, 'Edital de Monitoria CIC 2026.1',         'Selecao para monitoria remunerada e voluntaria.',      '2026-06-01', '2026-07-20', 8, 7.00),
(2, 1, 'Edital Complementar Banco de Dados',      'Chamada complementar para apoio em laboratorio.',      '2026-04-01', '2026-04-30', 2, 7.50),
(3, 1, 'Edital de Monitoria CIC 2026.2',          'Selecao para o segundo semestre de 2026.',             '2026-07-01', '2026-08-10', 6, 7.00),
(4, 2, 'Edital de Monitoria MAT 2026.1',          'Monitoria para disciplinas do departamento de MAT.',   '2026-05-01', '2026-06-15', 3, 7.00),
(5, 1, 'Edital Algoritmos 2026.1',                'Apoio especifico para a disciplina de Algoritmos.',    '2026-06-10', '2026-07-10', 2, 8.00);

SELECT setval('editais_id_edital_seq', 5);

-- ============================================================
-- CANDIDATURAS (8 registros)
-- ============================================================

INSERT INTO candidaturas (id_candidatura, id_edital, id_estudante, id_turma, data_inscricao, ira, nota_disciplina, status) VALUES
(1, 1, 6, 1, '2026-06-05', 4.35, 8.7, 'APROVADA'),
(2, 2, 7, 2, '2026-04-08', 4.62, 9.1, 'APROVADA'),
(3, 3, 6, 3, '2026-07-02', 4.35, 8.7, 'APROVADA'),
(4, 4, 8, 5, '2026-05-10', 4.10, 7.8, 'APROVADA'),
(5, 5, 4, 3, '2026-06-11', 4.50, 9.0, 'APROVADA'),
(6, 1, 4, 1, '2026-06-06', 4.50, 8.5, 'EM_ANALISE'),
(7, 2, 8, 2, '2026-04-10', 3.95, 6.8, 'REPROVADA'),
(8, 1, 7, 4, '2026-06-07', 4.20, 7.5, 'INSCRITA');

SELECT setval('candidaturas_id_candidatura_seq', 8);

-- ============================================================
-- ALOCACOES_MONITORES (5 registros)
-- ============================================================

INSERT INTO alocacoes_monitores (id_alocacao, id_candidatura, id_monitor, id_disciplina, id_turma, id_professor, data_inicio, data_fim, carga_horaria_semanal, status) VALUES
(1, 1, 6, 1, 1, 2, '2026-07-01', '2026-11-30', 12, 'ATIVA'),
(2, 2, 7, 2, 2, 2, '2026-05-01', '2026-08-31', 12, 'ATIVA'),
(3, 3, 6, 3, 3, 3, '2026-08-01', '2026-12-15', 10, 'ATIVA'),
(4, 4, 8, 5, 5, 3, '2026-06-01', '2026-10-31',  8, 'ATIVA'),
(5, 5, 4, 3, 3, 3, '2026-07-01', '2026-11-30', 12, 'ENCERRADA');

SELECT setval('alocacoes_monitores_id_alocacao_seq', 5);

-- ============================================================
-- DADOS_BANCARIOS (5 registros)
-- ============================================================

INSERT INTO dados_bancarios (id_dado_bancario, id_usuario, banco, agencia, conta, tipo_conta, chave_pix, atualizado_em) VALUES
(1, 6, 'Banco do Brasil',  '3602-1', '128934-5', 'CORRENTE', 'mateus.lima@aluno.unb.br',   '2026-05-02'),
(2, 7, 'Caixa Economica',  '0421-8', '993421-0', 'POUPANCA', 'beatriz.oliveira@unb.br',    '2026-05-03'),
(3, 4, 'Bradesco',         '1234-5', '567890-1', 'CORRENTE', '231045678',                   '2026-05-04'),
(4, 8, 'Itau',             '9876-3', '112233-4', 'CORRENTE', 'pedro.alves@aluno.unb.br',   '2026-05-05'),
(5, 5, 'Nubank',           '0001-9', '445566-7', 'CORRENTE', 'camila.financeiro@unb.br',   '2026-05-06');

SELECT setval('dados_bancarios_id_dado_bancario_seq', 5);

-- ============================================================
-- DOCUMENTOS_ANEXOS (5 registros)
-- O campo conteudo usa BYTEA para armazenar o binario do arquivo.
-- Aqui usamos o cabecalho magico de um PDF real (%PDF-1.4) como exemplo.
-- ============================================================

INSERT INTO documentos_anexos (id_documento, id_usuario, id_edital, id_candidatura, nome_arquivo, tipo_documento, mime_type, conteudo, data_upload) VALUES
(1, 4, 1, 6, 'historico_luisa.pdf',   'Historico Escolar',   'application/pdf', decode('255044462d312e34', 'hex'), '2026-06-06'),
(2, 6, 1, 1, 'historico_mateus.pdf',  'Historico Escolar',   'application/pdf', decode('255044462d312e34', 'hex'), '2026-06-05'),
(3, 7, 2, 2, 'historico_beatriz.pdf', 'Historico Escolar',   'application/pdf', decode('255044462d312e34', 'hex'), '2026-04-08'),
(4, 1, 1, NULL, 'edital_cic_2026_1.pdf', 'Edital Publicado', 'application/pdf', decode('255044462d312e34', 'hex'), '2026-06-01'),
(5, 8, 4, 4, 'historico_pedro.pdf',   'Historico Escolar',   'application/pdf', decode('255044462d312e34', 'hex'), '2026-05-10');

SELECT setval('documentos_anexos_id_documento_seq', 5);

-- ============================================================
-- AGENDA_SLOTS (5 registros)
-- ============================================================

INSERT INTO agenda_slots (id_slot, id_alocacao, data_slot, hora_inicio, hora_fim, local_atendimento, modalidade, reservado) VALUES
(1, 1, '2026-07-07', '14:00', '15:00', 'Laboratorio CIC 02', 'PRESENCIAL', TRUE),
(2, 1, '2026-07-08', '09:00', '10:00', 'Google Meet',         'ONLINE',     TRUE),
(3, 2, '2026-07-09', '16:00', '17:00', 'Laboratorio CIC 01', 'PRESENCIAL', TRUE),
(4, 2, '2026-07-10', '10:00', '11:00', 'Microsoft Teams',     'ONLINE',     TRUE),
(5, 3, '2026-07-11', '14:00', '15:00', 'Laboratorio CIC 03', 'HIBRIDA',    TRUE);

SELECT setval('agenda_slots_id_slot_seq', 5);

-- ============================================================
-- SESSOES_TUTORIA (5 registros)
-- ============================================================

INSERT INTO sessoes_tutoria (id_sessao, id_slot, id_estudante, assunto, observacoes, realizada, data_registro) VALUES
(1, 1, 4, 'Modelagem ER',         'Duvidas sobre cardinalidade e normalizacao.',     TRUE,  '2026-07-07'),
(2, 2, 4, 'SQL Joins',            'Atendimento concluido com exercicios praticos.',  TRUE,  '2026-07-08'),
(3, 3, 7, 'Arvores Binarias',     'Revisao de busca e insercao em arvores.',         TRUE,  '2026-07-09'),
(4, 4, 8, 'Recursao',             'Exercicios de fatorial e Fibonacci.',             TRUE,  '2026-07-10'),
(5, 5, 4, 'Algoritmos de Busca',  'Busca linear e binaria com exemplos.',            FALSE, '2026-07-11');

SELECT setval('sessoes_tutoria_id_sessao_seq', 5);

-- ============================================================
-- REGISTROS_FREQUENCIA (5 registros)
-- ============================================================

INSERT INTO registros_frequencia (id_frequencia, id_alocacao, data_atividade, horas, descricao, validado, id_professor_validador) VALUES
(1, 1, '2026-07-07', 2.0, 'Atendimento sobre modelagem ER e normalizacao.',       TRUE,  2),
(2, 1, '2026-07-08', 1.5, 'Preparacao de material de apoio para SQL.',            TRUE,  2),
(3, 2, '2026-07-09', 2.0, 'Atendimento sobre estruturas de arvore.',              TRUE,  2),
(4, 2, '2026-07-10', 1.0, 'Revisao de exercicios de recursao com os alunos.',    FALSE, NULL),
(5, 3, '2026-07-11', 2.5, 'Preparacao de lista de exercicios de algoritmos.',    FALSE, NULL);

SELECT setval('registros_frequencia_id_frequencia_seq', 5);

-- ============================================================
-- AVALIACOES_TUTORIA (5 registros)
-- ============================================================

INSERT INTO avaliacoes_tutoria (id_avaliacao, id_sessao, id_estudante, nota, comentario, data_avaliacao) VALUES
(1, 1, 4, 5, 'Atendimento muito claro e objetivo.',               '2026-07-07'),
(2, 2, 4, 5, 'Excelente explicacao sobre SQL Joins.',             '2026-07-08'),
(3, 3, 7, 4, 'Boa explicacao, mas poderia ter mais exemplos.',    '2026-07-09'),
(4, 4, 8, 3, 'Atendimento razoavel, precisei estudar mais.',      '2026-07-10'),
(5, 1, 7, 4, 'Aproveitei bem a sessao, monitor bem preparado.',   '2026-07-07');

SELECT setval('avaliacoes_tutoria_id_avaliacao_seq', 5);
