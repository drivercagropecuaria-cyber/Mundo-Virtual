TRANSFERENCIA GPT CONSOLIDADA - 7 FEB 2026

OBJETIVO
Documento unico para transferir contexto completo do trabalho para outro agente GPT.

RESUMO EXECUTIVO
- Ajustes em scripts Python para encoding, escrita de relatorios e leitura de contrato com BOM.
- Criacao de bootstrap SQL e blocos de drift-fix para schema PostGIS.
- Ajustes no import de GeoJSON para payload minimo de fix_flags.
- Diversos snippets SQL para normalizacao, hashes, views, flags e consultas de validacao.
- Pipeline e validacao apontaram casos de KML com zero features (pendente).

ESCOPO DO TRABALHO
- Pipeline GIS (import KML/GeoJSON, validacao, export).
- Schema e dados PostGIS (tabelas, views, indices, backfills).
- Regras de normalizacao e deduplicacao por hash.
- Diagnosticos e consultas de qualidade.

ARQUITETURA E AMBIENTE
- OS: Windows.
- Workspace principal: C:\Users\rober\Desktop\Mundo Virtual Villa Canabrava.
- Banco: Postgres com PostGIS, esquema principal: villa_canabrava.
- Tabelas principais: villa_canabrava.geo_features e villa_canabrava.layers.

FUNCIONALIDADES (DETALHADO)
- Ingestao:
	- Import de KML/GeoJSON por pasta.
	- Mapeamento de layer_name e atributos associados.
	- Geometrias convertidas para SRID target via ST_SetSRID.
- Validacao:
	- Manifesto e relatorio com encoding consistente.
	- Conferencia de camadas esperadas vs. importadas.
	- Deteccao de layers sem features (KML vazio).
- Normalizacao:
	- Linha canonica deterministica (canon_line).
	- Tentativa de polygonizacao segura (canon_geom).
	- Normalizacao de colecoes e consistencia de tipo.
- Deteccao de duplicatas:
	- Hash exato (sensivel a direcao).
	- Hash canonico (independente de direcao e ordem de segmentos).
	- Relatorios de duplicatas por hash.
- Metricas:
	- area_ha e perimeter_km via geografia.
	- Views de metricas e flags para outliers.
- Export:
	- FeatureCollection GeoJSON via SQL com jsonb_agg.
	- Saida unica para downstream (GIS/visualizacao/QA).

FERRAMENTAS E TECNOLOGIAS
- Linguagens:
	- Python para pipeline e validacoes.
	- SQL para schema, views, normalizacao e export.
- Banco:
	- Postgres + PostGIS.
	- Extensoes: postgis, pgcrypto, pg_trgm.
- Funcoes GIS:
	- ST_LineMerge, ST_Dump, ST_Normalize, ST_Node, ST_Polygonize.
	- ST_IsEmpty, ST_Boundary, ST_MakeValid, ST_AsEWKB.
	- ST_AsGeoJSON, ST_GeomFromGeoJSON, ST_SetSRID.
- Hashing:
	- digest() + encode() com sha256.
- Infra:
	- Docker (container Postgres).
	- PowerShell para execucao local.

DESIGN (PRINCIPIOS E DECISOES)
- Consistencia de encoding:
	- Leitura de JSON com BOM via utf-8-sig.
	- Escrita de manifest/report com utf-8 e newline "\n".
- Modelo de dados:
	- geo_features como tabela de features com geometria e atributos.
	- layers como catalogo de camadas e metadados.
- Normalizacao geometrica:
	- canon_line garante direcao deterministica.
	- canon_geom promove polygonizacao quando ciclo fechado, senao mantem linha.
	- ST_Normalize aplicado para estabilidade de WKB.
- Deduplicacao:
	- geom_hash_exact garante identidade estrita.
	- geom_hash_canon permite agrupar equivalentes topologicos.
	- Indices parciais para performance em hashes nao nulos.
- Robustez:
	- Triggers para manter hashes atualizados em INSERT/UPDATE.
	- Backfill para populacao retroativa.
	- Views para flags e outliers sem alterar base.
- Export:
	- Export em uma unica query para consistencia de output.
	- Propriedades relevantes dentro de properties.

