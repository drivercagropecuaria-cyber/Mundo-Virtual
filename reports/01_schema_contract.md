# Contrato do schema villa_canabrava

Data: 2026-02-07

## Tabelas

```text
table_name
--------------
geo_features
layers
museum_items
(3 rows)
```

## Colunas: geo_features

```text
column_name  | data_type          | is_nullable
--------------+---------------------+------------
id           | uuid                | NO
name         | character varying   | NO
category     | character varying   | NO
subcategory  | character varying   | YES
layer_name   | character varying   | NO
geometry     | USER-DEFINED        | YES
area_ha      | numeric             | YES
perimeter_km | numeric             | YES
attributes   | jsonb               | YES
source_kml   | character varying   | YES
created_at   | timestamp           | YES
updated_at   | timestamp           | YES
```

## Colunas: layers

```text
column_name  | data_type          | is_nullable
--------------+---------------------+------------
id           | uuid                | NO
name         | character varying   | NO
display_name | character varying   | YES
description  | text                | YES
category     | character varying   | YES
style_config | jsonb               | YES
is_visible   | boolean             | YES
z_index      | integer             | YES
created_at   | timestamp           | YES
updated_at   | timestamp           | YES
```

## Indices

```text
geo_features_pkey
idx_geo_features_attributes_gin
idx_geo_features_category
idx_geo_features_geometry
idx_geo_features_layer
idx_geo_features_name_gin
idx_layers_category
layers_name_key
layers_pkey
idx_museum_items_location
idx_museum_items_tags
museum_items_pkey
```

## Constraints

```text
fk_layers (FOREIGN KEY layer_name -> layers.name)
geo_features_pkey (PRIMARY KEY id)
layers_name_key (UNIQUE name)
layers_pkey (PRIMARY KEY id)
museum_items_pkey (PRIMARY KEY id)
```

## Contagens por tabela

```text
geo_features: 665
layers: 250
museum_items: 0
```

## Observacoes

- Para idempotencia, foi criado o arquivo `db/migrations/0002_idempotency.sql` que adiciona `feature_hash` e um indice unico por arquivo.
