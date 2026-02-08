# 🗺️ ROADMAP DE IMPLEMENTAÇÃO ATEMPORAL
## Do Zero ao Mundo Durável

**Versão:** 1.0  
**Data:** 06 de Fevereiro de 2026  
**Horizonte:** 2026-2028

---

## 🎯 VISÃO DO ROADMAP

Este roadmap descreve a implementação prática de um mundo virtual atemporal, seguindo os princípios, arquitetura e padrões definidos na documentação de fundação.

**Abordagem:** "Vertical Slice First" - Entregar uma fatia completa do sistema o mais cedo possível, provando a atemporalidade desde o início.

---

## 📅 FASE 0: FUNDAÇÃO (Semanas 1-4)

### Objetivo
Estabelecer a base técnica, ferramentas e processos que garantem atemporalidade desde o primeiro commit.

### Entregáveis

| Semana | Atividade | Entregável | Responsável |
|--------|-----------|------------|-------------|
| **S1** | Setup de repositórios | Monorepo com estrutura atemporal | DevOps |
| **S1** | Definição de padrões | Documento de padrões aprovado | Arquiteto |
| **S2** | CI/CD pipeline | Build, test, deploy automatizado | DevOps |
| **S2** | Infraestrutura base | K8s cluster + monitoring | DevOps |
| **S3** | Banco de dados | PostgreSQL + PostGIS + migrations | Backend |
| **S3** | Sistema de eventos | Event store + snapshot service | Backend |
| **S4** | Pipeline de assets | USD → glTF → CDN funcionando | 3D/Tech Art |
| **S4** | Validação | Primeiro asset atravessando pipeline | QA |

### Estrutura de Repositório

```
villa-canabrava-atemporal/
├── .github/
│   └── workflows/
│       ├── ci.yaml
│       ├── cd.yaml
│       └── snapshot.yaml
│
├── docs/
│   ├── architecture/
│   ├── standards/
│   └── api/
│
├── infrastructure/
│   ├── terraform/
│   ├── kubernetes/
│   └── ansible/
│
├── services/
│   ├── world-service/
│   ├── gis-service/
│   ├── content-service/
│   └── user-service/
│
├── clients/
│   ├── web-client/          # WebGPU + WebXR
│   ├── vr-client/           # OpenXR
│   └── mobile-client/       # React Native
│
├── assets/
│   ├── source/              # OpenUSD
│   ├── intermediate/        # glTF
│   └── runtime/             # glTF + Draco + KTX2
│
├── shared/
│   ├── protobuf/            # Definições gRPC
│   ├── openapi/             # Especificações API
│   └── schemas/             # JSON Schema
│
└── tools/
    ├── asset-pipeline/
    ├── migration-tool/
    └── snapshot-tool/
```

---

## 📅 FASE 1: VERTICAL SLICE (Semanas 5-12)

### Objetivo
Entregar uma fatia vertical completa: um único ambiente (sede) com todas as camadas funcionando, provando a atemporalidade.

### Escopo do Vertical Slice

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    VERTICAL SLICE: SEDE VILLA TEREZINHA                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  CONTEXTO:                                                                  │
│  • 1 ambiente: Sede Villa Terezinha                                         │
│  • ~50 objetos interativos                                                  │
│  • 1 modelo 3D completo (exterior + interior simplificado)                  │
│  • Multiplayer básico (até 10 usuários simultâneos)                         │
│  • Persistência (usuário entra/sai, mundo continua)                         │
│                                                                             │
│  PIPELINE:                                                                  │
│  OpenUSD (fonte) → glTF → CDN → Cliente Web (WebGPU)                        │
│                                                                             │
│  META: Conseguir trocar o cliente (web → VR) sem quebrar o mundo           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Cronograma Detalhado

| Semana | Backend | Frontend | 3D/Assets | Infra |
|--------|---------|----------|-----------|-------|
| **S5** | World Service API | Setup React + WebGPU | Fotogrametria sede | CDN config |
| **S6** | Entity state + persistence | Render básico | Modelagem sede | S3 buckets |
| **S7** | Multiplayer (WebSocket) | Camera + controls | Texturização | Load balancer |
| **S8** | Interest management | Input handling | LOD generation | Monitoring |
| **S9** | Snapshot service | UI/UX básica | Pipeline completo | Alerting |
| **S10** | Auth (OIDC) | Auth integration | Asset optimization | Security |
| **S11** | Testing + bug fixes | Testing + polish | Final assets | Stress test |
| **S12** | **LAUNCH VERTICAL SLICE** | | | |

### Métricas de Sucesso

| Métrica | Target | Mínimo |
|---------|--------|--------|
| Latência (input → render) | < 50ms | < 100ms |
| FPS (WebGPU) | 60 | 30 |
| Tempo de carregamento | < 5s | < 10s |
| Usuários simultâneos | 10 | 5 |
| Uptime | 99.9% | 99.5% |

