# 💾 PERSISTÊNCIA E PRESERVAÇÃO
## Garantindo a Longevidade do Mundo Virtual

**Versão:** 1.0  
**Data:** 06 de Fevereiro de 2026  
**Status:** Estratégia de Preservação Obrigatória

---

## 🎯 PRINCÍPIO FUNDAMENTAL

> *"O mundo deve sobreviver a falhas de hardware, falhas humanas, falhas de software e falhas de organização. A preservação não é backup. É garantia de futuro."*

**Regra dos 3-2-1-1-0:**
- **3** cópias dos dados
- **2** tipos de mídia diferentes
- **1** cópia off-site
- **1** cópia offline/imutável (air-gapped)
- **0** erros após recuperação testada

---

## 📊 ESTRATÉGIA DE PRESERVAÇÃO EM CAMADAS

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PIRÂMIDE DE PRESERVAÇÃO                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                        ┌─────────────┐                                      │
│                        │   ATIVO     │  ← Dados em uso (hot)               │
│                        │   (Hot)     │     Latência: < 10ms                │
│                        │   SSD/DRAM  │     Retenção: Operação              │
│                        └──────┬──────┘                                      │
│                               │                                             │
│                    ┌──────────┴──────────┐                                  │
│                    │      WARM           │  ← Snapshots recentes           │
│                    │   (Warm Storage)    │     Latência: < 100ms           │
│                    │      NAS/S3         │     Retenção: 7-30 dias         │
│                    └──────────┬──────────┘                                  │
│                               │                                             │
│              ┌────────────────┴────────────────┐                            │
│              │              COLD               │  ← Arquivo histórico      │
│              │         (Cold Storage)          │     Latência: minutos       │
│              │        S3 Glacier/Deep          │     Retenção: 7 anos        │
│              └────────────────┬────────────────┘                            │
│                               │                                             │
│        ┌──────────────────────┴──────────────────────┐                      │
│        │                ARCHIVE                      │  ← Preservação      │
│        │         (Immutable Archive)                 │     permanente        │
│        │     Multiple Clouds + Physical              │     Retenção: Forever │
│        │          (M-DISC, LTO)                      │                       │
│        └─────────────────────────────────────────────┘                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 SNAPSHOTS DO MUNDO

### Frequência e Retenção

| Tipo | Frequência | Retenção | Storage | Propósito |
|------|------------|----------|---------|-----------|
| **Real-time** | Contínuo | 1 hora | RAM + SSD | Recuperação imediata |
| **Hot** | 10 minutos | 24 horas | SSD | Rollback rápido |
| **Warm** | 1 hora | 7 dias | NAS/S3 Standard | Recuperação de incidentes |
| **Daily** | 24 horas | 30 dias | S3 Standard-IA | Recuperação semanal |
| **Weekly** | 7 dias | 90 dias | S3 Glacier | Recuperação mensal |
| **Monthly** | 30 dias | 7 anos | S3 Glacier Deep | Compliance |
| **Yearly** | 365 dias | Forever | Multi-cloud + Physical | Preservação permanente |

### Formato de Snapshot

```json
{
  "snapshot_spec": {
    "version": "1.0.0",
    "snapshot_id": "snap_2026-02-06T00:00:00Z_norte",
    "world_version": "villa_canabrava.world.v2.3.1",
    "schema_version": "schema.v1.5.0",
    
    "metadata": {
      "timestamp": "2026-02-06T00:00:00.000Z",
      "shard_id": "norte",
      "shard_region": [-44.0, -17.4, -43.95, -17.35],
      "created_by": "snapshot-service@v2.1.0",
      "compression": "zstd:18"
    },
    
    "statistics": {
      "entity_count": 15420,
      "player_count": 127,
      "active_sessions": 45,
      "total_size_bytes": 52428800,
      "compressed_size_bytes": 8912896
    },
    
    "files": {
      "world_state": {
        "uri": "s3://villa-canabrava-snapshots/2026/02/06/world_state.usd.zst",
        "format": "openusd",
        "size_bytes": 25165824,
        "checksum": "sha256:a1b2c3d4e5f6..."
      },
      "entities": {
        "uri": "s3://villa-canabrava-snapshots/2026/02/06/entities.jsonl.zst",
        "format": "jsonl",
        "size_bytes": 15728640,
        "checksum": "sha256:b2c3d4e5f6g7..."
      },
      "players": {
        "uri": "s3://villa-canabrava-snapshots/2026/02/06/players.parquet",
        "format": "parquet",
        "size_bytes": 1048576,
        "checksum": "sha256:c3d4e5f6g7h8..."
      },
      "events": {
        "uri": "s3://villa-canabrava-snapshots/2026/02/06/events.jsonl.zst",
        "format": "jsonl",
        "size_bytes": 10485760,
        "checksum": "sha256:d4e5f6g7h8i9..."
      },
      "manifest": {
        "uri": "s3://villa-canabrava-snapshots/2026/02/06/manifest.json",
        "format": "json",
        "size_bytes": 4096,
        "checksum": "sha256:e5f6g7h8i9j0..."
      }
    },
    
    "restoration": {
      "estimated_time_seconds": 120,
      "dependencies": ["postgresql:16", "postgis:3.4"],
      "verification": {
        "checksum_algorithm": "sha256",
        "entity_count_verified": true,
        "referential_integrity": true
      }
    }
  }
}
```

