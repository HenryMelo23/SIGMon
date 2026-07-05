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

#### Linux/Mac

Crie o banco e o usuário:

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

Execute os scripts SQL na ordem abaixo (os GRANTs ao `sigmon_user` já estão incluídos no `sigmon_create.sql`):

```bash
sudo -u postgres psql -d sigmon -f sql/sigmon_create.sql
sudo -u postgres psql -d sigmon -f sql/sigmon_procedures.sql
sudo -u postgres psql -d sigmon -f sql/sigmon_views.sql
sudo -u postgres psql -d sigmon -f sql/sigmon_triggers.sql
sudo -u postgres psql -d sigmon -f sql/sigmon_seeds.sql
```

#### Windows

Abra o **psql** (instalado junto com o PostgreSQL) e crie o banco e o usuário:

```sql
CREATE DATABASE sigmon;
CREATE USER sigmon_user WITH PASSWORD 'senha';
GRANT ALL PRIVILEGES ON DATABASE sigmon TO sigmon_user;
\c sigmon
GRANT ALL ON SCHEMA public TO sigmon_user;
\q
```

Execute os scripts SQL pelo **cmd** ou **PowerShell** a partir da raiz do projeto (ajuste o caminho do `psql` se necessário):

```powershell
psql -U postgres -d sigmon -f sql/sigmon_create.sql
psql -U postgres -d sigmon -f sql/sigmon_procedures.sql
psql -U postgres -d sigmon -f sql/sigmon_views.sql
psql -U postgres -d sigmon -f sql/sigmon_triggers.sql
psql -U postgres -d sigmon -f sql/sigmon_seeds.sql
```

> No Windows o `psql` normalmente fica em `C:\Program Files\PostgreSQL\<versao>\bin\psql.exe`. Adicione essa pasta ao PATH ou execute os comandos de dentro dela.

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

| Perfil | Nome | E-mail |
|---|---|---|
| Administrador | Ana Beatriz | admin@unb.br |
| Professor | Prof. Maristela | maristela@unb.br |
| Professor | Prof. Caetano | caetano@unb.br |
| Monitor | Rafael Mendes | monitor@unb.br |
| Estudante | Pedro Alves | estudante@unb.br |
| Estudante | Amanda Silva | amanda@unb.br |

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
| Estudante | Editais abertos, histórico escolar, candidaturas, agenda, sessões e avaliações |
| Monitor | Alocação própria, agenda, sessões e avaliações recebidas |
| Professor | Turmas, candidaturas e alocações |
| Administrador | Cadastros completos (usuários, disciplinas, horários, departamentos), editais, histórico e inscrições |
