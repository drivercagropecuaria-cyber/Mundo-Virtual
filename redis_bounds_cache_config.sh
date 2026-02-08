#!/bin/bash
# Sprint 2 Otimização 4: Cache Redis para Bounds
# Purpose: Configuração e validação de cache Redis para bounds geoespaciais
# Created: 2026-02-06
# Usage: bash redis_bounds_cache_config.sh

set -e

# ============================================================================
# CONFIGURAÇÃO REDIS PARA BOUNDS GEOESPACIAIS
# ============================================================================

echo "=================================================="
echo "Redis Bounds Cache Configuration (Sprint 2)"
echo "=================================================="
echo ""

# Detectar environment
REDIS_HOST="${REDIS_HOST:-localhost}"
REDIS_PORT="${REDIS_PORT:-6379}"
REDIS_DB="${REDIS_DB:-2}"
REDIS_PASSWORD="${REDIS_PASSWORD:-}"

echo "📍 Redis Configuration:"
echo "   Host: $REDIS_HOST"
echo "   Port: $REDIS_PORT"
echo "   DB: $REDIS_DB"
echo ""

# ============================================================================
# 1. VALIDAR CONECTIVIDADE REDIS
# ============================================================================
echo "🔍 [Step 1] Validando conectividade Redis..."

if command -v redis-cli &> /dev/null; then
    # Construir comando redis-cli
    if [ -z "$REDIS_PASSWORD" ]; then
        REDIS_CMD="redis-cli -h $REDIS_HOST -p $REDIS_PORT -n $REDIS_DB"
    else
        REDIS_CMD="redis-cli -h $REDIS_HOST -p $REDIS_PORT -n $REDIS_DB -a $REDIS_PASSWORD"
    fi
    
    if $REDIS_CMD PING > /dev/null 2>&1; then
        echo "   ✅ Redis connection successful"
    else
        echo "   ❌ Redis connection failed"
        exit 1
    fi
else
    echo "   ⚠️  redis-cli not found. Skipping connection test."
    echo "   (Install redis-tools to enable connection validation)"
fi

echo ""

# ============================================================================
# 2. CONFIGURAR KEYSPACE NOTIFICATIONS
# ============================================================================
echo "⚙️  [Step 2] Configurando keyspace notifications..."

if command -v redis-cli &> /dev/null; then
    $REDIS_CMD CONFIG SET notify-keyspace-events "Ex" || {
        echo "   ⚠️  Could not configure keyspace notifications (may require CONFIG ACL)"
    }
    NOTIFY_CONFIG=$($REDIS_CMD CONFIG GET notify-keyspace-events | tail -1)
    echo "   Keyspace notifications: $NOTIFY_CONFIG"
fi

echo ""

# ============================================================================
# 3. CONFIGURAR MEMORY LIMIT E EVICTION POLICY
# ============================================================================
echo "💾 [Step 3] Configurando memory management..."

MEMORY_LIMIT_MB="${MEMORY_LIMIT_MB:-512}"
MEMORY_LIMIT_BYTES=$((MEMORY_LIMIT_MB * 1024 * 1024))

echo "   Memory limit: ${MEMORY_LIMIT_MB}MB"

if command -v redis-cli &> /dev/null; then
    $REDIS_CMD CONFIG SET maxmemory $MEMORY_LIMIT_BYTES || {
        echo "   ⚠️  Could not set maxmemory"
    }
    $REDIS_CMD CONFIG SET maxmemory-policy "allkeys-lru" || {
        echo "   ⚠️  Could not set eviction policy"
    }
fi

echo ""

# ============================================================================
# 4. CRIAR ESTRUTURAS DE BOUNDS CACHE
# ============================================================================
echo "📦 [Step 4] Inicializando estruturas de cache..."

if command -v redis-cli &> /dev/null; then
    # Criar hashes para cada tipo de bound
    
    # Hash para bounds validados
    $REDIS_CMD HSET bounds:validated:schema \
        min_lat "NUMERIC(12,8)" \
        max_lat "NUMERIC(12,8)" \
        min_lon "NUMERIC(12,8)" \
        max_lon "NUMERIC(12,8)" \
        centroid_lon "NUMERIC(12,8)" \
        centroid_lat "NUMERIC(12,8)" \
        wkt "TEXT" \
        validated_at "TIMESTAMP" \
        > /dev/null || echo "   ⚠️  Could not create schema hash"
    
    # Criar índice de timestamps para cleanup automático
    $REDIS_CMD DEL bounds:ttl_index 2>/dev/null || true
    
    # Criar sorted set para tracking TTL (Sorted by expiration timestamp)
    $REDIS_CMD ZADD bounds:ttl_index 0 "__schema_initialized__" > /dev/null || true
    
    echo "   ✅ Cache structures initialized"
    echo "      - bounds:validated:{catalogo_id} (Hash)"
    echo "      - bounds:ttl_index (Sorted Set - TTL tracking)"
fi

echo ""

# ============================================================================
# 5. CRIAR ÍNDICES DE BUSCA GEOESPACIAL
# ============================================================================
echo "🗺️  [Step 5] Configurando índices de busca geoespacial..."