### Script de Criação de Snapshot

```python
# snapshot_service.py
import asyncio
import json
import zstandard
import hashlib
from datetime import datetime
from typing import Dict, List
import boto3

class WorldSnapshotService:
    def __init__(self, db_pool, s3_client):
        self.db = db_pool
        self.s3 = s3_client
        self.bucket = "villa-canabrava-snapshots"
        
    async def create_snapshot(self, shard_id: str) -> Dict:
        """Cria um snapshot completo do mundo"""
        
        timestamp = datetime.utcnow()
        snapshot_id = f"snap_{timestamp.isoformat()}_{shard_id}"
        
        # 1. Coletar estado do mundo
        world_state = await self._collect_world_state(shard_id)
        
        # 2. Coletar entidades
        entities = await self._collect_entities(shard_id)
        
        # 3. Coletar jogadores ativos
        players = await self._collect_players(shard_id)
        
        # 4. Coletar eventos recentes
        events = await self._collect_events(shard_id, hours=1)
        
        # 5. Comprimir e salvar
        files = {}
        
        # World State (OpenUSD)
        files['world_state'] = await self._save_and_upload(
            data=world_state,
            filename=f"{snapshot_id}/world_state.usd",
            format='openusd'
        )
        
        # Entities (JSON Lines)
        files['entities'] = await self._save_and_upload(
            data=entities,
            filename=f"{snapshot_id}/entities.jsonl",
            format='jsonl'
        )
        
        # Players (Parquet)
        files['players'] = await self._save_and_upload(
            data=players,
            filename=f"{snapshot_id}/players.parquet",
            format='parquet'
        )
        
        # Events (JSON Lines)
        files['events'] = await self._save_and_upload(
            data=events,
            filename=f"{snapshot_id}/events.jsonl",
            format='jsonl'
        )
        
        # 6. Criar manifesto
        manifest = {
            "snapshot_spec": {
                "version": "1.0.0",
                "snapshot_id": snapshot_id,
                "world_version": await self._get_world_version(),
                "schema_version": await self._get_schema_version(),
                "metadata": {
                    "timestamp": timestamp.isoformat(),
                    "shard_id": shard_id,
                    "created_by": "snapshot-service@v2.1.0",
                    "compression": "zstd:18"
                },
                "statistics": {
                    "entity_count": len(entities),
                    "player_count": len(players),
                    "total_size_bytes": sum(f['size_bytes'] for f in files.values())
                },
                "files": files
            }
        }
        
        # 7. Salvar manifesto
        manifest_key = f"{snapshot_id}/manifest.json"
        self.s3.put_object(
            Bucket=self.bucket,
            Key=manifest_key,
            Body=json.dumps(manifest, indent=2).encode('utf-8'),
            ContentType='application/json',
            Metadata={'snapshot-id': snapshot_id}
        )
        
        return manifest
    
    async def _save_and_upload(self, data, filename: str, format: str) -> Dict:
        """Comprime, calcula checksum e faz upload"""
        
        # Serializar
        if format == 'jsonl':
            serialized = '\n'.join(json.dumps(item) for item in data).encode('utf-8')
        elif format == 'openusd':
            serialized = data.encode('utf-8')  # Já é USD serializado
        elif format == 'parquet':
            serialized = data  # Já é bytes
        else:
            serialized = json.dumps(data).encode('utf-8')
        
        # Comprimir com Zstd
        compressor = zstandard.ZstdCompressor(level=18)
        compressed = compressor.compress(serialized)
        
        # Calcular checksum
        checksum = hashlib.sha256(compressed).hexdigest()
        
        # Upload
        key = f"{filename}.zst"
        self.s3.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=compressed,
            ContentType='application/zstd',
            Metadata={
                'checksum-sha256': checksum,
                'uncompressed-size': str(len(serialized)),
                'compression': 'zstd:18'
            }
        )
        
        return {
            "uri": f"s3://{self.bucket}/{key}",
            "format": format,
            "size_bytes": len(compressed),
            "uncompressed_size_bytes": len(serialized),
            "checksum": f"sha256:{checksum}"
        }
```

