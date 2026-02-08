# STAGE 4 LOCAL PERFORMANCE REPORT - 6 FEB 2026

## Context
- Ambiente: local (postgres_test)
- Banco: biblioteca
- Postgres/PostGIS: 15 / 3.3.4
- Dataset: public.geometrias (10 registros)
- Objetivo: validação rapida de consultas espaciais e temporais com EXPLAIN ANALYZE

## Indexes verificados
- geometrias_pkey (btree em id)
- idx_geometrias_geometry (gist em geometry)
- idx_geometrias_temporal (btree em data_inicio, data_fim)

## Resultados (EXPLAIN ANALYZE)
- Q1 BBOX (geometry && ST_MakeEnvelope)
  - Plano: Seq Scan (tabela pequena)
  - Execucao: 1.474 ms
- Q2 Proximidade (ST_DWithin)
  - Plano: Index Scan (idx_geometrias_geometry)
  - Execucao: 0.830 ms
- Q3 Contencao (ST_Contains)
  - Plano: Index Scan (idx_geometrias_geometry)
  - Execucao: 0.438 ms
- Q4 Temporal (data_inicio/data_fim)
  - Plano: Seq Scan (tabela pequena)
  - Execucao: 0.113 ms
- Q5 KNN (ORDER BY geometry <-> POINT)
  - Plano: Seq Scan + Sort (tabela pequena)
  - Execucao: 0.177 ms
- Q5 KNN (com enable_seqscan=off)
  - Plano: Index Scan (idx_geometrias_geometry)
  - Execucao: 0.352 ms

## Resultados (KML seed em gis_data.features)
- Dataset: gis_data.features (456 registros)
- Q1 BBOX (geometry && ST_MakeEnvelope)
  - Plano: Index Scan (idx_features_geometry)
  - Execucao: 0.321 ms
- Q2 Proximidade (ST_DWithin geography, 20km)
  - Plano: Seq Scan (tabela pequena)
  - Execucao: 38.005 ms
- Q3 Interseccao (ST_Intersects + envelope)
  - Plano: Index Scan (idx_features_geometry)
  - Execucao: 0.408 ms
- Q4 KNN (ORDER BY geometry <-> POINT)
  - Plano: Index Scan (idx_features_geometry)
  - Execucao: 1.967 ms
- Q5 Proximidade (ST_DWithin geometry + bbox)
  - Plano: Index Scan (idx_features_geometry)
  - Execucao: 0.408 ms

## Observacoes
- Com apenas 10 registros, o planner favorece Seq Scan em algumas consultas.
- O indice GiST foi usado corretamente para consultas espaciais (ST_DWithin e ST_Contains).
- No KNN, o uso do GiST aparece apenas quando Seq Scan e desabilitado.
- No seed KML (253 registros), o GiST foi usado em BBOX/Intersects/KNN; ST_DWithin com geography manteve Seq Scan.
- Resultados servem como smoke test; nao representam carga real.

## Proximos passos
- Carregar seed completo para medir latencias realistas.
- Repetir Q1-Q4 e adicionar Q5-Q10 conforme o pacote de validacao final.
