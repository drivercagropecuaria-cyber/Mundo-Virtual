# ⚖️ GOVERNANÇA E VERSIONAMENTO
## Políticas de Evolução do Mundo Virtual

**Versão:** 1.0  
**Data:** 06 de Fevereiro de 2026  
**Status:** Políticas Obrigatórias

---

## 🎯 PRINCÍPIOS DE GOVERNANÇA

### 1. Transparência Total
Todas as decisões, mudanças e ações administrativas devem ser registradas e auditáveis.

### 2. Versionamento Semântico
Todas as componentes do mundo seguem Semantic Versioning (SemVer): `MAJOR.MINOR.PATCH`

### 3. Compatibilidade Garantida
- **Backward:** Novas versões suportam dados antigos
- **Forward:** Dados antigos podem ser migrados para novas versões

### 4. Recuperação Garantida
O mundo deve ser completamente restaurável a partir de snapshots e logs.

---

## 📊 ESTRUTURA DE VERSIONAMENTO

### Níveis de Versionamento

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    HIERARQUIA DE VERSIONAMENTO                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  NÍVEL 1: VERSÃO DO MUNDO (World Version)                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  villa_canabrava.world.v2.3.1                                       │   │
│  │                                                                     │   │
│  │  • MAJOR: Mudanças incompatíveis (ex: novo sistema de coordenadas) │   │
│  │  • MINOR: Novas features compatíveis (ex: novo tipo de entidade)   │   │
│  │  • PATCH: Correções de bugs, otimizações                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  NÍVEL 2: VERSÃO DE ESQUEMA (Schema Version)                                │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  schema.v1.5.0                                                      │   │
│  │                                                                     │   │
│  │  • Define estrutura de dados (tabelas, campos, relações)           │   │
│  │  • Migrações versionadas                                           │   │
│  │  • Documentação de breaking changes                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  NÍVEL 3: VERSÃO DE ASSET (Asset Version)                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  sede_villa_terezinha.v1.2.3                                        │   │
│  │                                                                     │   │
│  │  • Cada asset independente                                          │   │
│  │  • SemVer para evolução do asset                                    │   │
│  │  • Referências imutáveis                                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  NÍVEL 4: VERSÃO DE API (API Version)                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  /api/v1/...  /api/v2/...                                           │   │
│  │                                                                     │   │
│  │  • URL versioning                                                   │   │
│  │  • Deprecation policy                                               │   │
│  │  • Migration window                                                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🗄️ VERSIONAMENTO DE ESQUEMA

### Estrutura de Migrações

```
database/
├── migrations/
│   ├── schema_v1.0.0/           # Baseline
│   │   ├── 001_create_tables.sql
│   │   ├── 002_create_indexes.sql
│   │   └── 003_seed_data.sql
│   │
│   ├── schema_v1.1.0/           # Nova feature
│   │   ├── 001_add_entity_type.sql
│   │   └── 002_update_indexes.sql
│   │
│   ├── schema_v1.2.0/           # Outra feature
│   │   └── 001_add_user_preferences.sql
│   │
│   ├── schema_v2.0.0/           # Breaking change
│   │   ├── 001_migrate_coordinates.sql
│   │   ├── 002_drop_old_tables.sql
│   │   └── 003_create_new_tables.sql
│   │
│   └── rollback/                # Rollbacks (um por migração)
│       ├── rollback_v1.1.0_001.sql
│       └── rollback_v2.0.0_001.sql
│
└── seeds/                       # Dados iniciais
    ├── categories.sql
    └── default_users.sql
```

### Exemplo de Migração

```sql
-- migrations/schema_v1.1.0/001_add_entity_type.sql
-- Migration: Adicionar campo entity_subtype
-- Author: dev@example.com
-- Date: 2026-03-15
-- Ticket: VC-123

-- Up migration
ALTER TABLE world_v1.entities 
ADD COLUMN entity_subtype VARCHAR(100);

CREATE INDEX idx_entities_subtype 
ON world_v1.entities(entity_subtype);

-- Comentário documentando a mudança
COMMENT ON COLUMN world_v1.entities.entity_subtype 
IS 'Subtipo da entidade para categorização mais granular';

-- Registro da migração
INSERT INTO schema_migrations (version, migration_name, applied_at)
VALUES ('1.1.0', '001_add_entity_type', NOW());
```

```sql
-- rollback/rollback_v1.1.0_001.sql
-- Rollback: Remover campo entity_subtype

DROP INDEX IF EXISTS idx_entities_subtype;

ALTER TABLE world_v1.entities 
DROP COLUMN IF EXISTS entity_subtype;

DELETE FROM schema_migrations 
WHERE version = '1.1.0' AND migration_name = '001_add_entity_type';
```

### Ferramenta de Migração

