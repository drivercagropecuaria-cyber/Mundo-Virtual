-- Migration: rename_catalogo_itens_to_catalogo
-- Created at: 1770369100
-- Purpose: Rename table catalogo_itens to catalogo (official table name per governance decision)

-- Rename table
ALTER TABLE catalogo_itens RENAME TO catalogo;

-- Rename indexes to match new table name
ALTER INDEX IF EXISTS idx_catalogo_deleted RENAME TO idx_catalogo_deleted_at;

-- Rename constraints
ALTER INDEX IF EXISTS catalogo_itens_pkey RENAME TO catalogo_pkey;

-- Update RLS policies to reference new table name
-- (This is handled by Postgres automatically when renaming the table)

-- Update soft_delete function reference
CREATE OR REPLACE FUNCTION soft_delete_catalogo_item(p_item_id INTEGER)
RETURNS void AS $$
BEGIN
  UPDATE catalogo 
  SET deleted_at = NOW()
  WHERE id = p_item_id AND deleted_at IS NULL;
END;
$$ LANGUAGE plpgsql;

-- Log migration
INSERT INTO public.audit_log (table_name, operation, record_id, user_id, details, created_at)
VALUES ('catalogo', 'SCHEMA_CHANGE', NULL, NULL, 'Renamed table catalogo_itens to catalogo', NOW())
ON CONFLICT DO NOTHING;
