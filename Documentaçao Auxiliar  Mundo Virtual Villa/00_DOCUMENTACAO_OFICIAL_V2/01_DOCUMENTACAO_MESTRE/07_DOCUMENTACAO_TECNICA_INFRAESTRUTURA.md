# 🔧 DOCUMENTAÇÃO TÉCNICA DE INFRAESTRUTURA
## Especificações Técnicas do Universo Virtual Villa Canabrava

**Versão:** 1.0  
**Data:** 06 de Fevereiro de 2026  
**Status:** Documento Técnico

---

## 📋 ARQUITETURA DE SISTEMA

### Visão Geral

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ARQUITETURA DO SISTEMA                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        CAMADA DE CLIENTE                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │   Web    │  │  Mobile  │  │  VR/AR   │  │  Desktop │            │   │
│  │  │  Browser │  │   App    │  │  Headset │  │   App    │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼─────────────┼─────────────┼─────────────┼──────────────────┘   │
│          │             │             │             │                        │
│          └─────────────┴──────┬──────┴─────────────┘                        │
│                               │                                             │
│  ┌────────────────────────────┴─────────────────────────────────────────┐  │
│  │                      CAMADA DE APLICAÇÃO                              │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │  │
│  │  │    API       │  │   GraphQL    │  │   WebSocket  │  │   CDN     │ │  │
│  │  │    REST      │  │   Gateway    │  │   Server     │  │   Edge    │ │  │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └─────┬─────┘ │  │
│  └─────────┼─────────────────┼─────────────────┼────────────────┼───────┘  │
│            │                 │                 │                │          │
│  ┌─────────┴─────────────────┴─────────────────┴────────────────┴───────┐ │
│  │                      CAMADA DE SERVIÇOS                               │ │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐  │ │
│  │  │ Museu  │ │  GIS   │ │  Auth  │ │Content │ │  User  │ │ Search │  │ │
│  │  │Service │ │Service │ │Service │ │Service │ │Service │ │Service │  │ │
│  │  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘  │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │                        CAMADA DE DADOS                              │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │ │
│  │  │PostgreSQL│ │ MongoDB  │ │  Redis   │ │Elasticsearch│ │  S3    │  │ │
│  │  │ +PostGIS │ │Documents │ │  Cache   │ │  Search  │ │ Storage│  │ │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │                     CAMADA DE INFRAESTRUTURA                        │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │ │
│  │  │ Kubernetes│ │  Docker  │ │ Terraform│ │  Ansible │ │  CI/CD   │  │ │
│  │  │  Cluster │ │ Containers│ │   IAC    │ │Automation│ │ Pipeline │  │ │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 🖥️ STACK TECNOLÓGICO

### Frontend

| Componente | Tecnologia | Versão | Uso |
|------------|------------|--------|-----|
| Framework | React | 18.x | UI principal |
| Linguagem | TypeScript | 5.x | Tipagem estática |
| Estilização | Tailwind CSS | 3.x | CSS utility-first |
| Componentes | shadcn/ui | latest | Biblioteca de componentes |
| Mapas | MapLibre GL JS | 3.x | Visualização geoespacial |
| 3D Web | Three.js / React Three Fiber | latest | Visualização 3D |
| Estado | Zustand | 4.x | Gerenciamento de estado |
| Query | TanStack Query | 5.x | Fetching de dados |
| Formulários | React Hook Form | 7.x | Validação de forms |

### Backend

| Componente | Tecnologia | Versão | Uso |
|------------|------------|--------|-----|
| Runtime | Node.js | 20.x | Ambiente de execução |
| Framework | NestJS | 10.x | API REST/GraphQL |
| Linguagem | TypeScript | 5.x | Tipagem estática |
| ORM | Prisma | 5.x | Acesso a dados |
| GraphQL | Apollo Server | 4.x | API GraphQL |
| WebSocket | Socket.io | 4.x | Comunicação real-time |
| Autenticação | Passport.js | latest | Autenticação |
| Validação | class-validator | latest | Validação de DTOs |

### Banco de Dados

| Componente | Tecnologia | Versão | Uso |
|------------|------------|--------|-----|
| Principal | PostgreSQL | 16.x | Dados relacionais |
| Extensão GIS | PostGIS | 3.4.x | Dados geoespaciais |
| Documentos | MongoDB | 7.x | Documentos flexíveis |
| Cache | Redis | 7.x | Cache e sessões |
| Busca | Elasticsearch | 8.x | Busca full-text |
| Séries temporais | TimescaleDB | 2.x | Dados temporais |
| Armazenamento | MinIO / S3 | latest | Arquivos e assets |

