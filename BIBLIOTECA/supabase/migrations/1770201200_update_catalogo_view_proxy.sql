-- Atualizar view para expor URLs originais e proxy separadas

DROP VIEW IF EXISTS v_catalogo_audit_recente CASCADE;
DROP VIEW IF EXISTS v_catalogo_stats CASCADE;
DROP VIEW IF EXISTS v_catalogo_completo CASCADE;
DROP VIEW IF EXISTS v_catalogo_ativo CASCADE;

CREATE OR REPLACE VIEW v_catalogo_ativo AS
SELECT * FROM catalogo
WHERE deleted_at IS NULL;

CREATE OR REPLACE VIEW v_catalogo_completo AS
SELECT
  c.id,
  c.identificador,
  c.titulo,
  c.descricao,
  c.data_captacao,
  c.frase_memoria,
  c.observacoes,
  c.responsavel,
  c.media_id,

  c.area_fazenda_id,
  c.ponto_id,
  c.tipo_projeto_id,
  c.nucleo_pecuaria_id,
  c.nucleo_agro_id,
  c.operacao_id,
  c.marca_id,
  c.evento_id,
  c.funcao_historica_id,
  c.tema_principal_id,
  c.status_id,
  c.capitulo_id,

  af.name as area_fazenda_nome,
  p.name as ponto_nome,
  tp.name as tipo_projeto_nome,
  np.name as nucleo_pecuaria_nome,
  na.name as nucleo_agro_nome,
  op.name as operacao_nome,
  mv.name as marca_nome,
  ep.name as evento_nome,
  fh.name as funcao_historica_nome,
  tprinc.name as tema_principal_nome,
  sm.name as status_nome,
  cf.name as capitulo_nome,

  -- Dados originais
  ma.filename as arquivo_nome,
  ma.mime_type as arquivo_tipo,
  ma.size_bytes as arquivo_tamanho,
  ma.public_url as arquivo_url,

  -- Dados proxy (MP4)
  ma.proxy_filename,
  ma.proxy_mime_type,
  ma.proxy_size_bytes,
  ma.proxy_url,

  ma.thumbnail_url,
  ma.width,
  ma.height,
  ma.duration_seconds,

  c.created_at,
  c.updated_at,
  c.deleted_at

FROM catalogo c
LEFT JOIN taxonomy_categories af ON c.area_fazenda_id = af.id
LEFT JOIN taxonomy_categories p ON c.ponto_id = p.id
LEFT JOIN taxonomy_categories tp ON c.tipo_projeto_id = tp.id
LEFT JOIN taxonomy_categories np ON c.nucleo_pecuaria_id = np.id
LEFT JOIN taxonomy_categories na ON c.nucleo_agro_id = na.id
LEFT JOIN taxonomy_categories op ON c.operacao_id = op.id
LEFT JOIN taxonomy_categories mv ON c.marca_id = mv.id
LEFT JOIN taxonomy_categories ep ON c.evento_id = ep.id
LEFT JOIN taxonomy_categories fh ON c.funcao_historica_id = fh.id
LEFT JOIN taxonomy_categories tprinc ON c.tema_principal_id = tprinc.id
LEFT JOIN taxonomy_categories sm ON c.status_id = sm.id
LEFT JOIN taxonomy_categories cf ON c.capitulo_id = cf.id
LEFT JOIN media_assets ma ON c.media_id = ma.id
WHERE c.deleted_at IS NULL;

CREATE OR REPLACE VIEW v_catalogo_stats AS
SELECT
  COUNT(*) as total_itens,
  COUNT(DISTINCT area_fazenda_id) as areas_unicas,
  COUNT(DISTINCT nucleo_pecuaria_id) as nucleos_pecuaria_unicos,
  COUNT(DISTINCT nucleo_agro_id) as nucleos_agro_unicos,
  COUNT(DISTINCT status_id) as status_unicos,
  COUNT(media_id) as itens_com_midia,
  MIN(data_captacao) as data_mais_antiga,
  MAX(data_captacao) as data_mais_recente
FROM catalogo
WHERE deleted_at IS NULL;

CREATE OR REPLACE VIEW v_catalogo_audit_recente AS
SELECT
  ca.id,
  ca.item_id,
  ca.action,
  ca.field_name,
  ca.old_value,
  ca.new_value,
  ca.changed_at,
  ca.user_email,
  ci.titulo as item_titulo
FROM catalogo_audit ca
LEFT JOIN catalogo ci ON ca.item_id = ci.id
WHERE ca.changed_at >= NOW() - INTERVAL '30 days'
ORDER BY ca.changed_at DESC;
