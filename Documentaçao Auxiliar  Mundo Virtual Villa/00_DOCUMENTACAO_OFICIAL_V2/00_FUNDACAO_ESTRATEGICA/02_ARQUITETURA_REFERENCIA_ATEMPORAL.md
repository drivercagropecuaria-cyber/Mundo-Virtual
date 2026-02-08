# 🏛️ ARQUITETURA DE REFERÊNCIA ATEMPORAL
## Camadas que Envelhecem Bem

**Versão:** 1.0  
**Data:** 06 de Fevereiro de 2026  
**Status:** Arquitetura de Referência  
**Padrão:** Atemporal / Standards-First

---

## 📐 VISÃO GERAL DA ARQUITETURA

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ARQUITETURA ATEMPORAL VILLA CANABRAVA                    │
│                         "Camadas que Envelhecem Bem"                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  CAMADA 6: CLIENTES (Substituíveis)                                 │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │   Web    │  │   VR     │  │  Mobile  │  │ Desktop  │            │   │
│  │  │  Browser │  │  OpenXR  │  │  Native  │  │  Native  │            │   │
│  │  │  WebGPU  │  │  Headset │  │   App    │  │   App    │            │   │
│  │  │  WebXR   │  │          │  │          │  │          │            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  │                                                                     │   │
│  │  NOTA: Estes clientes podem ser trocados, adicionados ou           │   │
│  │  removidos SEM AFETAR O MUNDO. O mundo continua existindo.         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ▲                                        │
│                                    │ HTTP/3, WebSocket, WebRTC              │
│                                    │                                        │
│  ┌─────────────────────────────────┴───────────────────────────────────┐   │
│  │  CAMADA 5: API GATEWAY (Fachada)                                    │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │  • Rate Limiting  • Auth  • Routing  • Caching  • Metrics   │   │   │
│  │  │  • Kong / AWS API Gateway / Traefik (substituível)          │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ▲                                        │
│                                    │ gRPC / GraphQL / REST                  │
│                                    │                                        │
│  ┌─────────────────────────────────┴───────────────────────────────────┐   │
│  │  CAMADA 4: SERVIÇOS DE DOMÍNIO (O Mundo)                            │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │   │
│  │  │   World      │  │   Content    │  │   Social     │  │ Economy  │ │   │
│  │  │   Service    │  │   Service    │  │   Service    │  │ Service  │ │   │
│  │  │              │  │              │  │              │  │          │ │   │
│  │  │ • Estado     │  │ • Assets     │  │ • Chat       │  │ • Currency│ │   │
│  │  │ • Posições   │  │ • Scenes     │  │ • Presence   │  │ • Trade   │ │   │
│  │  │ • Physics    │  │ • Metadata   │  │ • Groups     │  │ • Market  │ │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────┘ │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │   │
│  │  │   GIS        │  │   Museum     │  │   User       │  │ Analytics│ │   │
│  │  │   Service    │  │   Service    │  │   Service    │  │ Service  │ │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ▲                                        │
│                                    │ Event Bus / Message Queue              │
│                                    │                                        │
│  ┌─────────────────────────────────┴───────────────────────────────────┐   │
│  │  CAMADA 3: SIMULAÇÃO AUTORITATIVA (A Verdade)                       │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │  SIMULATION ENGINE                                          │   │   │
│  │  │  • Tick loop (20-60 Hz)                                     │   │   │
│  │  │  • State reconciliation                                     │   │   │
│  │  │  • Spatial partitioning                                     │   │   │
│  │  │  • Interest management                                      │   │   │
│  │  │  • Anti-cheat validation                                    │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ▲                                        │
│                                    │ SQL / NoSQL / Cache                    │
│                                    │                                        │
│  ┌─────────────────────────────────┴───────────────────────────────────┐   │
│  │  CAMADA 2: PERSISTÊNCIA (A Memória)                                 │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │   │
│  │  │  PostgreSQL  │  │   MongoDB    │  │    Redis     │  │   S3     │ │   │
│  │  │   + PostGIS  │  │  (Documents) │  │   (Cache)    │  │ (Assets) │ │   │
│  │  │              │  │              │  │              │  │          │ │   │
│  │  │ • World state│  │ • Content    │  │ • Sessions   │  │ • glTF   │ │   │
│  │  │ • GIS data   │  │ • Metadata   │  │ • Hot data   │  │ • Textures│ │   │
│  │  │ • Users      │  │ • Logs       │  │ • Rate limit │  │ • Audio  │ │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────┘ │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │Elasticsearch │  │  TimescaleDB │  │   TileServer │              │   │
│  │  │   (Search)   │  │  (Time Series)│  │   (Maps)     │              │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ▲                                        │
│                                    │ Terraform / Ansible                    │
│                                    │                                        │
│  ┌─────────────────────────────────┴───────────────────────────────────┐   │
│  │  CAMADA 1: INFRAESTRUTURA (Substituível)                            │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │   │
│  │  │  Kubernetes  │  │    Docker    │  │  Terraform   │  │  CI/CD   │ │   │
│  │  │   (K8s)      │  │  (Containers)│  │    (IaC)     │  │ (GitHub) │ │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────┘ │   │
│  │                                                                     │   │
│  │  CLOUD: AWS / Azure / GCP / On-Premise (substituível)              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 DETALHAMENTO POR CAMADA

