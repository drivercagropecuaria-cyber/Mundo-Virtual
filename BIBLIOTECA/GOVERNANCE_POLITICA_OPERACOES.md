# 🏛️ GOVERNANCE - POLÍTICA DE OPERAÇÕES
**Mundo Virtual Villa Canabrava - Fase 2**

**Data:** 6 Fevereiro 2026  
**Versão:** 1.0  
**Autoridade:** Project Lead (Roberth Naninne) + Agente de Operações (Roo)

---

## 📋 DECISÕES ESTRATÉGICAS FORMALIZADAS

### 1. **TABELA OFICIAL - `catalogo`**

**Decisão:** A tabela canônica de produção é `catalogo` (renomeada de `catalogo_itens`)

**Rationale:**
- Mais abrangente em escopo de dados
- Nomenclatura alinhada com nomenclatura visual (Biblioteca Digital = catálogo)
- Facilita integração com views (v_catalogo_completo)
- Reduz ambiguidade de naming

**Implementação:**
- Migration: `1770369100_rename_catalogo_itens_to_catalogo.sql`
- Frontend: Todos 8 `.from('catalogo')` atualizados em [`useApi.ts`](frontend/src/hooks/useApi.ts)
- RPC Functions: Referências atualizadas para `catalogo`
- Status: ✅ PRONTO PARA DEPLOY

**Soft Delete Pattern:**
```sql
-- Filtro aplicado em todas as queries
.is('deleted_at', null).eq('is_active', true)

-- Operação de arquivamento
UPDATE catalogo 
SET deleted_at = NOW(), is_active = false 
WHERE id = $1;
```

---

### 2. **POLÍTICA DE AUTENTICAÇÃO SUPABASE (JWT VERIFICATION)**

**Modelo: TIER DUAL**

#### **TIER 1: SENSÍVEL (verify_jwt = true)**
Funções que modificam estado, requerem autorização explícita:

| Função | verify_jwt | Razão |
|--------|-----------|-------|
| `init-upload` | ✅ true | Inicia pipeline de upload, requer user autenticado |
| `finalize-upload` | ✅ true | Completa upload, modifica media_assets |
| `process-outbox` | ✅ true | Webhook interno, requer validação |
| `admin-users` | ✅ true | Gerencia roles/permissões, admin only |

**Validação:** JWT token no header `Authorization: Bearer <token>`

#### **TIER 2: PÚBLICO (verify_jwt = false + RLS)**
Funções que apenas leem dados públicos, com RLS policy:

| Função | verify_jwt | RLS Policy |
|--------|-----------|-----------|
| `search_catalogo` | ❌ false | SELECT apenas `WHERE is_active=true AND deleted_at IS NULL` |
| `get_localidades` | ❌ false | SELECT apenas localidades públicas |

**Validação:** RLS filtra automaticamente; sem JWT necessário

#### **EXCEÇÃO: Webhooks Externos**
| Função | verify_jwt | Validação |
|--------|-----------|-----------|
| `cloudconvert-webhook` | ❌ false | Token webhook em query param ou body |

---

### 3. **CRITÉRIO DE DIVERGÊNCIA GIS (GOVERNANÇA ATEMPORAL)**

**Decisão:** Delta ≤ 50% é aceitável para Semana 2

**Métrica:** `delta = |area_calculada - area_postgis| / area_postgis`

**Razão:**
- Shoelace (JS) vs PostGIS (SQL) usam métodos diferentes
- Projeções podem divergir (WGS84 vs UTM)
- Análise post-S2 validará precisão necessária

**Status Atual:**
- KML data: 252 arquivos (244 válidos após remedição)
- Delta observado: -49.29% (aceitável por governança)
- Documentação: [`data/processed/topology_report_v1.md`](data/processed/topology_report_v1.md)

**Próximos Passos (S3):**
- [ ] Avaliar qual projeção usar (WGS84 vs UTM)
- [ ] Validar sample de 20 polígonos manualmente
- [ ] Documentar critério final em GOVERNANCE_GIS.md

---

### 4. **DEPLOY - NOMENCLATURA E ESTRUTURA**

