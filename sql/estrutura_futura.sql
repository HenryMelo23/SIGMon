-- Estrutura futura para PostgreSQL.
-- Este arquivo é documental: não é executado pela aplicação atual.

CREATE TABLE departamentos (
  id_departamento SERIAL PRIMARY KEY,
  nome TEXT NOT NULL,
  sigla VARCHAR(20) NOT NULL UNIQUE,
  email TEXT NOT NULL
);

CREATE TABLE usuarios (
  id_usuario SERIAL PRIMARY KEY,
  id_departamento INTEGER NOT NULL REFERENCES departamentos(id_departamento),
  nome TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  matricula VARCHAR(30) NOT NULL,
  papel VARCHAR(20) NOT NULL CHECK (papel IN ('ESTUDANTE','MONITOR','PROFESSOR','ADMINISTRADOR','FINANCEIRO')),
  senha_hash TEXT NOT NULL,
  ativo BOOLEAN NOT NULL DEFAULT TRUE,
  data_cadastro DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE editais (
  id_edital SERIAL PRIMARY KEY,
  id_departamento INTEGER NOT NULL REFERENCES departamentos(id_departamento),
  titulo TEXT NOT NULL,
  descricao TEXT NOT NULL,
  data_inicio DATE NOT NULL,
  data_fim DATE NOT NULL,
  quantidade_vagas INTEGER NOT NULL CHECK (quantidade_vagas > 0),
  nota_minima NUMERIC(4,2) NOT NULL CHECK (nota_minima BETWEEN 0 AND 10)
);

CREATE TABLE candidaturas (
  id_candidatura SERIAL PRIMARY KEY,
  id_edital INTEGER NOT NULL REFERENCES editais(id_edital),
  id_estudante INTEGER NOT NULL REFERENCES usuarios(id_usuario),
  data_inscricao DATE NOT NULL DEFAULT CURRENT_DATE,
  ira NUMERIC(4,2) NOT NULL,
  nota_disciplina NUMERIC(4,2) NOT NULL,
  status VARCHAR(20) NOT NULL,
  UNIQUE (id_edital, id_estudante)
);

-- Demais tabelas seguirão o mesmo padrão:
-- disciplinas, turmas, alocacoes_monitores, dados_bancarios,
-- documentos_anexos, agenda_slots, sessoes_tutoria,
-- registros_frequencia, avaliacoes_tutoria e auditoria.

CREATE INDEX idx_candidaturas_status ON candidaturas(status);
CREATE INDEX idx_usuarios_papel ON usuarios(papel);