PLANO DE ACAO DE EXECUCAO (FIM A FIM)
FASE 0 - PREPARO
1) Verificar container Postgres/PostGIS ativo.
2) Confirmar schema villa_canabrava e extensoes instaladas.
3) Validar SRID padrao e amostras de geometrias.

FASE 1 - BOOTSTRAP E MIGRACAO
1) Rodar bootstrap_villa_canabrava.sql se ambiente novo.
2) Aplicar migrations (hashes e canonizacao).
3) Executar drift-fix de colunas se necessario.

FASE 2 - INGESTAO
1) Importar KML/GeoJSON por pasta.
2) Garantir layer_name e attributes populados.
3) Aplicar fix_flags quando necessario.

FASE 3 - NORMALIZACAO E HASHES
1) Executar canon_line/canon_geom.
2) Popular hashes com backfill e manter triggers ativos.
3) Criar indices parciais em hashes.

FASE 4 - QA E VALIDACAO
1) Rodar validacao de manifesto vs. layers.
2) Checar duplicatas por hash exato e canonico.
3) Inspecionar flags e outliers.

FASE 5 - EXPORT E ENTREGA
1) Exportar FeatureCollection para GeoJSON.
2) Validar tamanho, encoding e schema do output.
3) Entregar arquivo final para downstream.

ESTRUTURA DO WORKSPACE (PARCIAL)
- scripts/gis/validate_pipeline.py
- scripts/gis/import_geojson_folder.py
- scripts/db/bootstrap_villa_canabrava.sql
- db/migrations/20260207_01_cercas_hashes.sql
- villa_canabrava_export.geojson (export planejado)
- Documentos .md de governanca e relatorios no root

ARQUIVOS IMPORTANTES E ESTADO
1) scripts/gis/validate_pipeline.py
	 - Ajuste de escrita de relatorio/manifesto: encoding utf-8, newline "\n", try/except, stderr e sys.exit(2).
	 - read_contract: encoding utf-8-sig, retorno dict.
	 - Objetivo: garantir consistencia de leitura/escrita com BOM e falhas tratadas.

2) scripts/db/bootstrap_villa_canabrava.sql
	 - Criado para bootstrap (extensoes postgis/pgcrypto/pg_trgm, schema, tabelas, indices).
	 - Blocos de drift-fix adicionando colunas (category, subcategory, name, attributes, source_kml).
	 - Backfills de subcategory.
	 - Campos area_ha e perimeter_km em geo_features e layers, com backfills.
	 - Observacao: blocos em transacoes separadas para drift-fix.

3) scripts/gis/import_geojson_folder.py
	 - rows.append reduzido para carregar somente fix_flags como "{}" no fim do tuple.
	 - O template SQL ainda faz now() e COALESCE(%s::jsonb,'{}').
	 - Geometry entra via ST_SetSRID(ST_GeomFromGeoJSON(%s), srid).

4) db/migrations/20260207_01_cercas_hashes.sql
	 - Documento de migration criado no workspace (conteudo baseado em canonizacao e hashes).
	 - Ver abaixo "SQL CONSOLIDADO" para o bloco final sugerido.

5) villa_canabrava_export.geojson
	 - Arquivo de export planejado via docker exec + psql, comando foi interrompido com ^C.

DECISOES E AJUSTES REALIZADOS
- Encoding:
	- Leitura de contrato JSON com BOM via utf-8-sig.
	- Escrita de manifest e report com utf-8 e newline consistente.
- Import GeoJSON:
	- fix_flags gravado como JSON vazio, removendo placeholders None.
- PostGIS:
	- Campos de area/perimetro calculados por geografia.
	- Views para metricas e flags.

QUERIES E VIEWS MAIS USADAS (LISTA RAPIDA)
- Views:
	- cercas_poly (line merge + polygonizacao segura)
	- cercas_metrics (length/perimeter/area)
	- cercas_flags (flags de outliers)
- Duplicatas:
	- geom_hash_exact (hash sensivel a direcao)
	- geom_hash_canon (hash canonico)
- Checagens:
	- cardinality(flags) > 0
	- GeometryType(canon_geom(geom_norm))