### CAMADA 1: Infraestrutura (Substituível)

**Princípio:** A infraestrutura física/cloud deve ser completamente substituível sem afetar o mundo.

**Componentes:**

| Componente | Tecnologia Atual | Alternativas | Padrão |
|------------|------------------|--------------|--------|
| Orquestração | Kubernetes | Docker Swarm, Nomad | CNCF |
| Containers | Docker | containerd, Podman | OCI |
| IaC | Terraform | Pulumi, CloudFormation | - |
| Config | Ansible | Chef, Puppet, Salt | - |
| CI/CD | GitHub Actions | GitLab CI, Jenkins | - |

**Requisitos de Portabilidade:**
- Manifestos Kubernetes puros (sem CRDs proprietários)
- Helm charts versionados
- Terraform modules documentados
- Scripts de migração entre clouds

---

### CAMADA 2: Persistência (A Memória)

**Princípio:** Os dados do mundo devem sobreviver a trocas de tecnologia de banco de dados.

#### 2.1 PostgreSQL + PostGIS (Dados Relacionais)

```sql
-- Schema versionado (migrações com Flyway/Liquibase)
CREATE SCHEMA world_v1;

-- Tabela de estado do mundo (autoritativa)
CREATE TABLE world_v1.entity_states (
    entity_id UUID PRIMARY KEY,
    entity_type VARCHAR(100) NOT NULL,
    position GEOMETRY(POINTZ, 4326),  -- WGS84 com altitude
    rotation JSONB,  -- Quaternion {x, y, z, w}
    properties JSONB,  -- Propriedades extensíveis
    version INTEGER DEFAULT 1,  -- Para optimistic locking
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    shard_id VARCHAR(50)  -- Para sharding horizontal
);

-- Índices espaciais
CREATE INDEX idx_entity_position ON world_v1.entity_states USING GIST(position);
CREATE INDEX idx_entity_type ON world_v1.entity_states(entity_type);
CREATE INDEX idx_entity_shard ON world_v1.entity_states(shard_id);

-- Tabela de snapshots (para recuperação)
CREATE TABLE world_v1.world_snapshots (
    snapshot_id UUID PRIMARY KEY,
    snapshot_time TIMESTAMPTZ DEFAULT NOW(),
    shard_id VARCHAR(50),
    entity_count INTEGER,
    snapshot_data BYTEA,  -- Comprimido (zstd)
    checksum VARCHAR(64)  -- SHA-256
);

-- Tabela de eventos (event sourcing leve)
CREATE TABLE world_v1.world_events (
    event_id UUID PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,
    entity_id UUID,
    payload JSONB,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    sequence_number BIGINT,  -- Para ordenação total
    shard_id VARCHAR(50)
);

CREATE INDEX idx_events_entity ON world_v1.world_events(entity_id, sequence_number);
CREATE INDEX idx_events_time ON world_v1.world_events(timestamp);
```

#### 2.2 MongoDB (Documentos Flexíveis)