---

## 📜 EVENT SOURCING (LOG DE EVENTOS)

### Conceito

O mundo é representado não apenas por seu estado atual, mas por **todos os eventos** que o levaram a esse estado. Isso permite:
- Replay completo da história
- Auditoria total
- Correção de erros via eventos compensatórios

### Modelo de Eventos

```protobuf
// events.proto
syntax = "proto3";

package villa_canabrava.events.v1;

message WorldEvent {
    // Identificação
    string event_id = 1;
    string event_type = 2;
    int64 sequence_number = 3;
    
    // Timestamp (ordenação)
    int64 timestamp_unix_nanos = 4;
    
    // Atores
    string actor_id = 5;        // Quem causou
    string actor_type = 6;      // user, system, admin
    
    // Alvo
    string entity_id = 7;       // O que foi afetado
    string entity_type = 8;
    
    // Payload específico do evento
    oneof payload {
        EntityCreated entity_created = 10;
        EntityUpdated entity_updated = 11;
        EntityDeleted entity_deleted = 12;
        EntityMoved entity_moved = 13;
        PlayerJoined player_joined = 14;
        PlayerLeft player_left = 15;
        WorldModified world_modified = 16;
    }
    
    // Metadados
    string shard_id = 20;
    string client_version = 21;
    string server_version = 22;
    map<string, string> metadata = 23;
}

message EntityCreated {
    string entity_id = 1;
    string entity_type = 2;
    Transform initial_transform = 3;
    map<string, bytes> initial_properties = 4;
}

message EntityUpdated {
    string entity_id = 1;
    repeated PropertyChange changes = 2;
}

message PropertyChange {
    string property_name = 1;
    bytes old_value = 2;
    bytes new_value = 3;
}

message EntityMoved {
    string entity_id = 1;
    Vector3 old_position = 2;
    Vector3 new_position = 3;
    Quaternion old_rotation = 4;
    Quaternion new_rotation = 5;
}
```

### Replay de Eventos

```python
# event_replay.py
class EventReplay:
    def __init__(self, event_store):
        self.event_store = event_store
    
    async def replay_to_state(self, entity_id: str, timestamp: datetime = None):
        """
        Reconstrói o estado de uma entidade a partir de seus eventos.
        Se timestamp for None, retorna estado atual.
        """
        
        # Buscar todos os eventos da entidade
        events = await self.event_store.get_events(
            entity_id=entity_id,
            up_to=timestamp
        )
        
        # Estado inicial vazio
        state = None
        
        # Aplicar cada evento
        for event in events:
            state = self._apply_event(state, event)
        
        return state
    
    def _apply_event(self, state, event):
        """Aplica um evento ao estado"""
        
        if event.type == 'entity.created':
            return Entity(
                id=event.entity_id,
                type=event.payload['entity_type'],
                transform=event.payload['initial_transform'],
                properties=event.payload['initial_properties']
            )
        
        elif event.type == 'entity.updated':
            for change in event.payload['changes']:
                state.properties[change['property_name']] = change['new_value']
            state.version += 1
            return state
        
        elif event.type == 'entity.moved':
            state.transform.position = event.payload['new_position']
            state.transform.rotation = event.payload['new_rotation']
            return state
        
        elif event.type == 'entity.deleted':
            return None  # Entidade removida
        
        return state
    
    async def replay_world(self, start_time: datetime, end_time: datetime):
        """
        Replay completo do mundo em um período.
        Útil para auditoria e debugging.
        """
        events = await self.event_store.get_events_in_range(
            start_time=start_time,
            end_time=end_time
        )
        
        world_states = []
        current_state = WorldState()
        
        for event in events:
            current_state = self._apply_event_to_world(current_state, event)
            world_states.append({
                'timestamp': event.timestamp,
                'state': current_state.copy()
            })
        
        return world_states
```

---

## 🗄️ ARMAZENAMENTO MULTI-CLOUD

### Estratégia de Distribuição

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DISTRIBUIÇÃO MULTI-CLOUD                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  PRIMARY (Hot)              SECONDARY (Warm)           TERTIARY (Cold)      │
│  ┌─────────────┐           ┌─────────────┐           ┌─────────────┐       │
│  │    AWS      │           │    GCP      │           │   Azure     │       │
│  │  us-east-1  │◀─────────▶│ us-central1 │◀─────────▶│  Brazil     │       │
│  │             │  Sync     │             │  Sync     │  South      │       │
│  │ • Snapshots │           │ • Snapshots │           │ • Snapshots │       │
│  │ • Assets    │           │ • Assets    │           │ • Assets    │       │
│  │ • Logs      │           │ • Logs      │           │ • Logs      │       │
│  └─────────────┘           └─────────────┘           └─────────────┘       │
│                                                                             │
│  POLÍTICA DE SINCRONIZAÇÃO:                                                │
│  • Assíncrona (eventual consistency)                                        │
│  • RPO: 5 minutos (Recovery Point Objective)                               │
│  • RTO: 30 minutos (Recovery Time Objective)                               │
│                                                                             │
│  OFFLINE (Immutable)                                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  • M-DISC (1000 anos)                                               │   │
│  │  • LTO-9 Tapes (30 anos)                                            │   │
│  │  • Armazenado em cofre físico                                       │   │
│  │  • Atualização: Anual                                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Código de Sincronização

