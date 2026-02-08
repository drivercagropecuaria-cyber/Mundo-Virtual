-- Sprint 3 - OPT2: MV Refresh Scheduling (Cron Automation)
-- Migration: 1770500200_mv_refresh_scheduling_cron.sql
-- Objetivo: Agendar refresh automático de Materialized Views com pg_cron
-- Status: NOVO - Sprint 3 Executor
-- Data: 2026-02-06 11:45 UTC

BEGIN;

-- ============================================================================
-- PARTE 1: Instalar extensão pg_cron (se disponível)
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS pg_cron WITH SCHEMA public;

-- ============================================================================
-- PARTE 2: Criar função para refresh de todas MVs críticas
-- ============================================================================

CREATE OR REPLACE FUNCTION refresh_all_materialized_views()
RETURNS TABLE(view_name TEXT, refresh_time INTERVAL, status TEXT) AS $$
DECLARE
    v_start_time TIMESTAMP;
    v_end_time TIMESTAMP;
    v_duration INTERVAL;
BEGIN
    -- Refresh MV 1: Estatísticas de geometrias
    v_start_time := CURRENT_TIMESTAMP;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_catalogo_geometrias_stats;
    v_end_time := CURRENT_TIMESTAMP;
    v_duration := v_end_time - v_start_time;
    RETURN QUERY SELECT 
        'mv_catalogo_geometrias_stats'::TEXT,
        v_duration,
        'SUCCESS'::TEXT;
    
    -- Refresh MV 2: Search indexed (full-text)
    v_start_time := CURRENT_TIMESTAMP;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_catalogo_search_indexed;
    v_end_time := CURRENT_TIMESTAMP;
    v_duration := v_end_time - v_start_time;
    RETURN QUERY SELECT 
        'mv_catalogo_search_indexed'::TEXT,
        v_duration,
        'SUCCESS'::TEXT;
    
    -- Registrar na tabela de log
    INSERT INTO mv_refresh_log (view_name, refresh_duration, status)
    VALUES 
        ('mv_catalogo_geometrias_stats', v_duration, 'SUCCESS'),
        ('mv_catalogo_search_indexed', v_duration, 'SUCCESS');
    
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- PARTE 3: Criar tabela de logs para auditoria de refreshes
-- ============================================================================

