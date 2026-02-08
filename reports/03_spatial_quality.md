# Relatorio de qualidade espacial

Generated: 2026-02-07T15:38:40.395989Z
Schema: villa_canabrava

## Saude geral

- PostGIS enabled: YES
- Total features: 665
- Null geometry: 0
- Invalid geometry: 0
- SRID mismatch: 0
- Extent: BOX(-44.00506939952185 -17.44128662887662,-43.8847160344 -17.3128380449)

## Contagem por tipo de geometria

| geom_type | count |
| --- | --- |
| POLYGON | 661 |
| LINESTRING | 4 |

## EXPLAIN - Filtro por bbox

```text
Limit  (cost=0.00..0.91 rows=5 width=16)
  ->  Seq Scan on geo_features  (cost=0.00..120.31 rows=663 width=16)
        Filter: (geometry && '0103000020E610000001000000050000000F94341DA60046C0EB2F1729F87031C00F94341DA60046C043CA7327165031C056FF00603EF145C043CA7327165031C056FF00603EF145C0EB2F1729F87031C00F94341DA60046C0EB2F1729F87031C0'::geometry)
```

## EXPLAIN - ST_Intersects

```text
Limit  (cost=0.00..126.27 rows=5 width=16)
  ->  Seq Scan on geo_features  (cost=0.00..16743.65 rows=663 width=16)
        Filter: st_intersects(geometry, '0103000020E610000001000000050000000F94341DA60046C0EB2F1729F87031C00F94341DA60046C043CA7327165031C056FF00603EF145C043CA7327165031C056FF00603EF145C0EB2F1729F87031C00F94341DA60046C0EB2F1729F87031C0'::geometry)
```