```python
# migration_tool.py
import os
import psycopg2
from psycopg2.extras import RealDictCursor

class SchemaMigration:
    def __init__(self, db_url):
        self.conn = psycopg2.connect(db_url)
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        self._ensure_migration_table()
    
    def _ensure_migration_table(self):
        """Cria tabela de controle de migrações se não existir"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS schema_migrations (
                id SERIAL PRIMARY KEY,
                version VARCHAR(20) NOT NULL,
                migration_name VARCHAR(255) NOT NULL,
                applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                checksum VARCHAR(64),
                applied_by VARCHAR(100),
                UNIQUE(version, migration_name)
            )
        ''')
        self.conn.commit()
    
    def get_current_version(self):
        """Retorna versão atual do schema"""
        self.cursor.execute('''
            SELECT version FROM schema_migrations 
            ORDER BY applied_at DESC LIMIT 1
        ''')
        result = self.cursor.fetchone()
        return result['version'] if result else '0.0.0'
    
    def migrate(self, target_version=None):
        """Executa migrações até a versão alvo"""
        current = self.get_current_version()
        
        # Encontrar migrações pendentes
        migrations = self._get_pending_migrations(current, target_version)
        
        for migration in migrations:
            print(f"Aplicando: {migration['version']}/{migration['name']}")
            self._apply_migration(migration)
        
        print(f"Migração completa. Versão: {self.get_current_version()}")
    
    def rollback(self, steps=1):
        """Desfaz últimas N migrações"""
        for _ in range(steps):
            last_migration = self._get_last_migration()
            if not last_migration:
                print("Nenhuma migração para desfazer")
                return
            
            print(f"Revertendo: {last_migration['version']}/{last_migration['migration_name']}")
            self._apply_rollback(last_migration)
```

---

## 💾 PERSISTÊNCIA E PRESERVAÇÃO

### Estratégia de Snapshots

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ESTRATÉGIA DE SNAPSHOTS                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  FREQUÊNCIA          RETENÇÃO              ARMAZENAMENTO                     │
│  ┌──────────┐       ┌──────────┐          ┌──────────────┐                  │
│  │ Hot      │       │ 24 horas │          │ SSD local    │                  │
│  │ 10 min   │──────▶│          │─────────▶│              │                  │
│  └──────────┘       └──────────┘          └──────────────┘                  │
│                                                                             │
│  ┌──────────┐       ┌──────────┐          ┌──────────────┐                  │
│  │ Warm     │       │ 7 dias   │          │ NAS/S3       │                  │
│  │ 1 hora   │──────▶│          │─────────▶│ Standard     │                  │
│  └──────────┘       └──────────┘          └──────────────┘                  │
│                                                                             │
│  ┌──────────┐       ┌──────────┐          ┌──────────────┐                  │
│  │ Cold     │       │ 7 anos   │          │ S3 Glacier   │                  │
│  │ 1 dia    │──────▶│          │─────────▶│ Deep Archive │                  │
│  └──────────┘       └──────────┘          └──────────────┘                  │
│                                                                             │
│  ┌──────────┐       ┌──────────┐          ┌──────────────┐                  │
│  │ Archive  │       │ Forever  │          │ Multiple     │                  │
│  │ Mensal   │──────▶│          │─────────▶│ Clouds +     │                  │
│  └──────────┘       └──────────┘          │ Physical     │                  │
│                                           └──────────────┘                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Formato de Snapshot

```json
{
  "snapshot": {
    "id": "snap_2026-02-06T00:00:00Z_shard_norte",
    "version": "2.3.1",
    "timestamp": "2026-02-06T00:00:00Z",
    "shard_id": "norte",
    
    "statistics": {
      "entity_count": 15420,
      "player_count": 127,
      "size_bytes": 52428800
    },
    
    "format": {
      "type": "openusd+json",
      "version": "1.0"
    },
    
    "files": {
      "world_state": "s3://villa-canabrava-snapshots/snap_2026-02-06/world.usd.zst",
      "entities": "s3://villa-canabrava-snapshots/snap_2026-02-06/entities.jsonl.zst",
      "metadata": "s3://villa-canabrava-snapshots/snap_2026-02-06/metadata.json"
    },
    
    "checksums": {
      "world_state": "sha256:abc123...",
      "entities": "sha256:def456...",
      "metadata": "sha256:ghi789..."
    },
    
    "compression": {
      "algorithm": "zstd",
      "level": 18
    }
  }
}
```

### Event Sourcing (Log de Eventos)

```sql
-- Tabela de eventos do mundo
CREATE TABLE world_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(100) NOT NULL,
    
    -- Identificação
    entity_id UUID,
    player_id UUID,
    shard_id VARCHAR(50),
    
    -- Payload do evento
    payload JSONB NOT NULL,
    
    -- Metadados
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    sequence_number BIGINT NOT NULL,
    
    -- Rastreabilidade
    client_version VARCHAR(20),
    server_version VARCHAR(20),
    
    -- Índices
    INDEX idx_events_entity (entity_id, sequence_number),
    INDEX idx_events_time (timestamp),
    INDEX idx_events_type (event_type),
    INDEX idx_events_shard (shard_id)
);

-- Particionamento por mês
CREATE TABLE world_events_2026_02 PARTITION OF world_events
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
```

