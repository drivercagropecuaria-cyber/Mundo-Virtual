BEGIN;

CREATE OR REPLACE FUNCTION villa_canabrava.set_updated_at()
RETURNS trigger AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_geo_features_updated_at ON villa_canabrava.geo_features;
CREATE TRIGGER trg_geo_features_updated_at
BEFORE UPDATE ON villa_canabrava.geo_features
FOR EACH ROW EXECUTE FUNCTION villa_canabrava.set_updated_at();

DROP TRIGGER IF EXISTS trg_layers_updated_at ON villa_canabrava.layers;
CREATE TRIGGER trg_layers_updated_at
BEFORE UPDATE ON villa_canabrava.layers
FOR EACH ROW EXECUTE FUNCTION villa_canabrava.set_updated_at();

COMMIT;