---

## 📅 FASE 2: EXPANSÃO (Semanas 13-24)

### Objetivo
Expandir o mundo para cobrir todas as áreas principais da fazenda, implementar sharding e escalar a infraestrutura.

### Áreas a Implementar

| Área | Prioridade | Complexidade | Semana |
|------|------------|--------------|--------|
| Sede Villa Terezinha | ✅ Feito | - | - |
| Sede Retiro União | P0 | Média | S13-14 |
| Pivôs (7) | P0 | Média | S15-16 |
| Casas de Colono (8) | P1 | Média | S17-18 |
| Mata Nativa | P1 | Alta | S19-20 |
| Infraestrutura (silos, currais) | P2 | Baixa | S21-22 |
| APPs e Lagoas | P2 | Baixa | S23-24 |

### Sharding

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SHARDING DO MUNDO                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    VILLA CANABRAVA (7.729 ha)                       │   │
│  │                                                                     │   │
│  │   ┌─────────────┬─────────────┬─────────────┐                      │   │
│  │   │   SHARD     │   SHARD     │   SHARD     │                      │   │
│  │   │   NOROESTE  │   NORDESTE  │   NORTE     │                      │   │
│  │   │   (~2k ha)  │   (~2k ha)  │   (~2k ha)  │                      │   │
│  │   │             │             │             │                      │   │
│  │   │ • Mata      │ • Pivôs     │ • Sede      │                      │   │
│  │   │ • APPs      │ • Poços     │ • Retiros   │                      │   │
│  │   └─────────────┴─────────────┴─────────────┘                      │   │
│  │   ┌─────────────┬─────────────┬─────────────┐                      │   │
│  │   │   SHARD     │   SHARD     │   SHARD     │                      │   │
│  │   │   SUDOESTE  │   SUDESTE   │   SUL       │                      │   │
│  │   │   (~2k ha)  │   (~2k ha)  │   (~2k ha)  │                      │   │
│  │   │             │             │             │                      │   │
│  │   │ • Silos     │ • Ferrovia  │ • Currais   │                      │   │
│  │   │ • Fábrica   │ • Estradas  │ • Confinam. │                      │   │
│  │   └─────────────┴─────────────┴─────────────┘                      │   │
│  │                                                                     │   │
│  │   • Handoff suave na fronteira entre shards                        │   │
│  │   • Balanceamento dinâmico de carga                                │   │
│  │   • Replicação cross-region para HA                                │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📅 FASE 3: CONFIABILIDADE (Semanas 25-36)

### Objetivo
Tornar o sistema production-ready com observabilidade, moderação, auditoria e migrações versionadas.

### Componentes

| Componente | Descrição | Semana |
|------------|-----------|--------|
| **Observabilidade** | Logs, métricas, tracing distribuído | S25-26 |
| **Moderação** | Ferramentas de moderação de conteúdo | S27-28 |
| **Auditoria** | Logs de auditoria imutáveis | S29-30 |
| **Migrações** | Sistema de migração de schema versionado | S31-32 |
| **Testes** | Testes de carga, chaos engineering | S33-34 |
| **Documentação** | API docs, guias de desenvolvimento | S35-36 |

