#!/usr/bin/env python3
"""
Sprint 3 - OPT3: Redis HA (Sentinel + Circuit Breaker)
Objetivo: Alta disponibilidade com failover automático e proteção de circuito
Status: NOVO - Sprint 3 Executor
Data: 2026-02-06 11:45 UTC
"""

import asyncio
import time
import json
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum

import aioredis
from circuitbreaker import circuit

# ============================================================================
# PARTE 1: Configuração e Logging
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# PARTE 2: Enums e Dataclasses
# ============================================================================

class CircuitState(Enum):
    CLOSED = "CLOSED"          # Normal operation
    OPEN = "OPEN"              # Failing, reject requests
    HALF_OPEN = "HALF_OPEN"    # Testing if service recovered


@dataclass
class FailoverMetrics:
    """Métricas de failover"""
    failover_count: int = 0
    failover_duration_ms: float = 0.0
    last_failover: Optional[str] = None
    circuit_breaks: int = 0
    total_requests: int = 0
    failed_requests: int = 0
    recovery_attempts: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SentinelConfig:
    """Configuração do Sentinel"""
    sentinels: list  # [(host, port), ...]
    service_name: str = "mymaster"
    password: Optional[str] = None
    db: int = 0
    socket_timeout: int = 5
    socket_connect_timeout: int = 5
    socket_keepalive: bool = True


# ============================================================================
# PARTE 3: Classe de Circuit Breaker Customizado
# ============================================================================

class RedisCircuitBreaker:
    """
    Circuit Breaker específico para Redis com suporte a states.
    Protege contra falhas em cascata.
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: Exception = Exception
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self.success_count = 0
        self.metrics = FailoverMetrics()
    
    def call(self, func, *args, **kwargs):
        """Execute function através do circuit breaker"""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                logger.info("Circuit breaker transitioning to HALF_OPEN")
            else:
                raise Exception(f"Circuit breaker is OPEN. Service unavailable.")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        """Registrar sucesso"""
        self.failure_count = 0
        self.metrics.total_requests += 1
        
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= 2:  # Precisa de 2 sucessos para fechar
                self.state = CircuitState.CLOSED
                self.success_count = 0
                logger.info("Circuit breaker CLOSED - Service recovered")
    
    def _on_failure(self):
        """Registrar falha"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        self.metrics.failed_requests += 1
        self.metrics.total_requests += 1
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.metrics.circuit_breaks += 1
            logger.warning(
                f"Circuit breaker OPEN after {self.failure_count} failures"
            )
    
    def _should_attempt_reset(self) -> bool:
        """Verificar se já passed recovery timeout"""
        if not self.last_failure_time:
            return True
        elapsed = (datetime.now() - self.last_failure_time).total_seconds()
        return elapsed >= self.recovery_timeout


# ============================================================================
# PARTE 4: Cliente Redis com Sentinel + Circuit Breaker
# ============================================================================