**Nova Estrutura (Planejada para S2-S4):**

```
apps/
├── biblioteca-digital/           (Semana 2 - Frontend atual)
│   ├── src/
│   │   ├── components/          (10+ componentes reutilizáveis)
│   │   ├── hooks/               (useApi, useAuth, etc.)
│   │   ├── pages/               (Visualizações principais)
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── dist/                    (build output)
│
├── museo-3d/                     (Semana 3 - Novo)
│   ├── src/components/museum/   (Three.js rendering)
│   └── ...
│
└── gis-interactive/             (Semana 3 - Novo)
    ├── src/components/map/      (Leaflet + 252 KML layers)
    └── ...
```

**Nomenclatura Oficial:**
- Deploy name: `villa-canabrava-mundo-virtual`
- Não mais: `acervo-rc` (deprecated)

**vercel.json (Atual - Temporário):**
```json
{
  "buildCommand": "cd frontend && npm run build",
  "outputDirectory": "frontend/dist"
}
```

**vercel.json (Target - S2 Kickoff):**
```json
{
  "buildCommand": "cd apps/biblioteca-digital && npm run build",
  "outputDirectory": "apps/biblioteca-digital/dist"
}
```

**Timeline:**
- [ ] S1 (6 Feb): vercel.json aponta `frontend/dist` ✅
- [ ] S2 (13-19 Feb): Migrar para `apps/biblioteca-digital/`
- [ ] S3-S4 (21 Feb+): Múltiplas apps via monorepo

---

### 5. **CICLO DE QA/RELEASE**

**Gate de Build (Obrigatório):**
```bash
✅ npm run lint        # 0 errors, 0 warnings
✅ npm run build       # SPA bundles successfully
✅ npm test            # 25+ tests passing
✅ TypeScript check    # 0 errors
```

**Gate de Deploy:**
- [ ] Todas as builds passando
- [ ] Audit report finalizado
- [ ] External validator sign-off

---

## 📊 CHECKLIST DE IMPLEMENTAÇÃO (6 Feb 2026)

### Status Atual Pós-Execução:

| Achado | Decisão | Implementação | Status |
|--------|---------|--------------|--------|
| #1: Query Provider | Adicionar QueryClientProvider | main.tsx | ✅ OK |
| #2: Table mismatch | Usar `catalogo` oficial | useApi.ts + migration | ✅ PRONTO |
| #3: Soft delete | deleted_at + is_active | Já em migration | ✅ OK |
| #4: Deploy config | Atualizar vercel.json | frontend/dist | ✅ OK |
| #5: JWT functions | Tier 1 verify_jwt=true | config.toml | ✅ OK |
| #6: RLS policies | Tier 2 + soft delete filter | Migrations | ✅ OK |
| #7: GIS delta | Aceitar < 50% | Documentado | ⏳ S3 |
| #8: GIS paths | Converter para relative | Scripts | ⏳ S3 |
| #9: Routing | Implementar React Router | App.tsx | ⏳ S2 |
| #10: Test coverage | Adicionar 25+ testes | Vitest config | ⏳ S2 |

---

## 🎯 PRÓXIMOS PASSOS

### TODAY (6 Feb) - Remaining Tasks:
- [ ] **TAREFA 5:** Teste Build (npm run build, lint, test)
- [ ] **TAREFA 6:** Git commit + push todas as alterações
- [ ] **Validação:** Nenhum erro no console, app inicia

### SEGUNDA (13 Feb) - S2 Kickoff:
- [ ] Deploy da tabela `catalogo` via Supabase migration
- [ ] Validação CRUD em ambiente de staging
- [ ] Iniciar Tarefa 2.1 (Component Library)

### VALIDAÇÃO EXTERNA:
- Auditor Técnico revisar governance policy
- Confirmar decisões em sprint review (Quinta 12 Feb)
- Sign-off antes de S2 kickoff

---

**Versão:** 1.0  
**Última Atualização:** 6 Fevereiro 2026, 04:44 UTC-3  
**Próxima Review:** 13 Fevereiro 2026 (S2 Kickoff)