### Stack de Observabilidade

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    OBSERVABILIDADE                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  LOGS                    MÉTRICAS              TRACING                       │
│  ┌──────────┐           ┌──────────┐          ┌──────────┐                  │
│  │  App     │──────────▶│Prometheus│◀─────────│  App     │                  │
│  │  Logs    │  Fluentd  │  Server  │  Jaeger  │  Traces  │                  │
│  └────┬─────┘           └────┬─────┘          └────┬─────┘                  │
│       │                      │                     │                        │
│       ▼                      ▼                     ▼                        │
│  ┌──────────┐           ┌──────────┐          ┌──────────┐                  │
│  │   Loki   │           │ Grafana  │          │  Jaeger  │                  │
│  │  (store) │           │(dashboard│          │   UI     │                  │
│  └──────────┘           └──────────┘          └──────────┘                  │
│                                                                             │
│  ALERTAS:                                                                   │
│  • Latência > 100ms (P99)                                                   │
│  • Erro > 1%                                                                │
│  • CPU > 80%                                                                │
│  • Memória > 85%                                                            │
│  • Disco > 80%                                                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📅 FASE 4: ECOSISTEMA (Semanas 37-52)

### Objetivo
Construir ferramentas para que a comunidade possa contribuir e estender o mundo.

### Ferramentas

| Ferramenta | Descrição | Público |
|------------|-----------|---------|
| **World Editor** | Editor web de mundo com permissões | Editores autorizados |
| **Asset Uploader** | Upload de assets com validação | Contribuidores |
| **API Pública** | REST/GraphQL para integrações | Desenvolvedores |
| **SDK** | SDK para criação de clientes alternativos | Comunidade |
| **Marketplace** | Economia de assets (se aplicável) | Criadores |

### World Editor (Web)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    WORLD EDITOR WEB                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TOOLBAR                                                            │   │
│  │  [Select] [Move] [Rotate] [Scale] [Place] [Delete]                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│  ┌──────────────┐  ┌──────────────────────────────────────────────────┐   │
│  │              │  │                                                  │   │
│  │  ASSET      │  │                                                  │   │
│  │  LIBRARY    │  │              VIEWPORT 3D                         │   │
│  │             │  │                                                  │   │
│  │  [🔍]       │  │         (WebGPU render)                          │   │
│  │             │  │                                                  │   │
│  │  📁 Sede    │  │                                                  │   │
│  │  📁 Pivôs   │  │                                                  │   │
│  │  📁 Mata    │  │                                                  │   │
│  │             │  │                                                  │   │
│  │  [Upload]   │  └──────────────────────────────────────────────────┘   │
│  │             │  ┌──────────────────────────────────────────────────┐   │
│  └──────────────┘  │  PROPERTIES                                      │   │
│                    │  Position: [x] [y] [z]                           │   │
│  ┌──────────────┐  │  Rotation: [x] [y] [z] [w]                       │   │
│  │  LAYERS     │  │  Scale:    [x] [y] [z]                           │   │
│  │             │  │                                                  │   │
│  │  ☑️ Base    │  │  [Save] [Revert] [Publish]                       │   │
│  │  ☐ Overlay  │  └──────────────────────────────────────────────────┘   │
│  │             │                                                        │   │
│  └──────────────┘                                                        │   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 CRONOGRAMA VISUAL

```
2026
├───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┤
│ FEV MAR ABR MAI JUN JUL AGO SET OUT NOV DEZ                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ FASE 0: FUNDAÇÃO          [████████]                                        │
│                           Semanas 1-4                                       │
│                                                                             │
│ FASE 1: VERTICAL SLICE            [████████████████]                        │
│                                   Semanas 5-12                              │
│                                   🚀 LAUNCH: Sede                            │
│                                                                             │
│ FASE 2: EXPANSÃO                          [████████████████████████]        │
│                                           Semanas 13-24                     │
│                                           🚀 LAUNCH: Fazenda Completa        │
│                                                                             │
│ FASE 3: CONFIABILIDADE                                          [████████████│
│                                                                 ████████████]│
│                                                                 Semanas 25-36│
│                                                                             │
│ FASE 4: ECOSISTEMA                                                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

2027
├───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┤
│ JAN FEV MAR ABR MAI JUN JUL AGO SET OUT NOV DEZ                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ FASE 4: ECOSISTEMA (cont.)  [████████████████████████████████████████████]│
│                             Semanas 37-52 (2026) + 2027                     │
│                                                                             │
│ FASE 5: MATURIDADE (2027-2028)                                              │
│ • VR/AR completo                                                            │
│ • Metaverso expandido                                                       │
│ • Comunidade ativa                                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 👥 EQUIPE POR FASE

### Fase 0-1 (Semanas 1-12)

| Função | Qtd | Dedicação |
|--------|-----|-----------|
| Tech Lead / Arquiteto | 1 | 100% |
| Backend Engineer | 2 | 100% |
| Frontend Engineer | 2 | 100% |
| 3D / Tech Artist | 1 | 100% |
| DevOps Engineer | 1 | 100% |
| QA Engineer | 1 | 50% |

### Fase 2-4 (Semanas 13-52)

| Função | Qtd | Dedicação |
|--------|-----|-----------|
| Tech Lead / Arquiteto | 1 | 100% |
| Backend Engineer | 3 | 100% |
| Frontend Engineer | 3 | 100% |
| 3D / Tech Artist | 2 | 100% |
| DevOps Engineer | 1 | 100% |
| QA Engineer | 1 | 100% |
| Product Manager | 1 | 100% |
| UX Designer | 1 | 50% |

---

## 💰 ORÇAMENTO POR FASE

| Fase | Duração | Custo Estimado (USD) | Principais Gastos |
|------|---------|---------------------|-------------------|
| Fase 0 | 4 semanas | $50.000 | Setup, ferramentas |
| Fase 1 | 8 semanas | $150.000 | Desenvolvimento, assets |
| Fase 2 | 12 semanas | $250.000 | Assets, infraestrutura |
| Fase 3 | 12 semanas | $200.000 | Observabilidade, testes |
| Fase 4 | 16 semanas | $300.000 | Ferramentas, SDK |
| **Total 2026** | **52 semanas** | **$950.000** | |

---

**FIM DO ROADMAP DE IMPLEMENTAÇÃO**
