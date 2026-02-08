# RELATORIO ULTIMOS 25 COMANDOS (PSReadLine)

Fonte: historico persistido do PSReadLine (ultimas 500 linhas filtradas).
Observacao: valores de variaveis como $scan, $name, $vol e $sql nao aparecem no historico.

## Comandos (1..25)

1) Comando:
```text
docker run --rm -v 6ed974cb09dc1aefb040770dc2275ab7549d19f14b7b5bb35e4a9d6db0de3802:/data alpine sh -lc "cat /data/PG_VERSION || true"`
```
Significado: sobe um container temporario e tenta ler o arquivo PG_VERSION dentro do volume.
Esperado: retornar a versao do cluster PostgreSQL ou vazio.
Verificar: saida do comando com a versao ou nada.

2) Comando:
```text
docker rm -f $scan 2>$null`
```
Significado: remove o container cujo nome esta em $scan, ignorando erros.
Esperado: container removido (ou nenhum erro).
Verificar: ausencia do container em docker ps.

3) Comando:
```text
docker run -d --name $scan -v ${vol}:/var/lib/postgresql/data postgis/postgis:15-3.3-alpine | Out-Null`
```
Significado: inicia um container PostGIS usando o volume em $vol.
Esperado: container iniciado em background.
Verificar: docker ps mostra $scan rodando.

4) Comando:
```text
docker exec -i $scan psql -U postgres -P pager=off -c "\l"`
```
Significado: lista bancos no Postgres do container $scan.
Esperado: lista de bancos (postgres, template0, template1, etc.).
Verificar: saida com lista de bancos.

5) Comando:
```text
docker exec -i $scan psql -U postgres -d biblioteca -P pager=off -c "SELECT to_regclass('public.geometrias') AS geometrias;"`
```
Significado: verifica se a tabela public.geometrias existe.
Esperado: coluna geometrias com nome da tabela ou NULL.
Verificar: saida com public.geometrias ou vazio.

6) Comando:
```text
docker exec -i $scan psql -U postgres -d biblioteca -P pager=off -c "\dt public.*"`
```
Significado: lista tabelas no schema public.
Esperado: lista de tabelas, incluindo geometrias se existir.
Verificar: saida com tabelas.

7) Comando:
```text
docker rm -f $scan`
```
Significado: remove o container $scan.
Esperado: container removido.
Verificar: docker ps nao mostra $scan.

8) Comando:
```text
docker rm -f pgold 2>$null`
```
Significado: remove container pgold, ignorando erros.
Esperado: container removido ou inexistente.
Verificar: docker ps nao mostra pgold.

9) Comando:
```text
docker run -d --name pgold -v 6ed974cb09dc1aefb040770dc2275ab7549d19f14b7b5bb35e4a9d6db0de3802:/var/lib/postgresql/data postgis/postgis:15-3.3-alpine | Out-Null`
```
Significado: inicia container pgold com o volume indicado.
Esperado: container iniciado.
Verificar: docker ps mostra pgold.

10) Comando:
```text
docker exec -i pgold sh -lc "pg_dump -U postgres -d biblioteca -t public.geometrias -Fc -f /tmp/geometrias.dump"`
```
Significado: gera backup da tabela public.geometrias em formato custom.
Esperado: arquivo /tmp/geometrias.dump criado no container.
Verificar: ausencia de erro e existencia do arquivo no container.

11) Comando:
```text
docker cp pgold:/tmp/geometrias.dump .\backup\geometrias.dump`
```
Significado: copia o backup do container para o host.
Esperado: arquivo .\backup\geometrias.dump criado.
Verificar: arquivo presente no host.

12) Comando:
```text
docker rm -f pgold`
```
Significado: remove o container pgold.
Esperado: container removido.
Verificar: docker ps nao mostra pgold.

13) Comando:
```text
docker cp .\backup\geometrias.dump postgres_test:/tmp/geometrias.dump`
```
Significado: copia o backup para o container postgres_test.
Esperado: arquivo /tmp/geometrias.dump criado no container.
Verificar: existencia do arquivo no container.

14) Comando:
```text
docker exec -it postgres_test sh -lc "pg_restore -U postgres -d biblioteca -c -t public.geometrias /tmp/geometrias.dump"`
```
Significado: restaura a tabela public.geometrias no banco biblioteca.
Esperado: tabela recriada e dados restaurados.
Verificar: ausencia de erros e contagem de linhas.