### Infraestrutura

| Componente | Tecnologia | Uso |
|------------|------------|-----|
| Orquestração | Kubernetes | Container orchestration |
| Containers | Docker | Containerização |
| IAC | Terraform | Infraestrutura como código |
| Automação | Ansible | Configuração de servidores |
| CI/CD | GitHub Actions | Pipeline de deploy |
| Monitoramento | Prometheus + Grafana | Métricas e dashboards |
| Logging | ELK Stack | Centralização de logs |
| CDN | CloudFlare / AWS CloudFront | Distribuição de conteúdo |

### 3D/VR/AR

| Componente | Tecnologia | Uso |
|------------|------------|-----|
| Motor VR | Unreal Engine 5.3 | Experiências VR |
| Alternativa | Unity 2023 | Aplicações multiplataforma |
| Web 3D | Three.js | Visualização web |
| Modelagem | Blender | Criação de assets |
| Fotogrametria | RealityCapture | Modelos a partir de fotos |
| Otimização | Simplygon | LOD e otimização |

---

## 🗄️ ESQUEMA DE BANCO DE DADOS

### PostgreSQL + PostGIS

```sql
-- Schema principal
CREATE SCHEMA IF NOT EXISTS villa_canabrava;

-- Tabela de usuários
CREATE TABLE villa_canabrava.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    avatar_url VARCHAR(500),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de feições geoespaciais
CREATE TABLE villa_canabrava.geo_features (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100),
    layer_name VARCHAR(100),
    geometry GEOMETRY(GEOMETRY, 4326),
    area_ha DECIMAL(12, 4),
    perimeter_km DECIMAL(12, 4),
    centroid GEOMETRY(POINT, 4326),
    bbox GEOMETRY(POLYGON, 4326),
    attributes JSONB DEFAULT '{}',
    media_urls JSONB DEFAULT '[]',
    is_visible BOOLEAN DEFAULT true,
    z_index INTEGER DEFAULT 0,
    style_config JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES villa_canabrava.users(id),
    updated_by UUID REFERENCES villa_canabrava.users(id)
);

-- Índices espaciais
CREATE INDEX idx_geo_features_geometry ON villa_canabrava.geo_features USING GIST(geometry);
CREATE INDEX idx_geo_features_centroid ON villa_canabrava.geo_features USING GIST(centroid);
CREATE INDEX idx_geo_features_category ON villa_canabrava.geo_features(category);
CREATE INDEX idx_geo_features_name ON villa_canabrava.geo_features USING gin(name gin_trgm_ops);
CREATE INDEX idx_geo_features_attributes ON villa_canabrava.geo_features USING gin(attributes);

-- Tabela de camadas
CREATE TABLE villa_canabrava.layers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(255),
    description TEXT,
    category VARCHAR(100),
    style_config JSONB DEFAULT '{}',
    is_visible BOOLEAN DEFAULT true,
    is_basemap BOOLEAN DEFAULT false,
    z_index INTEGER DEFAULT 0,
    min_zoom INTEGER DEFAULT 0,
    max_zoom INTEGER DEFAULT 22,
    attribution TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de itens do museu
CREATE TABLE villa_canabrava.museum_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    description TEXT,
    content_type VARCHAR(50) NOT NULL, -- 'image', 'video', 'audio', 'document', '3d_model'
    collection VARCHAR(100),
    media_urls JSONB NOT NULL DEFAULT '[]',
    thumbnail_url VARCHAR(500),
    metadata JSONB DEFAULT '{}',
    tags TEXT[] DEFAULT '{}',
    related_features UUID[] DEFAULT '{}',
    related_items UUID[] DEFAULT '{}',
    publish_date DATE,
    is_published BOOLEAN DEFAULT false,
    view_count INTEGER DEFAULT 0,
    download_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES villa_canabrava.users(id),
    updated_by UUID REFERENCES villa_canabrava.users(id)
);

-- Índices para museu
CREATE INDEX idx_museum_items_type ON villa_canabrava.museum_items(content_type);
CREATE INDEX idx_museum_items_collection ON villa_canabrava.museum_items(collection);
CREATE INDEX idx_museum_items_published ON villa_canabrava.museum_items(is_published);
CREATE INDEX idx_museum_items_tags ON villa_canabrava.museum_items USING gin(tags);

-- Tabela de tours virtuais
CREATE TABLE villa_canabrava.virtual_tours (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    duration_minutes INTEGER,
    difficulty VARCHAR(20), -- 'easy', 'medium', 'hard'
    target_audience VARCHAR(50),
    thumbnail_url VARCHAR(500),
    waypoints JSONB DEFAULT '[]',
    is_published BOOLEAN DEFAULT false,
    view_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de logs de acesso
CREATE TABLE villa_canabrava.access_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES villa_canabrava.users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100),
    resource_id UUID,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Particionamento por data
CREATE TABLE villa_canabrava.access_logs_2026 PARTITION OF villa_canabrava.access_logs
    FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');
```