```python
# multi_cloud_sync.py
import asyncio
import boto3
from google.cloud import storage as gcs
from azure.storage.blob import BlobServiceClient

class MultiCloudSync:
    def __init__(self):
        self.aws_s3 = boto3.client('s3')
        self.gcs = gcs.Client()
        self.azure = BlobServiceClient.from_connection_string(
            os.environ['AZURE_STORAGE_CONNECTION_STRING']
        )
        
        self.buckets = {
            'aws': 'villa-canabrava-snapshots',
            'gcp': 'villa-canabrava-snapshots',
            'azure': 'villacanabravasnapshots'
        }
    
    async def sync_object(self, key: str, source: str = 'aws'):
        """Sincroniza um objeto entre clouds"""
        
        # Download do source
        if source == 'aws':
            response = self.aws_s3.get_object(
                Bucket=self.buckets['aws'],
                Key=key
            )
            data = response['Body'].read()
        
        # Upload para outros clouds (em paralelo)
        destinations = ['gcp', 'azure']
        
        await asyncio.gather(*[
            self._upload_to_cloud(cloud, key, data)
            for cloud in destinations
        ])
        
        print(f"Sincronizado: {key}")
    
    async def _upload_to_cloud(self, cloud: str, key: str, data: bytes):
        """Faz upload para uma cloud específica"""
        
        if cloud == 'gcp':
            bucket = self.gcs.bucket(self.buckets['gcp'])
            blob = bucket.blob(key)
            blob.upload_from_string(data)
            
        elif cloud == 'azure':
            container = self.azure.get_container_client(
                self.buckets['azure']
            )
            container.upload_blob(name=key, data=data, overwrite=True)
```

---

## ✅ TESTES DE RECUPERAÇÃO

### Cronograma de Testes

| Frequência | Tipo | Escopo | Duração Máxima |
|------------|------|--------|----------------|
| Semanal | Snapshot individual | 1 shard | 30 minutos |
| Mensal | Snapshot completo | Todos shards | 2 horas |
| Trimestral | Disaster recovery | Full restore | 4 horas |
| Anual | Full DR + validação | + Verificação de integridade | 8 horas |

### Procedimento de Teste

```bash
#!/bin/bash
# disaster_recovery_test.sh

set -e

echo "=== DISASTER RECOVERY TEST ==="
echo "Data: $(date)"
echo ""

# 1. Selecionar snapshot de teste
SNAPSHOT_ID="snap_2026-02-06T00:00:00Z_norte"
echo "[1/6] Snapshot selecionado: $SNAPSHOT_ID"

# 2. Provisionar ambiente de recuperação
echo "[2/6] Provisionando ambiente de recuperação..."
terraform -chdir=./infra/recovery apply -auto-approve

# 3. Download do snapshot
echo "[3/6] Downloadando snapshot..."
aws s3 sync \
    s3://villa-canabrava-snapshots/$SNAPSHOT_ID/ \
    ./recovery/$SNAPSHOT_ID/

# 4. Verificar checksums
echo "[4/6] Verificando integridade..."
./scripts/verify_checksums.sh ./recovery/$SNAPSHOT_ID/

# 5. Restaurar banco de dados
echo "[5/6] Restaurando banco de dados..."
./scripts/restore_database.sh ./recovery/$SNAPSHOT_ID/

# 6. Validar restauração
echo "[6/6] Validando restauração..."
./scripts/validate_restoration.sh

# 7. Relatório
RECOVERY_TIME=$(($SECONDS / 60))
echo ""
echo "=== RESULTADO ==="
echo "Tempo de recuperação: ${RECOVERY_TIME} minutos"
echo "RTO alvo: 30 minutos"
echo "Status: $([ $RECOVERY_TIME -le 30 ] && echo 'PASS' || echo 'FAIL')"

# 8. Cleanup
echo "[Cleanup] Removendo ambiente de recuperação..."
terraform -chdir=./infra/recovery destroy -auto-approve

echo ""
echo "=== TESTE CONCLUÍDO ==="
```

---

**FIM DA PERSISTÊNCIA E PRESERVAÇÃO**