15) Comando:
```text
docker exec -i postgres_test psql -U postgres -d biblioteca -P pager=off -c "\dt public.*"`
```
Significado: lista tabelas apos o restore.
Esperado: public.geometrias presente.
Verificar: tabela listada.

16) Comando:
```text
docker exec -i postgres_test psql -U postgres -d biblioteca -P pager=off -c "SELECT COUNT(*) FROM public.geometrias;"`
```
Significado: conta registros da tabela.
Esperado: numero maior que zero.
Verificar: valor retornado.

17) Comando:
```text
docker exec -i postgres_test psql -U postgres -d biblioteca -P pager=off -c "\d+ public.geometrias"`
```
Significado: mostra estrutura detalhada da tabela.
Esperado: colunas e tipos exibidos.
Verificar: colunas, tipos e indexes.

18) Comando:
```text
docker rm -f $name 2>$null`
```
Significado: remove o container cujo nome esta em $name.
Esperado: container removido ou inexistente.
Verificar: docker ps nao mostra $name.

19) Comando:
```text
docker run -d --name $name -v ${vol}:/var/lib/postgresql/data postgis/postgis:15-3.3-alpine | Out-Null`
```
Significado: inicia um container PostGIS com o volume em $vol.
Esperado: container iniciado.
Verificar: docker ps mostra $name.

20) Comando:
```text
docker exec -i $name psql -U postgres -d biblioteca -P pager=off -c "SELECT COUNT(*) AS total FROM public.geometrias;"`
```
Significado: conta registros da tabela no container $name.
Esperado: total retornado.
Verificar: valor da contagem.

21) Comando:
```text
docker exec -i $name psql -U postgres -d biblioteca -P pager=off -c "SELECT MIN(id), MAX(id) FROM public.geometrias;"`
```
Significado: pega os limites de ID da tabela.
Esperado: dois valores numericos.
Verificar: MIN e MAX retornados.

22) Comando:
```text
docker exec -i $name psql -U postgres -d biblioteca -P pager=off -c "SELECT ST_X(geometry), ST_Y(geometry) FROM public.geometrias ORDER BY id LIMIT 5;"`
```
Significado: amostra coordenadas de geometrias.
Esperado: 5 linhas com coordenadas.
Verificar: valores numericos validos.

23) Comando:
```text
docker rm -f $name`
```
Significado: remove o container $name.
Esperado: container removido.
Verificar: docker ps nao mostra $name.

24) Comando:
```text
docker exec -i postgres_test psql -U postgres -d biblioteca -P pager=off -c "$sql"`
```
Significado: executa o SQL armazenado na variavel $sql.
Esperado: depende do conteudo de $sql.
Verificar: saida do psql conforme o SQL.

25) Comando:
```text
docker exec -i postgres_test psql -U postgres -d biblioteca -P pager=off -c "VACUUM (ANALYZE) public.geometrias;"`
```
Significado: otimiza e atualiza estatisticas da tabela.
Esperado: comando executado sem erro.
Verificar: mensagem de VACUUM concluido.

## Resumo executivo

Estado atual do sistema:
- Porta ativa do banco canonico: 15433
- Schema principal: villa_canabrava
- Total de feicoes (validacao mais recente): 665

Divergencias e hipoteses:
- Features=413 (importacao completa) vs Total=665 (validacao). Hipotese: houve importacao anterior com 252 feicoes, e a nova importacao somou 413, resultando em 665.
- Skipped=44 indica feicoes vazias ou geometrias invalidas durante a importacao.

Proximos 5 passos objetivos:
1) Confirmar se a duplicacao (252 + 413) e esperada ou se deve haver limpeza da tabela antes do import.
2) Se nao for esperada, limpar a tabela villa_canabrava.geo_features e reimportar.
3) Investigar por que alguns arquivos seguem com 0 feicoes (ex.: Curral - Confinamento para Sequestro de Bezerros, Estrada).
4) Revalidar e atualizar [validation_report.md](validation_report.md) apos qualquer ajuste.
5) Gerar backup do schema final e registrar o estado em um relatorio executivo.