SQL CONSOLIDADO (CANONIZACAO + HASHES + BACKFILL + INDICES)
Obs: bloco abaixo eh o consolidado mais recente para cercas_norm. Ajuste nomes conforme seu schema.

BEGIN;

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 1) canon_line: deterministico e sem forcar MULTI sempre
CREATE OR REPLACE FUNCTION canon_line(g geometry)
RETURNS geometry
LANGUAGE sql
IMMUTABLE
STRICT
PARALLEL SAFE
AS $$
WITH dumped AS (
	SELECT (ST_Dump(ST_LineMerge(g))).geom AS ln
),
fixed AS (
	SELECT
		CASE
			WHEN GeometryType(ln) = 'LINESTRING' THEN
				CASE
					WHEN (ST_X(ST_StartPoint(ln)) > ST_X(ST_EndPoint(ln)))
						OR (ST_X(ST_StartPoint(ln)) = ST_X(ST_EndPoint(ln))
								AND ST_Y(ST_StartPoint(ln)) > ST_Y(ST_EndPoint(ln)))
					THEN ST_Reverse(ln)
					ELSE ln
				END
			ELSE ln
		END AS ln2
	FROM dumped
),
col AS (
	SELECT ST_Normalize(ST_Collect(ln2)) AS gcol
	FROM fixed
)
SELECT ST_CollectionExtract(gcol, 2)
FROM col;
$$;

-- 2) canon_geom: tenta POLYGON quando "grafo" estiver fechado
CREATE OR REPLACE FUNCTION canon_geom(g geometry)
RETURNS geometry
LANGUAGE plpgsql
IMMUTABLE
STRICT
PARALLEL SAFE
AS $$
DECLARE
	ln   geometry;
	poly geometry;
BEGIN
	IF g IS NULL OR ST_IsEmpty(g) THEN
		RETURN NULL;
	END IF;

	ln := canon_line(g);

	IF ln IS NOT NULL
		 AND NOT ST_IsEmpty(ln)
		 AND ST_IsEmpty(ST_Boundary(ln)) THEN
		poly := ST_CollectionExtract(
							ST_MakeValid(ST_Polygonize(ST_Node(ln))),
							3
						);
	ELSE
		poly := NULL;
	END IF;

	IF poly IS NOT NULL AND NOT ST_IsEmpty(poly) THEN
		RETURN ST_Normalize(poly);
	END IF;

	RETURN ST_Normalize(ln);
END;
$$;

-- 3) Colunas hash
ALTER TABLE cercas_norm
	ADD COLUMN IF NOT EXISTS geom_hash_exact text,
	ADD COLUMN IF NOT EXISTS geom_hash_canon text;

-- 4) Trigger hashes
CREATE OR REPLACE FUNCTION cercas_norm_hash_trg()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
	gcanon geometry;
BEGIN
	IF NEW.geom_norm IS NULL OR ST_IsEmpty(NEW.geom_norm) THEN
		NEW.geom_hash_exact := NULL;
		NEW.geom_hash_canon := NULL;
		RETURN NEW;
	END IF;

	NEW.geom_hash_exact := encode(digest(ST_AsEWKB(NEW.geom_norm), 'sha256'), 'hex');

	gcanon := canon_geom(NEW.geom_norm);
	NEW.geom_hash_canon := encode(digest(ST_AsEWKB(gcanon), 'sha256'), 'hex');

	RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_cercas_norm_hash ON cercas_norm;

CREATE TRIGGER trg_cercas_norm_hash
BEFORE INSERT OR UPDATE OF geom_norm
ON cercas_norm
FOR EACH ROW
EXECUTE FUNCTION cercas_norm_hash_trg();

-- 5) Backfill
WITH x AS (
	SELECT
		id,
		encode(digest(ST_AsEWKB(geom_norm), 'sha256'), 'hex') AS h_exact,
		encode(digest(ST_AsEWKB(canon_geom(geom_norm)), 'sha256'), 'hex') AS h_canon
	FROM cercas_norm
	WHERE geom_norm IS NOT NULL AND NOT ST_IsEmpty(geom_norm)
)
UPDATE cercas_norm n
SET geom_hash_exact = x.h_exact,
		geom_hash_canon = x.h_canon