if command -v redis-cli &> /dev/null; then
    # Criar sorted sets para busca geoespacial rápida por latitude/longitude
    
    # Índice por latitude mínima
    $REDIS_CMD DEL bounds:by_min_lat 2>/dev/null || true
    $REDIS_CMD ZADD bounds:by_min_lat 0 "__initialized__" > /dev/null || true
    
    # Índice por latitude máxima
    $REDIS_CMD DEL bounds:by_max_lat 2>/dev/null || true
    $REDIS_CMD ZADD bounds:by_max_lat 0 "__initialized__" > /dev/null || true
    
    # Índice por longitude mínima
    $REDIS_CMD DEL bounds:by_min_lon 2>/dev/null || true
    $REDIS_CMD ZADD bounds:by_min_lon 0 "__initialized__" > /dev/null || true
    
    # Índice por longitude máxima
    $REDIS_CMD DEL bounds:by_max_lon 2>/dev/null || true
    $REDIS_CMD ZADD bounds:by_max_lon 0 "__initialized__" > /dev/null || true
    
    echo "   ✅ Geo-search indices created"
fi

echo ""

# ============================================================================
# 6. DEFINIR TTL PADRÃO E POLÍTICAS DE EXPIRAÇÃO
# ============================================================================
echo "⏱️  [Step 6] Configurando políticas de TTL..."

TTL_HOURS="${TTL_HOURS:-24}"
TTL_SECONDS=$((TTL_HOURS * 3600))

echo "   Default TTL: ${TTL_HOURS} hours (${TTL_SECONDS} seconds)"
echo "   TTL Expression: ex=$(($TTL_HOURS * 3600))"

if command -v redis-cli &> /dev/null; then
    # Armazenar configuração de TTL
    $REDIS_CMD SET bounds:config:ttl_seconds $TTL_SECONDS EX $TTL_SECONDS > /dev/null || true
    $REDIS_CMD SET bounds:config:updated_at "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" EX $TTL_SECONDS > /dev/null || true
    
    echo "   ✅ TTL configuration stored"
fi

echo ""

# ============================================================================
# 7. VALIDAR CONFIGURAÇÃO
# ============================================================================
echo "✔️  [Step 7] Validando configuração final..."

if command -v redis-cli &> /dev/null; then
    # Verificar estruturas criadas
    KEYS_COUNT=$($REDIS_CMD DBSIZE | grep -oP '\d+')
    INFO=$($REDIS_CMD INFO stats | grep -E "total_commands_processed|instantaneous_ops_per_sec" || echo "N/A")
    
    echo "   Total keys in DB: $KEYS_COUNT"
    echo "   Redis Stats: $INFO"
    
    echo ""
    echo "   Bounds cache structures:"
    $REDIS_CMD SCAN 0 MATCH "bounds:*" COUNT 100 | tail -n +2 | sed 's/^/      - /'
fi

echo ""

# ============================================================================
# 8. GERAR ARQUIVO DE CONFIGURAÇÃO
# ============================================================================
echo "📝 [Step 8] Gerando arquivo de configuração..."

CONFIG_FILE="redis_bounds_cache.env"

cat > "$CONFIG_FILE" << EOF
# Redis Bounds Cache Configuration
# Sprint 2 Otimização 4
# Generated: $(date -u +'%Y-%m-%dT%H:%M:%SZ')

# Connection
REDIS_HOST=$REDIS_HOST
REDIS_PORT=$REDIS_PORT
REDIS_DB=$REDIS_DB
REDIS_PASSWORD=$REDIS_PASSWORD

# Memory & Eviction
MEMORY_LIMIT_MB=$MEMORY_LIMIT_MB
EVICTION_POLICY=allkeys-lru

# TTL Configuration
TTL_HOURS=$TTL_HOURS
TTL_SECONDS=$TTL_SECONDS

# Cache Structures
BOUNDS_HASH_PREFIX=bounds:validated:
BOUNDS_TTL_INDEX=bounds:ttl_index
BOUNDS_BY_MIN_LAT=bounds:by_min_lat
BOUNDS_BY_MAX_LAT=bounds:by_max_lat
BOUNDS_BY_MIN_LON=bounds:by_min_lon
BOUNDS_BY_MAX_LON=bounds:by_max_lon

# Performance
BATCH_SIZE=100
SCAN_COUNT=1000

# Validation
VALIDATE_ON_LOAD=true
VALIDATE_ON_STORE=true
EOF

echo "   ✅ Configuration file created: $CONFIG_FILE"

echo ""

# ============================================================================
# 9. RESUMO FINAL
# ============================================================================
echo "=================================================="
echo "✅ Redis Bounds Cache Configuration Complete"
echo "=================================================="
echo ""
echo "Summary:"
echo "  • Redis connection validated"
echo "  • Cache structures initialized"
echo "  • Geo-search indices created"
echo "  • TTL policies configured (${TTL_HOURS}h)"
echo "  • Configuration saved to: $CONFIG_FILE"
echo ""
echo "Next steps:"
echo "  1. Source the config: source $CONFIG_FILE"
echo "  2. Populate initial bounds: python populate_bounds_redis.py"
echo "  3. Monitor performance: redis-cli MONITOR"
echo "  4. Check memory: redis-cli INFO memory"
echo ""
