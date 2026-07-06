# SIGMon - Sistema Integrado de Gestão de Monitoria

Aplicação web para gestão de monitoria acadêmica desenvolvida para o Departamento de Ciência da Computação da Universidade de Brasília.

**Integrantes:** Luis Henrique Bessa de Melo e Carlos Victor Albuquerque Oliveira

## Stack

- Python + Flask
- Jinja2 Templates
- PostgreSQL + psycopg2 (sem ORM)
- HTML, CSS e JavaScript simples

## Pré-requisitos

- Python 3.10+
- PostgreSQL 14+

## Como rodar

### 1. Clone o repositório e crie o ambiente virtual

```bash
git clone <url-do-repositorio>
cd SIGMon
python -m venv venv
```

Ative o ambiente virtual:

```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

Edite o `.env`:

```env
SECRET_KEY=qualquer-string-aqui-serve-para-desenvolvimento
DATABASE_URL=postgresql://sigmon_user:senha@localhost:5432/sigmon
```

> O `SECRET_KEY` é usado pelo Flask para assinar os cookies de sessão. Em desenvolvimento qualquer valor funciona. Em produção use uma string longa e aleatória.

### 4. Configure o banco de dados

Crie o banco e o usuário no PostgreSQL:

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE sigmon;
CREATE USER sigmon_user WITH PASSWORD 'senha';
GRANT ALL PRIVILEGES ON DATABASE sigmon TO sigmon_user;
\c sigmon
GRANT ALL ON SCHEMA public TO sigmon_user;
\q
```

Execute os scripts SQL:

```bash
sudo cp sql/sigmon_create.sql /tmp/
sudo cp sql/sigmon_seeds.sql /tmp/
sudo cp sql/sigmon_views.sql /tmp/
sudo cp sql/sigmon_triggers.sql /tmp/
sudo cp sql/sigmon_procedures.sql /tmp/
sudo -u postgres psql -d sigmon -f /tmp/sigmon_create.sql
sudo -u postgres psql -d sigmon -f /tmp/sigmon_seeds.sql
sudo -u postgres psql -d sigmon -f /tmp/sigmon_views.sql
sudo -u postgres psql -d sigmon -f /tmp/sigmon_triggers.sql
sudo -u postgres psql -d sigmon -f /tmp/sigmon_procedures.sql
sudo -u postgres psql -d sigmon -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO sigmon_user; GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO sigmon_user;"
```

### 5. Rode a aplicação

```bash
python run.py
```

Acesse em: `http://localhost:5000`

Se a porta estiver ocupada:

```bash
# Linux/Mac
PORT=5001 python run.py

# Windows PowerShell
$env:PORT=5001; python run.py
```

## Usuários de teste

Todos usam a senha `123456`.

| Perfil | E-mail |
|---|---|
| Administrador | admin@unb.br |
| Professor Caetano | professor@unb.br |
| Estudante Pedro | pedro@unb.br |
| Estudante Amanda | amanda@unb.br |
| Monitor Rafael | rafael@unb.br |
| Financeiro | financeiro@unb.br |

## Estrutura do projeto

```
app/
  models/          Entidades do domínio (dataclasses)
  repositories/    Acesso ao banco de dados (SQL puro)
  services/        Regras de negócio
  routes/          Blueprints Flask
  templates/       Telas Jinja2
  static/          CSS e JS
  database/        Conexão e pool PostgreSQL
  utils/           Permissões, decorators e validações
sql/
  sigmon_create.sql     Criação das tabelas
  sigmon_seeds.sql      Dados iniciais
  sigmon_views.sql      Views
  sigmon_triggers.sql   Triggers
  sigmon_procedures.sql Procedures
run.py             Entrada da aplicação
```

## Perfis e permissões

| Perfil | Acesso |
|---|---|
| Estudante | Editais abertos, candidaturas, agenda, sessões e avaliações |
| Monitor | Alocação própria, agenda, sessões, frequência e avaliações |
| Professor | Turmas, candidaturas, alocações e validação de frequência |
| Administrador | Cadastros completos, editais, candidaturas e alocações |
| Financeiro | Monitores ativos, dados bancários e frequências validadas |