FROM x
WHERE n.id = x.id
	AND (n.geom_hash_exact IS DISTINCT FROM x.h_exact
			 OR n.geom_hash_canon IS DISTINCT FROM x.h_canon);

-- 6) Indices parciais
CREATE INDEX IF NOT EXISTS cercas_norm_hash_canon_notnull_idx
ON cercas_norm (geom_hash_canon)
WHERE geom_hash_canon IS NOT NULL;

CREATE INDEX IF NOT EXISTS cercas_norm_hash_exact_notnull_idx
ON cercas_norm (geom_hash_exact)
WHERE geom_hash_exact IS NOT NULL;

COMMIT;

CONSULTAS DE VALIDACAO (SNIPPETS)
- Duplicatas canonicas:
	SELECT geom_hash_canon, count(*) AS qtd, array_agg(id ORDER BY id) AS ids
	FROM cercas_norm
	WHERE geom_hash_canon IS NOT NULL
	GROUP BY geom_hash_canon
	HAVING count(*) > 1
	ORDER BY qtd DESC;

- Duplicatas exatas:
	SELECT geom_hash_exact, count(*) AS qtd, array_agg(id ORDER BY id) AS ids
	FROM cercas_norm
	WHERE geom_hash_exact IS NOT NULL
	GROUP BY geom_hash_exact
	HAVING count(*) > 1
	ORDER BY qtd DESC;

- Flags:
	SELECT *
	FROM cercas_flags
	WHERE cardinality(flags) > 0;

- Tipos resultantes de canon_geom:
	WITH t AS (
		SELECT id, canon_geom(geom_norm) AS g
		FROM cercas_norm
		WHERE geom_norm IS NOT NULL AND NOT ST_IsEmpty(geom_norm)
	)
	SELECT GeometryType(g) AS tipo, count(*) AS qtd
	FROM t
	GROUP BY 1
	ORDER BY qtd DESC;

PENDENCIAS E RISCOS
- Export geojson interrompido (comando docker exec + psql foi abortado com ^C).
- Pipeline de validacao indicou camadas faltando por KMLs com zero features.

COMANDOS IMPORTANTES
- Export geo_features para GeoJSON (quando container estiver ok):
	docker exec -i villa_canabrava_postgis psql -U postgres -d postgres -At -c "
	SELECT jsonb_build_object(
			'type','FeatureCollection',
			'features', jsonb_agg(
					jsonb_build_object(
							'type','Feature',
							'geometry', ST_AsGeoJSON(geometry)::jsonb,
							'properties', jsonb_build_object(
									'name', name,
									'layer_name', layer_name,
									'category', category,
									'subcategory', subcategory,
									'area_ha', area_ha,
									'perimeter_km', perimeter_km,
									'attributes', attributes
							)
					)
			)
	) FROM villa_canabrava.geo_features;
	" > villa_canabrava_export.geojson

NOTAS OPERACIONAIS
- KMLs vazios podem gerar mismatch no manifesto e devem ser tratados como excecao.
- Em caso de BOM, usar utf-8-sig para evitar caracteres espurios.
- Para polygonizar linhas, usar ST_Node antes de ST_Polygonize quando houver gaps.
- Confirmar SRID antes de calculos de area/perimetro.

PROXIMOS PASSOS SUGERIDOS
1) Reexecutar export GeoJSON com o container correto e salvar o arquivo.
2) Rodar validacoes de duplicata (hash exact/canon) e revisar flags.
3) Verificar layers com zero features e decidir se entram no manifesto.

HISTORICO DE AJUSTES RELEVANTES
- validate_pipeline.py: imports, read_contract utf-8-sig, report/manifest com newline padrao e try/except.
- bootstrap_villa_canabrava.sql: drift-fix de schema e campos metricos.
- import_geojson_folder.py: rows payload reduzido, fix_flags JSON.

NOTAS PARA O PROXIMO AGENTE
- Prioridade: validar camadas faltantes (KML sem features) e decidir se remover do contrato ou corrigir origem.
- Reexecutar export geojson se necessario.
- Se necessario, revalidar hashes canonicos com queries de comparacao ST_Equals.
