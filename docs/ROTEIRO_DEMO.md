# Roteiro de demonstracao SIGMon

Todos os usuarios usam senha `123456`.

## Preparar banco

```powershell
psql -d sigmon -f sql/sigmon_create.sql
psql -d sigmon -f sql/sigmon_seeds.sql
psql -d sigmon -f sql/sigmon_views.sql
psql -d sigmon -f sql/sigmon_triggers.sql
psql -d sigmon -f sql/sigmon_procedures.sql
```

## Logins

- Admin: `admin@unb.br`
- Pedro: `pedro@unb.br`
- Caetano: `professor@unb.br`
- Rafael: `rafael@unb.br`

## Sequencia no front

1. Admin entra em Disciplinas, Horarios e Turmas; tentar remover uma disciplina/horario/turma vinculada para mostrar erro de FK/regra de negocio.
2. Pedro entra em Historico e cadastra Estruturas de Dados com mencao `SS` e PDF.
3. Admin entra em Historico e aprova o historico do Pedro.
4. Pedro entra em Editais, abre `Edital de Monitoria CIC 2026.1`, escolhe `Estruturas de Dados T01 - Prof. Caetano Silva`, IRA e mencao `SS`.
5. Abrir `psql` antes da aprovacao do Caetano e rodar os SELECTs abaixo.
6. Pedro entra em Inscricoes em turmas e solicita inscricao em `Banco de Dados T01`.
7. Admin entra em Inscricoes em turmas e aprova a inscricao do Pedro.
8. Rafael confere/cria slots em Agenda.
9. Pedro reserva o slot disponivel de Banco de Dados T01 na Agenda.
10. Rafael entra em Sessoes, marca a sessao do Pedro como realizada.
11. Pedro entra em Sessoes e avalia.
12. Rafael entra em Avaliacoes e confere `Desempenho por disciplina`: Banco de Dados deve somar as 2 sessoes pre-seedadas da Amanda mais a sessao ao vivo do Pedro.

## Procedure + trigger

Antes:

```sql
SELECT u.id_usuario, u.nome, u.papel, c.id_candidatura, c.status
FROM usuarios u
JOIN candidaturas c ON c.id_estudante = u.id_usuario
WHERE c.id_candidatura = 2;
```

Executar:

```sql
CALL aprovar_candidatura_e_alocar(2, 3);
```

Depois:

```sql
SELECT u.id_usuario, u.nome, u.papel, c.id_candidatura, c.status,
       a.id_alocacao, a.status AS status_alocacao
FROM usuarios u
JOIN candidaturas c ON c.id_estudante = u.id_usuario
LEFT JOIN alocacoes_monitores a ON a.id_candidatura = c.id_candidatura
WHERE c.id_candidatura = 2;

SELECT id_auditoria, id_usuario, acao, entidade, detalhes, criado_em
FROM auditoria
WHERE acao IN ('MUDANCA_PAPEL', 'APROVAR_CANDIDATURA')
ORDER BY id_auditoria DESC;
```

## View

```sql
SELECT *
FROM vw_avaliacoes_monitoria
WHERE monitor = 'Rafael Nogueira'
ORDER BY disciplina;
```