```javascript
// Coleção de conteúdo do museu
{
  "_id": UUID("..."),
  "content_type": "museum_item",
  "schema_version": "1.0.0",
  "title": {
    "pt": "Sede Villa Terezinha",
    "en": "Villa Terezinha Headquarters"
  },
  "description": { ... },
  "media": {
    "thumbnail": "https://cdn.villacanabrava.world/assets/thumb/001.webp",
    "images": [...],
    "models": [
      {
        "format": "glTF",
        "url": "https://cdn.villacanabrava.world/models/sede.glb",
        "variants": {
          "lod0": "..._lod0.glb",
          "lod1": "..._lod1.glb",
          "lod2": "..._lod2.glb"
        }
      }
    ]
  },
  "metadata": {
    "created_date": ISODate("1985-03-15"),
    "location": {
      "type": "Point",
      "coordinates": [-43.947776, -17.385117]
    },
    "tags": ["sede", "arquitetura", "historia"],
    "related_entities": [UUID("..."), UUID("...")]
  },
  "access_control": {
    "visibility": "public",
    "download": "registered"
  },
  "created_at": ISODate("2026-02-06T00:00:00Z"),
  "updated_at": ISODate("2026-02-06T00:00:00Z")
}
```

#### 2.3 Redis (Cache e Estado Transitório)

```
# Estrutura de chaves
world:session:{session_id} -> JSON (TTL: 24h)
world:presence:{shard_id} -> Set de user_ids
world:aoi:{user_id} -> Set de entity_ids visíveis
world:rate_limit:{user_id} -> Contadores
world:hot_entity:{entity_id} -> JSON (cache de entidade quente)
```

#### 2.4 S3/MinIO (Assets Imutáveis)

**Estrutura de Buckets:**

```
villa-canabrava-assets/
├── production/
│   ├── models/
│   │   ├── gltf/           # glTF 2.0 + Draco
│   │   ├── usd/            # OpenUSD (fonte)
│   │   └── chunks/         # Chunked para streaming
│   ├── textures/
│   │   ├── ktx2/           # Khronos Texture 2.0
│   │   └── webp/           # Fallback
│   ├── audio/
│   │   ├── opus/           # Opus codec
│   │   └── mp3/            # Fallback
│   └── metadata/
│       └── json/           # Metadados associados
├── staging/                # Mesma estrutura
└── archive/                # Snapshots históricos
```

---

### CAMADA 3: Simulação Autoritativa (A Verdade)

**Princípio:** O servidor é a única fonte de verdade. Clientes apenas renderizam.

```python
# Estrutura conceitual da Simulation Engine

class WorldSimulation:
    """
    Loop de simulação autoritativo.
    Roda a 20-60 Hz, dependendo do shard.
    """
    
    def __init__(self, shard_id: str):
        self.shard_id = shard_id
        self.tick_rate = 20  # Hz
        self.entities: Dict[UUID, Entity] = {}
        self.spatial_index = SpatialHash(cell_size=100)  # metros
        
    async def tick(self, delta_time: float):
        """
        Um frame de simulação.
        Ordem é CRÍTICA para determinismo.
        """
        # 1. Processar inputs dos clientes
        await self.process_inputs()
        
        # 2. Atualizar física (posições, velocidades)
        await self.update_physics(delta_time)
        
        # 3. Detectar colisões
        await self.detect_collisions()
        
        # 4. Resolver colisões
        await self.resolve_collisions()
        
        # 5. Executar comportamentos de entidades
        await self.update_behaviors(delta_time)
        
        # 6. Atualizar índice espacial
        await self.update_spatial_index()
        
        # 7. Calcular interesse espacial para cada jogador
        await self.calculate_interest_areas()
        
        # 8. Enviar atualizações para clientes
        await self.broadcast_updates()
        
        # 9. Persistir estado (a cada N ticks)
        if self.tick_count % self.snapshot_interval == 0:
            await self.persist_snapshot()
    
    def calculate_interest_area(self, player: Player) -> Set[UUID]:
        """
        Determina quais entidades um jogador deve receber.
        Baseado em distância, relevância e LOD.
        """
        aoi_radius = player.aoi_radius  # Área de interesse
        nearby = self.spatial_index.query_radius(
            player.position, 
            aoi_radius
        )
        
        # Filtrar por relevância
        relevant = {e for e in nearby if self.is_relevant(player, e)}
        
        return relevant
```

---

### CAMADA 4: Serviços de Domínio (O Mundo)

#### 4.1 World Service