### Exemplo de Eventos

```json
// Evento: Entidade movida
{
  "event_id": "evt_abc123",
  "event_type": "entity.moved",
  "entity_id": "ent_sede_principal",
  "player_id": null,
  "shard_id": "norte",
  "payload": {
    "old_position": {"x": 0, "y": 0, "z": 0},
    "new_position": {"x": 10, "y": 0, "z": 5},
    "velocity": {"x": 1, "y": 0, "z": 0.5},
    "rotation": {"x": 0, "y": 0.707, "z": 0, "w": 0.707}
  },
  "timestamp": "2026-02-06T12:34:56.789Z",
  "sequence_number": 123456789,
  "client_version": "web.2.3.1",
  "server_version": "world.2.3.1"
}

// Evento: Player interagiu
{
  "event_type": "player.interacted",
  "player_id": "usr_joao_silva",
  "entity_id": "ent_porta_sede",
  "payload": {
    "interaction_type": "open",
    "position": {"x": 5, "y": 0, "z": 10}
  }
}

// Evento: Mundo modificado (admin)
{
  "event_type": "world.modified",
  "player_id": "admin_carlos",
  "payload": {
    "modification_type": "entity_added",
    "entity_type": "pivo_irrigacao",
    "properties": {
      "area_hectares": 45.89,
      "location": {"lat": -17.385, "lon": -43.948}
    }
  }
}
```

---

## 📋 POLÍTICAS DE DEPRECATION

### API Deprecation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CICLO DE VIDA DE API                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  v1.0.0 ──────▶ v1.1.0 ──────▶ v1.2.0 ──────▶ v2.0.0                      │
│    │              │              │              │                           │
│    │              │              │              │                           │
│    ▼              ▼              ▼              ▼                           │
│  STABLE       DEPRECATED      SUNSET        REMOVED                         │
│              (6 meses)      (12 meses)                                      │
│                                                                             │
│  Política:                                                                 │
│  - MINOR releases: adicionam features, não quebram compatibilidade         │
│  - MAJOR releases: podem ter breaking changes                              │
│  - APIs deprecated: 6 meses de warning antes de sunset                     │
│  - APIs em sunset: ainda funcionam, mas documentadas como legacy           │
│  - APIs removidas: não funcionam mais (após 12 meses de deprecation)       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Headers de Deprecation

```http
HTTP/1.1 200 OK
Deprecation: Sun, 01 Jun 2026 00:00:00 GMT
Sunset: Sun, 01 Dec 2026 00:00:00 GMT
Link: </api/v2/world/entities>; rel="successor-version"
Warning: 299 - "API version v1 is deprecated. Please migrate to v2."
```

---

## 🔐 AUDITORIA E LOGS

### Eventos Auditáveis

| Categoria | Eventos | Retenção |
|-----------|---------|----------|
| **Autenticação** | Login, logout, falhas | 2 anos |
| **Autorização** | Mudanças de permissão | 7 anos |
| **Mutação de Dados** | CRUD em entidades | 7 anos |
| **Administração** | Ações de admins | 10 anos |
| **Segurança** | Tentativas de ataque | 2 anos |

### Formato de Log de Auditoria

```json
{
  "audit_id": "aud_abc123",
  "timestamp": "2026-02-06T12:34:56.789Z",
  "severity": "INFO",
  "category": "DATA_MUTATION",
  
  "actor": {
    "type": "user",
    "id": "usr_joao_silva",
    "ip": "192.168.1.100",
    "user_agent": "Mozilla/5.0...",
    "session_id": "sess_xyz789"
  },
  
  "action": {
    "type": "entity.update",
    "resource": "world.entities",
    "resource_id": "ent_sede_principal",
    "description": "Atualização de propriedades da sede"
  },
  
  "context": {
    "before": {"name": "Sede Antiga"},
    "after": {"name": "Sede Villa Terezinha"},
    "changes": ["name"]
  },
  
  "result": {
    "status": "success",
    "affected_rows": 1
  }
}
```

---

## 📜 CHANGELOG

### Formato Keep a Changelog

```markdown
# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/spec/v2.0.0.html).

## [Unreleased]

### Added
- Novo sistema de particionamento espacial
- Suporte a WebTransport

### Changed
- Melhoria de performance no carregamento de assets (40% mais rápido)

### Deprecated
- API v1 será descontinuada em 2026-12-01

### Fixed
- Correção de memory leak no renderizador WebGPU

### Security
- Atualização de dependências com vulnerabilidades conhecidas

## [2.3.1] - 2026-02-06

### Fixed
- Correção de bug na sincronização de entidades

## [2.3.0] - 2026-01-15

### Added
- Suporte a hand tracking em VR
- Novo sistema de LOD adaptativo

### Changed
- Migração de WebGL2 para WebGPU como renderizador padrão

## [2.2.0] - 2025-12-01

### Added
- Integração com OpenUSD para assets
- Pipeline de fotogrametria automatizado
```

---

**FIM DA GOVERNANÇA E VERSIONAMENTO**