---

## 📡 API REST

### Endpoints Principais

#### Autenticação

```
POST   /api/v1/auth/register       # Registrar novo usuário
POST   /api/v1/auth/login          # Login
POST   /api/v1/auth/logout         # Logout
POST   /api/v1/auth/refresh        # Refresh token
GET    /api/v1/auth/me             # Perfil do usuário
PUT    /api/v1/auth/me             # Atualizar perfil
```

#### Feições Geoespaciais

```
GET    /api/v1/features            # Listar feições
GET    /api/v1/features/:id        # Detalhes de uma feição
GET    /api/v1/features/search     # Busca espacial
POST   /api/v1/features            # Criar feição
PUT    /api/v1/features/:id        # Atualizar feição
DELETE /api/v1/features/:id        # Remover feição
GET    /api/v1/features/bbox/:bbox # Feições por bounding box
GET    /api/v1/features/near/:lat/:lon/:radius # Feições próximas
```

#### Museu

```
GET    /api/v1/museum/items        # Listar itens
GET    /api/v1/museum/items/:id    # Detalhes do item
GET    /api/v1/museum/search       # Busca no acervo
GET    /api/v1/museum/collections  # Listar coleções
GET    /api/v1/museum/collections/:id # Itens da coleção
POST   /api/v1/museum/items        # Criar item (admin)
PUT    /api/v1/museum/items/:id    # Atualizar item (admin)
DELETE /api/v1/museum/items/:id    # Remover item (admin)
```

#### Tours Virtuais

```
GET    /api/v1/tours               # Listar tours
GET    /api/v1/tours/:id           # Detalhes do tour
GET    /api/v1/tours/:id/waypoints # Waypoints do tour
POST   /api/v1/tours/:id/start     # Iniciar tour
POST   /api/v1/tours/:id/complete  # Completar tour
```

### Respostas da API

**Sucesso:**
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

**Erro:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Dados inválidos",
    "details": [ ... ]
  }
}
```

---

## 🔒 SEGURANÇA

### Autenticação

**JWT (JSON Web Tokens):**
- Access token: 15 minutos
- Refresh token: 7 dias
- Algoritmo: RS256 (asimétrico)

**OAuth 2.0 / OpenID Connect:**
- Google
- Facebook
- Apple

### Autorização

**RBAC (Role-Based Access Control):**

| Papel | Permissões |
|-------|------------|
| guest | Visualização pública |
| user | + Download baixa resolução |
| researcher | + Download alta resolução, API |
| editor | + Criar/editar conteúdo |
| admin | + Gerenciar usuários, configurações |

### Proteção de Dados

- Criptografia em trânsito (TLS 1.3)
- Criptografia em repouso (AES-256)
- Hash de senhas (bcrypt)
- Rate limiting
- Proteção contra CSRF, XSS, SQL Injection

---

## 📊 MONITORAMENTO

### Métricas Principais

| Métrica | Alerta | Crítico |
|---------|--------|---------|
| CPU | > 70% | > 90% |
| Memória | > 80% | > 95% |
| Disco | > 80% | > 90% |
| Latência API | > 200ms | > 500ms |
| Taxa de erro | > 1% | > 5% |

### Dashboards

- **Infraestrutura:** Grafana com métricas do Prometheus
- **Aplicação:** APM (Application Performance Monitoring)
- **Negócio:** Dashboard de KPIs

---

**FIM DA DOCUMENTAÇÃO TÉCNICA**