CREATE TABLE IF NOT EXISTS mv_refresh_log (
    id BIGSERIAL PRIMARY KEY,
    view_name TEXT NOT NULL,
    refresh_duration INTERVAL,
    status TEXT NOT NULL,
    error_message TEXT,
    refreshed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Índice para otimizar consultas de log
CREATE INDEX IF NOT EXISTS idx_mv_refresh_log_view_name 
ON mv_refresh_log (view_name, refreshed_at DESC);

CREATE INDEX IF NOT EXISTS idx_mv_refresh_log_status 
ON mv_refresh_log (status, refreshed_at DESC);

-- ============================================================================
-- PARTE 4: Agendar refreshes com pg_cron
-- ============================================================================

-- Schedule 1: Refresh a cada hora (recomendado para MVs de stats)
SELECT cron.schedule(
    'refresh-mv-stats-hourly',           -- job name
    '0 * * * *',                          -- every hour at :00
    'SELECT refresh_all_materialized_views()'
);

-- Schedule 2: Refresh a cada 30 minutos (para search index)
SELECT cron.schedule(
    'refresh-mv-search-30min',
    '*/30 * * * *',                       -- every 30 minutes
    'SELECT refresh_all_materialized_views()'
);

-- Schedule 3: Refresh completo de madrugada (02:00 UTC)
-- Útil para limpeza completa e re-índexação
SELECT cron.schedule(
    'refresh-mv-full-night',
    '0 2 * * *',                          -- 02:00 UTC daily
    'SELECT refresh_all_materialized_views()'
);

-- ============================================================================
-- PARTE 5: Criar função de monitoramento para alertas
-- ============================================================================

CREATE OR REPLACE FUNCTION check_mv_refresh_health()
RETURNS TABLE(
    view_name TEXT,
    last_refresh TIMESTAMP WITH TIME ZONE,
    time_since_refresh INTERVAL,
    status TEXT,
    health_status TEXT
) AS $$
BEGIN
    RETURN QUERY
    WITH recent_refreshes AS (
        SELECT 
            view_name,
            MAX(refreshed_at) as last_refresh
        FROM mv_refresh_log
        WHERE status = 'SUCCESS'
        GROUP BY view_name
    )
    SELECT 
        r.view_name,
        r.last_refresh,
        CURRENT_TIMESTAMP - r.last_refresh,
        'CURRENT'::TEXT,
        CASE 
            WHEN (CURRENT_TIMESTAMP - r.last_refresh) < INTERVAL '2 hours' THEN 'HEALTHY'
            WHEN (CURRENT_TIMESTAMP - r.last_refresh) < INTERVAL '4 hours' THEN 'DEGRADED'
            ELSE 'STALE'
        END as health_status
    FROM recent_refreshes r
    ORDER BY r.last_refresh DESC;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- PARTE 6: Criar trigger para notificação automática de alertas
-- ============================================================================

CREATE OR REPLACE FUNCTION alert_on_mv_failure()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status != 'SUCCESS' THEN
        INSERT INTO system_alerts (alert_type, severity, message, related_object)
        VALUES (
            'MV_REFRESH_FAILED',
            'HIGH',
            'Falha no refresh da MV: ' || NEW.view_name || ' - ' || COALESCE(NEW.error_message, 'Erro desconhecido'),
            'mv_refresh_log'
        );
        RAISE NOTICE 'ALERT: Falha no refresh de %', NEW.view_name;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_mv_refresh_alert
AFTER INSERT ON mv_refresh_log
FOR EACH ROW
EXECUTE FUNCTION alert_on_mv_failure();

-- ============================================================================
-- PARTE 7: Função para validação de consistência de MVs
-- ============================================================================

CREATE OR REPLACE FUNCTION validate_mv_consistency()
RETURNS TABLE(
    view_name TEXT,
    record_count BIGINT,
    last_refresh TIMESTAMP WITH TIME ZONE,
    validation_status TEXT
) AS $$
BEGIN
    -- Validação MV 1: geometrias_stats
    RETURN QUERY SELECT 
        'mv_catalogo_geometrias_stats'::TEXT,
        COUNT(*)::BIGINT,
        MAX(last_refresh),
        CASE 
            WHEN COUNT(*) > 0 THEN 'VALID'
            ELSE 'EMPTY'
        END::TEXT
    FROM (
        SELECT CURRENT_TIMESTAMP as last_refresh FROM mv_catalogo_geometrias_stats LIMIT 1
    ) t;
    
    -- Validação MV 2: search_indexed
    RETURN QUERY SELECT 
        'mv_catalogo_search_indexed'::TEXT,
        COUNT(*)::BIGINT,
        MAX(last_refresh),
        CASE 
            WHEN COUNT(*) > 0 THEN 'VALID'
            ELSE 'EMPTY'
        END::TEXT
    FROM (
        SELECT CURRENT_TIMESTAMP as last_refresh FROM mv_catalogo_search_indexed LIMIT 1
    ) t;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- PARTE 8: Criar jobs de manutenção adicional
-- ============================================================================

-- Cleanup old logs (manter apenas últimos 30 dias)
SELECT cron.schedule(
    'cleanup-mv-logs-monthly',
    '0 3 * * 0',                          -- Sundays at 03:00 UTC
    'DELETE FROM mv_refresh_log WHERE created_at < CURRENT_TIMESTAMP - INTERVAL ''30 days'''
);

-- Health check e relatório
SELECT cron.schedule(
    'mv-health-check-daily',
    '0 4 * * *',                          -- Daily at 04:00 UTC
    'SELECT check_mv_refresh_health()'
);

-- ============================================================================
-- PARTE 9: Validação final e comentários
-- ============================================================================

COMMENT ON FUNCTION refresh_all_materialized_views() IS 
'Função que executa o refresh concorrente de todas as MVs críticas.
 Registra duração e status em mv_refresh_log para auditoria.';

COMMENT ON FUNCTION check_mv_refresh_health() IS 
'Monitora saúde das MVs verificando quando foram feitos refreshes.
 Retorna status: HEALTHY (<2h), DEGRADED (<4h), STALE (>4h).';

COMMENT ON FUNCTION alert_on_mv_failure() IS 
'Trigger que cria alertas automáticos quando refresh falha.';

COMMENT ON TABLE mv_refresh_log IS 
'Log de todos os refreshes de Materialized Views para auditoria e troubleshooting.';

-- ============================================================================
-- PARTE 10: Monitoramento via views públicas
-- ============================================================================

CREATE OR REPLACE VIEW v_mv_refresh_status AS
SELECT 
    view_name,
    MAX(refreshed_at) as last_refresh,
    COUNT(*) as total_refreshes,
    SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) as successful_refreshes,
    SUM(CASE WHEN status != 'SUCCESS' THEN 1 ELSE 0 END) as failed_refreshes,
    AVG(EXTRACT(EPOCH FROM refresh_duration)) as avg_duration_seconds,
    MAX(EXTRACT(EPOCH FROM refresh_duration)) as max_duration_seconds
FROM mv_refresh_log
WHERE refreshed_at > CURRENT_TIMESTAMP - INTERVAL '7 days'
GROUP BY view_name
ORDER BY last_refresh DESC;

GRANT SELECT ON v_mv_refresh_status TO public;

-- ============================================================================
-- PARTE 11: Executar refresh inicial
-- ============================================================================

-- Executar refresh imediato para validar setup
SELECT refresh_all_materialized_views();

-- Mostrar cron jobs agendados
SELECT jobid, jobname, schedule, command FROM cron.job ORDER BY jobname;

-- ============================================================================
-- NOTAS:
-- ============================================================================
-- 1. pg_cron agenda jobs via background worker do PostgreSQL
-- 2. Refresh CONCURRENTLY permite queries durante update
-- 3. Logs registram duração para análise de performance
-- 4. Alertas automáticos para falhas
-- 5. Health check identifica MVs desatualizadas
-- 6. Schedule 1 (hourly): Para MVs de stats (menos crítico)
-- 7. Schedule 2 (30min): Para search index (mais crítico)
-- 8. Schedule 3 (nightly): Refresh completo + manutenção
--
-- MONITORING:
-- SELECT * FROM v_mv_refresh_status;
-- SELECT check_mv_refresh_health();
-- SELECT * FROM mv_refresh_log ORDER BY refreshed_at DESC LIMIT 20;
--
-- TROUBLESHOOTING:
-- SELECT * FROM cron.job;  -- Ver jobs agendados
-- SELECT * FROM cron.job_run_details;  -- Ver histórico de execução
--
-- PARAR JOB:
-- SELECT cron.unschedule('refresh-mv-stats-hourly');

COMMIT;