```protobuf
// world.proto
syntax = "proto3";
package villa_canabrava.world.v1;

service WorldService {
  // Estado do mundo
  rpc GetEntityState(GetEntityStateRequest) returns (EntityState);
  rpc StreamEntityStates(StreamEntityStatesRequest) returns (stream EntityStateUpdate);
  
  // Mutações (autorizadas)
  rpc MoveEntity(MoveEntityRequest) returns (MoveEntityResponse);
  rpc Interact(InteractRequest) returns (InteractResponse);
  
  // Queries espaciais
  rpc QueryEntitiesInRadius(QueryInRadiusRequest) returns (QueryResult);
  rpc QueryEntitiesInBox(QueryInBoxRequest) returns (QueryResult);
  
  // Snapshots
  rpc GetWorldSnapshot(GetSnapshotRequest) returns (WorldSnapshot);
  rpc RestoreWorldSnapshot(RestoreSnapshotRequest) returns (RestoreSnapshotResponse);
}

message EntityState {
  string entity_id = 1;
  string entity_type = 2;
  Transform transform = 3;
  map<string, bytes> properties = 4;
  int64 version = 5;
  int64 timestamp = 6;
}

message Transform {
  Vector3 position = 1;
  Quaternion rotation = 2;
  Vector3 scale = 3;
}

message Vector3 {
  double x = 1;
  double y = 2;
  double z = 3;
}

message Quaternion {
  double x = 1;
  double y = 2;
  double z = 3;
  double w = 4;
}
```

#### 4.2 GIS Service

```protobuf
// gis.proto
syntax = "proto3";
package villa_canabrava.gis.v1;

service GISService {
  // Features geoespaciais
  rpc GetFeature(GetFeatureRequest) returns (GeoFeature);
  rpc QueryFeatures(QueryFeaturesRequest) returns (stream GeoFeature);
  
  // Streaming de tiles
  rpc Stream3DTiles(Stream3DTilesRequest) returns (stream TileData);
  
  // Análise espacial
  rpc CalculateArea(CalculateAreaRequest) returns (AreaResult);
  rpc CalculateDistance(CalculateDistanceRequest) returns (DistanceResult);
  rpc FindNearest(FindNearestRequest) returns (NearestResult);
}

message GeoFeature {
  string feature_id = 1;
  string category = 2;
  string subcategory = 3;
  bytes geometry_wkb = 4;  // Well-Known Binary
  map<string, string> attributes = 5;
  double area_ha = 6;
}
```

---

### CAMADA 5: API Gateway (Fachada)

**Responsabilidades:**
- Rate limiting (100 req/min anônimo, 1000 req/min autenticado)
- Autenticação (JWT + OIDC)
- Routing para serviços
- Caching (Cache-Control, ETag)
- Métricas e logs

```yaml
# kong.yml (exemplo)
services:
  - name: world-service
    url: http://world-service:8080
    routes:
      - name: world-routes
        paths:
          - /api/v1/world
    plugins:
      - name: rate-limiting
        config:
          minute: 1000
      - name: jwt
        config:
          uri_param_names: []
          cookie_names: []
          key_claim_name: iss
          secret_is_base64: false
          claims_to_verify:
            - exp
```

---

### CAMADA 6: Clientes (Substituíveis)

#### 6.1 Cliente Web (WebGPU + WebXR)

```typescript
// Estrutura do cliente web

interface WorldClient {
  // Conexão
  connect(serverUrl: string): Promise<void>;
  disconnect(): void;
  
  // Render
  renderLoop(): void;
  
  // Input
  sendInput(input: PlayerInput): void;
  
  // Estado recebido
  onStateUpdate(callback: (update: StateUpdate) => void): void;
}

// WebGPU Renderer
class WebGPUWorldRenderer {
  private device: GPUDevice;
  private pipeline: GPURenderPipeline;
  private assetManager: GLTFAssetManager;
  
  async initialize(): Promise<void> {
    const adapter = await navigator.gpu.requestAdapter();
    this.device = await adapter.requestDevice();
    
    // Pipeline de renderização
    this.pipeline = await this.createRenderPipeline();
    
    // Gerenciador de assets glTF
    this.assetManager = new GLTFAssetManager(this.device);
  }
  
  async loadAsset(url: string): Promise<GLTFAsset> {
    // Carrega glTF + Draco + KTX2
    return this.assetManager.load(url);
  }
  
  render(entities: Entity[], camera: Camera): void {
    // Render loop otimizado
    const commandEncoder = this.device.createCommandEncoder();
    
    // ... renderização
    
    this.device.queue.submit([commandEncoder.finish()]);
  }
}

// WebXR Support
class WebXRSession {
  async enterVR(): Promise<void> {
    const session = await navigator.xr.requestSession('immersive-vr', {
      requiredFeatures: ['local-floor'],
      optionalFeatures: ['hand-tracking']
    });
    
    // Configura reference space
    const referenceSpace = await session.requestReferenceSpace('local-floor');
    
    // Loop de render XR
    session.requestAnimationFrame(this.onXRFrame);
  }
}
```