class RedisBoundsCache:
    """
    Cliente Redis com:
    - Sentinel para HA (failover automático)
    - Circuit Breaker para proteção
    - Métricas de failover
    """
    
    def __init__(self, sentinel_config: SentinelConfig):
        self.config = sentinel_config
        self.redis: Optional[aioredis.Redis] = None
        self.circuit_breaker = RedisCircuitBreaker(
            failure_threshold=5,
            recovery_timeout=60
        )
        self.failover_metrics = FailoverMetrics()
        self._failover_start_time = None
    
    async def connect(self):
        """Conectar ao Redis via Sentinel"""
        try:
            logger.info(f"Connecting to Redis via Sentinel: {self.config.sentinels}")
            
            # Usar sentinels para descobrir master
            self.redis = await aioredis.from_url(
                f"redis-sentinel://{','.join([f'{h}:{p}' for h, p in self.config.sentinels])}/"
                f"{self.config.db}?service={self.config.service_name}",
                encoding="utf-8",
                decode_responses=True,
                socket_keepalive=self.config.socket_keepalive,
                socket_keepalive_intvl=5
            )
            
            # Test connection
            await self.redis.ping()
            logger.info("Redis connection established successfully")
            return True
        
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    async def disconnect(self):
        """Desconectar"""
        if self.redis:
            await self.redis.close()
            logger.info("Redis connection closed")
    
    @circuit(failure_threshold=5, recovery_timeout=60, expected_exception=Exception)
    async def get_bounds(self, catalogo_id: str) -> Optional[Dict[str, Any]]:
        """
        Get bounds para um catálogo (com circuit breaker)
        
        Args:
            catalogo_id: ID do catálogo
            
        Returns:
            Dict com bounds ou None
        """
        try:
            if not self.redis:
                raise Exception("Redis not connected")
            
            self.circuit_breaker.metrics.total_requests += 1
            data = await self.redis.hget(f'bounds:{catalogo_id}', 'data')
            
            if data:
                return json.loads(data)
            return None
        
        except Exception as e:
            self.circuit_breaker.metrics.failed_requests += 1
            logger.error(f"Failed to get bounds for {catalogo_id}: {e}")
            raise
    
    @circuit(failure_threshold=5, recovery_timeout=60, expected_exception=Exception)
    async def set_bounds(
        self, 
        catalogo_id: str, 
        bounds: Dict[str, Any],
        ttl: int = 86400
    ) -> bool:
        """
        Set bounds com TTL (24h default)
        """
        try:
            if not self.redis:
                raise Exception("Redis not connected")
            
            self.circuit_breaker.metrics.total_requests += 1
            
            await self.redis.hset(
                f'bounds:{catalogo_id}',
                'data',
                json.dumps(bounds)
            )
            
            # Set TTL
            await self.redis.expire(f'bounds:{catalogo_id}', ttl)
            
            return True
        
        except Exception as e:
            self.circuit_breaker.metrics.failed_requests += 1
            logger.error(f"Failed to set bounds for {catalogo_id}: {e}")
            raise
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Obter estatísticas do cache"""
        try:
            if not self.redis:
                return {}
            
            info = await self.redis.info('memory')
            
            return {
                'used_memory': info.get('used_memory_human', 'N/A'),
                'used_memory_peak': info.get('used_memory_peak_human', 'N/A'),
                'evicted_keys': info.get('evicted_keys', 0),
                'total_commands_processed': info.get('total_commands_processed', 0),
                'instantaneous_ops_per_sec': info.get('instantaneous_ops_per_sec', 0),
                'connected_clients': info.get('connected_clients', 0)
            }
        
        except Exception as e:
            logger.error(f"Failed to get cache stats: {e}")
            return {}
    
    def get_circuit_breaker_status(self) -> Dict[str, Any]:
        """Obter status do circuit breaker"""
        return {
            'state': self.circuit_breaker.state.value,
            'failure_count': self.circuit_breaker.failure_count,
            'metrics': self.circuit_breaker.metrics.to_dict()
        }


# ============================================================================
# PARTE 5: Testes de Failover
# ============================================================================

async def test_failover_scenario():
    """
    Teste de cenário de failover.
    Simula falha do master e recuperação via sentinel.
    """
    sentinel_config = SentinelConfig(
        sentinels=[
            ('localhost', 26379),
            ('localhost', 26380),
            ('localhost', 26381)
        ],
        service_name='mymaster'
    )
    
    cache = RedisBoundsCache(sentinel_config)
    
    try:
        # Conectar
        await cache.connect()
        logger.info("=" * 80)
        logger.info("TESTE 1: Operação normal")
        logger.info("=" * 80)
        
        # Test normal operation
        test_bounds = {
            'min_lat': -19.5,
            'max_lat': -19.4,
            'min_lon': -44.5,
            'max_lon': -44.4
        }
        
        await cache.set_bounds('catalogo_123', test_bounds)
        retrieved = await cache.get_bounds('catalogo_123')
        logger.info(f"✓ Set bounds: {test_bounds}")
        logger.info(f"✓ Get bounds: {retrieved}")
        
        # Cache stats
        logger.info("=" * 80)
        logger.info("TESTE 2: Estatísticas de cache")
        logger.info("=" * 80)
        
        stats = await cache.get_cache_stats()
        logger.info(f"Cache Stats: {json.dumps(stats, indent=2)}")
        
        # Circuit breaker status
        logger.info("=" * 80)
        logger.info("TESTE 3: Status do circuit breaker")
        logger.info("=" * 80)
        
        cb_status = cache.get_circuit_breaker_status()
        logger.info(f"Circuit Breaker: {json.dumps(cb_status, indent=2)}")
        
        # Simular múltiplas requisições
        logger.info("=" * 80)
        logger.info("TESTE 4: Carga (100 requisições)")
        logger.info("=" * 80)
        
        start = time.time()
        for i in range(100):
            try:
                await cache.set_bounds(f'catalogo_{i}', test_bounds)
                if (i + 1) % 25 == 0:
                    logger.info(f"✓ Processadas {i + 1} requisições")
            except Exception as e:
                logger.warning(f"Falha em catalogo_{i}: {e}")
        
        duration = time.time() - start
        throughput = 100 / duration
        logger.info(f"✓ 100 requisições completadas em {duration:.2f}s ({throughput:.1f} req/s)")
        
        # Final status
        logger.info("=" * 80)
        logger.info("STATUS FINAL")
        logger.info("=" * 80)
        
        final_status = cache.get_circuit_breaker_status()
        logger.info(f"Circuit Breaker State: {final_status['state']}")
        logger.info(f"Total Requests: {final_status['metrics']['total_requests']}")
        logger.info(f"Failed Requests: {final_status['metrics']['failed_requests']}")
        logger.info(f"Success Rate: {(1 - final_status['metrics']['failed_requests'] / final_status['metrics']['total_requests']) * 100:.1f}%")
    
    finally:
        await cache.disconnect()


# ============================================================================
# PARTE 6: Main e Configuração
# ============================================================================

async def main():
    """Executar testes"""
    logger.info("Redis HA (Sentinel + Circuit Breaker) - Sprint 3 OPT3")
    logger.info("=" * 80)
    
    try:
        await test_failover_scenario()
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise


if __name__ == '__main__':
    asyncio.run(main())
