-- Migration: create_view_catalogo_completo
-- Created at: 1770369000
-- Description: Criar view v_catalogo_completo com filtro de itens ativos
-- Esta view é usada pela RPC search_catalogo para retornar resultados filtrados
-- ATUALIZACAO: Removidas referencias a tabela renomeada (ver migration 1770369100)

-- Adicionar coluna is_active na tabela catalogo (se ainda não existir)
ALTER TABLE catalogo
ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT true;

-- Adicionar coluna localidade_geom na tabela catalogo (se ainda não existir)
ALTER TABLE catalogo
ADD COLUMN IF NOT EXISTS localidade_geom GEOMETRY(POINT, 4326);

-- Criar índice para performance em queries de is_active
CREATE INDEX IF NOT EXISTS idx_catalogo_is_active ON catalogo(is_active)
WHERE deleted_at IS NULL;

-- Criar índice geométrico para localidade_geom (se spatial indexes forem necessários)
CREATE INDEX IF NOT EXISTS idx_catalogo_localidade_geom ON catalogo
USING GIST(localidade_geom)
WHERE deleted_at IS NULL;

-- DROP VIEW se existir (para evitar conflitos)
DROP VIEW IF EXISTS v_catalogo_completo CASCADE;

-- CREATE OR REPLACE VIEW v_catalogo_completo
-- Seleciona apenas itens ativos (deleted_at IS NULL AND is_active = true)
-- Inclui todos os campos necessários para a RPC search_catalogo
CREATE OR REPLACE VIEW v_catalogo_completo AS
SELECT
  c.id,
  c.titulo,
  c.descricao,
  c.identificador AS categoria,
  c.data_captacao AS data_criacao,
  c.arquivo_url,
  c.thumbnail_url,
  c.localidade_geom,
  c.is_active,
  c.deleted_at,
  c.created_at,
  c.updated_at,
  -- Campos adicionais do catalogo
  c.frase_memoria,
  c.observacoes,
  c.responsavel,
  c.media_id,
  -- IDs das relações
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
  c.capitulo_id
FROM catalogo c
WHERE c.deleted_at IS NULL AND c.is_active = true;

-- Comentar a view
COMMENT ON VIEW v_catalogo_completo IS
'View que contém todos os itens do catálogo ativos (não deletados e is_active=true).
Usada pela RPC search_catalogo para retornar resultados filtrados.
Inclui campos essenciais: id, titulo, descricao, categoria, data_criacao, arquivo_url,
thumbnail_url, localidade_geom, is_active, deleted_at, created_at, updated_at';

-- Conceder permissões de leitura para roles públicos
GRANT SELECT ON v_catalogo_completo TO anon, authenticated;