#### 6.2 Cliente VR Nativo (OpenXR)

```cpp
// Pseudocódigo C++ para cliente OpenXR

class OpenXRWorldClient {
public:
    bool Initialize() {
        // Carrega OpenXR runtime
        XrInstanceCreateInfo createInfo{XR_TYPE_INSTANCE_CREATE_INFO};
        strcpy(createInfo.applicationInfo.applicationName, "Villa Canabrava VR");
        createInfo.applicationInfo.apiVersion = XR_CURRENT_API_VERSION;
        
        xrCreateInstance(&createInfo, &instance);
        
        // Inicializa sistema
        XrSystemGetInfo systemInfo{XR_TYPE_SYSTEM_GET_INFO};
        systemInfo.formFactor = XR_FORM_FACTOR_HEAD_MOUNTED_DISPLAY;
        xrGetSystem(instance, &systemInfo, &systemId);
        
        // Cria sessão
        // ...
        
        return true;
    }
    
    void RenderFrame() {
        // Aguarda frame
        XrFrameWaitInfo waitInfo{XR_TYPE_FRAME_WAIT_INFO};
        XrFrameState frameState{XR_TYPE_FRAME_STATE};
        xrWaitFrame(session, &waitInfo, &frameState);
        
        // Renderiza para cada view (olho)
        for (uint32_t i = 0; i < viewCount; i++) {
            RenderView(views[i]);
        }
        
        // Submite frame
        xrEndFrame(session, &endFrameInfo);
    }
};
```

---

## 📡 PROTOCOLOS DE COMUNICAÇÃO

### Transporte: HTTP/3 + QUIC

**Vantagens:**
- Latência reduzida (0-RTT)
- Multiplexação sem head-of-line blocking
- Migração de conexão (mudar de WiFi para 4G sem reconectar)
- Congestion control moderno

### Fallbacks

| Cenário | Protocolo Primário | Fallback |
|---------|-------------------|----------|
| API REST | HTTP/3 | HTTP/2, HTTP/1.1 |
| Streaming | WebTransport | WebSocket |
| Real-time | WebRTC DataChannel | WebSocket |
| Voz | WebRTC | - |

---

## 🔄 FLUXO DE DADOS

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FLUXO DE DADOS ATEMPORAL                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  CLIENTE                              SERVIDOR                              │
│  ┌─────────────┐                      ┌─────────────┐                       │
│  │  1. Input   │─────────────────────▶│  2. Validar │                       │
│  │  (movimento)│                      │     Input   │                       │
│  └─────────────┘                      └──────┬──────┘                       │
│                                              │                              │
│                                              ▼                              │
│                                       ┌─────────────┐                       │
│                                       │  3. Simular │                       │
│                                       │   (tick)    │                       │
│                                       └──────┬──────┘                       │
│                                              │                              │
│                                              ▼                              │
│                                       ┌─────────────┐                       │
│                                       │  4. Calcular│                       │
│                                       │    AOI      │                       │
│                                       │  (quem vê)  │                       │
│                                       └──────┬──────┘                       │
│                                              │                              │
│  ┌─────────────┐                      ┌──────┴──────┐                       │
│  │ 6. Render   │◀─────────────────────│  5. Enviar  │                       │
│  │  (delta)    │                      │   updates   │                       │
│  └─────────────┘                      └─────────────┘                       │
│                                                                             │
│  LEGENDA:                                                                   │
│  ───────▶  Cliente → Servidor (input, intenção)                            │
│  ◀───────  Servidor → Cliente (estado autorizado)                          │
│                                                                             │
│  NOTA: O cliente NUNCA decide posição final. Apenas sugere.                │
│        O servidor é a única fonte de verdade.                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

**FIM DA ARQUITETURA DE REFERÊNCIA**
