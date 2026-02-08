# 🎯 PLANO DE VALIDAÇÃO E FECHAMENTO P0
**Mundo Virtual Villa Canabrava - Fase 2, Semana 1**

**Data:** 6 Fevereiro 2026  
**Gerado por:** Agente Executor de Operações (Roo) - Modo Architect  
**Status:** CICLO P0 - 6 Critérios Críticos Identificados

---

## 📊 SUMÁRIO EXECUTIVO - STATUS ATUAL

| # | Critério | Status | Prioridade | Bloqueador |
|---|----------|--------|-----------|-----------|
| 1 | **P0.GIS Geometry** | 🔴 FAIL | P0 | Validade geométrica 98.86% < 99% requerido |
| 2 | **P0.GIS Bounds** | 🔴 CONFLITO | P0 | Dataset bounds divergem do contrato oficial |
| 3 | **P0.GIS Delta** | ✅ PASS | P0 | -49.29% dentro de <50% (governança formalizada) |
| 4 | **P0.Schema RPC** | 🔴 FAIL | P0 | search_catalogo referencia tabela antiga |
| 5 | **P0.Security Webhook** | 🔴 FAIL | P0 | Autenticação JWT não obrigatória |
| 6 | **P0.Security .env** | 🔴 FAIL | P0 | Arquivos .env.local versionados |

**Resultado:** 1 PASS / 5 FAIL/CONFLITO = **P0 NÃO FECHADO** ❌

---

## 🔧 AÇÕES POR CRITÉRIO

### 1️⃣ P0.GIS Geometry - Revalidação Necessária

**Problema:** `geometry_validity_percent: 98.86` vs requerido `≥99`

**Evidência:**
- Arquivo: `BIBLIOTECA/reports/DB_VALIDATION_REPORT.json`
- Campo: `geometry_validity_percent: 98.86`
- Campo: `minimum_required_percent: 99`
- Campo: `meets_criteria: false`
- Recomendação: "aplicar ST_MakeValid() em ~600 geometrias"

**Ação Necessária:**
1. [ ] Executar ST_MakeValid() em todas as geometrias inválidas da tabela PostGIS
2. [ ] Revalidar com ST_IsValid() e confirmar percentual ≥99%
3. [ ] Gerar novo relatório com `meets_criteria: true`
4. [ ] Registrar evidência em EXEC_REPORT

**Comando SQL Esperado:**
```sql
-- Corrigir geometrias inválidas
UPDATE geometrias_villa 
SET geom = ST_MakeValid(geom) 
WHERE NOT ST_IsValid(geom);

-- Validar resultado
SELECT 
  COUNT(CASE WHEN ST_IsValid(geom) THEN 1 END)::float / COUNT(*) * 100 
  AS validity_percent
FROM geometrias_villa;
```

---

### 2️⃣ P0.GIS Bounds - Reconciliação de Dataset

**Problema:** Bounds em DB_VALIDATION_REPORT.json conflitam com contrato oficial

**Conflito Identificado:**
```
DB_VALIDATION_REPORT.json:
  "min_latitude": -19.98, "max_latitude": -19.65
  "min_longitude": -48.65, "max_longitude": -48.05

Contrato Oficial (DOCUMENTO_MAE):
  "latitude": -17.441287 a -17.312838
  "longitude": -44.005069 a -43.884716
```

**Ação Necessária:**
1. [ ] Verificar se DB_VALIDATION_REPORT.json é de outro dataset (legacy/teste)
2. [ ] Se sim, marcar como inválido e gerar novo do dataset OFICIAL
3. [ ] Se é o dataset correto, investigar por que difere do contrato
4. [ ] Confirmar que VILLA_CANABRAVA_DIGITAL_TWIN_GOLDEN.geojson tem bounds corretos
5. [ ] Registrar decisão e evidência em EXEC_REPORT

**Verificação:**
```bash
# Extrair bounds do GeoJSON oficial
jq '[.features[].geometry.coordinates | .[0][] | .[0]] | [min, max]' \
   Villa_Canabrava_Digital_World/data/final_export/VILLA_CANABRAVA_DIGITAL_TWIN_GOLDEN.geojson
```

---

### 3️⃣ P0.GIS Delta - ✅ EVIDÊNCIA COMPLETA (PASS)

**Status:** ✅ ATENDE CRITÉRIO

**Evidência:**
- Arquivo: `Villa_Canabrava_Digital_World/data/processed/topology_report_v1.md`
- Delta observado: -49.29% (11539.38 ha calculado vs 7729.26 ha esperado)
- Critério: `Delta ≤ 50%` conforme `BIBLIOTECA/GOVERNANCE_POLITICA_OPERACOES.md:74-88`
- Justificativa: Sobreposições em KML é normal (ex: Reserva Legal sobre Mata Nativa)

**Ação:** Nenhuma - **PASS CONFIRMADO**

---

### 4️⃣ P0.Schema RPC - Corrigir Referência de Tabela

**Problema:** Migration 1770169200_optimize_search_catalogo.sql linha 16 referencia `catalog_itens` (tabela foi renomeada para `catalogo`)

**Evidência:**
- Arquivo: `BIBLIOTECA/supabase/migrations/1770169200_optimize_search_catalogo.sql:16`
- Código: `FROM catalogo_itens ci` ← **ERRADO**
- Tabela oficial: `catalogo` (conforme migration 1770369100)
- Impacto: Função `search_catalogo()` vai falhar com erro `relation "catalog_itens" does not exist`

**Ação Necessária:**
1. [ ] Atualizar linha 16 de `FROM catalogo_itens ci` para `FROM catalogo ci`
2. [ ] Testar função com query de busca (ex: `search_catalogo('test', 10)`)
3. [ ] Confirmar que retorna resultados sem erro
4. [ ] Registrar correção e teste em EXEC_REPORT

**Correção:**
```sql
-- ANTES (Linha 16):
FROM catalogo_itens ci

-- DEPOIS:
FROM catalogo ci
```

---

### 5️⃣ P0.Security Webhook - Ativar JWT Obrigatório

**Problema:** `cloudconvert-webhook` tem `verify_jwt = false` + token opcional = sem autenticação

**Evidência:**
- Arquivo: `BIBLIOTECA/supabase/config.toml:7-8`
- Config: `verify_jwt = false`
- Lógica: Token obrigatório não é enforçado
- Risco: Endpoint aceita requisições sem autenticação

**Ação Necessária:**
1. [ ] Opção A: Ativar `verify_jwt = true` se webhook deve ser autenticado via JWT
   - Arquivo: `BIBLIOTECA/supabase/config.toml`
   - Alterar: `verify_jwt = false` → `verify_jwt = true`
2. [ ] Opção B: Se webhook deve ser público, implementar validação de token obrigatória em código
   - Arquivo: Localizar função `cloudconvert-webhook` em edge functions
   - Adicionar: Verificação obrigatória de `CLOUDCONVERT_WEBHOOK_TOKEN`
3. [ ] Testar webhook com e sem token (deve falhar sem token)
4. [ ] Registrar decisão e teste em EXEC_REPORT

**Status:** Aguardando decisão de arquitetura (opção A ou B)

---

### 6️⃣ P0.Security .env.local - Remover do Versionamento

**Problema:** Arquivos `.env.local` estão versionados no repositório (risco de secrets)

**Evidência:**
- Arquivo: `.env.local` existe em múltiplos diretórios
- `.gitignore` tem `*.local` mas arquivo pode estar já commitado
- Risco: Secrets de ambiente podem estar expostos no histórico do git

**Ação Necessária:**
1. [ ] Remover `.env.local` de todos os diretórios
2. [ ] Adicionar regra definitiva ao `.gitignore` (se não existir): `*.env.local`
3. [ ] Remover do histórico git (se já commitado):
   ```bash
   git filter-branch --tree-filter 'rm -f .env.local' -- --all
   ```
4. [ ] Confirmar ausência com: `git log --all --full-history -- .env.local`
5. [ ] Criar `.env.local.example` com structure (sem valores)
6. [ ] Registrar remediação em EXEC_REPORT

---

## 📋 KML ANÁLISE - ITEM SECUNDÁRIO

**Identificação de KML Faltante:**
- Esperado: 252 KML no diretório `Documentaçao Auxiliar  Mundo Virtual Villa/00_DOCUMENTACAO_OFICIAL_V2/03_INTELIGENCIA_GEOESPACIAL/KML_RAW`
- Processado: 251 features no GeoJSON final
- Discrepância: 1 arquivo não processado

**Ação (Secundária):**
1. [ ] Executar análise dos KML para identificar qual não foi importado
2. [ ] Confirmar se é erro de import ou arquivo vazio/inválido
3. [ ] Registrar em EXEC_REPORT como achado informativo (não bloqueia P0)

---

## 🎬 PRÓXIMOS PASSOS SEQUENCIAIS

### Fase 1: Validação Técnica (Code Mode)
```
[ ] Executar ST_MakeValid() - P0.GIS Geometry
[ ] Gerar relatório novo de bounds - P0.GIS Bounds
[ ] Testar search_catalogo após correção RPC - P0.Schema RPC
[ ] Definir security policy webhook - P0.Security Webhook
[ ] Remover .env.local + limpar git history - P0.Security .env
[ ] Análise KML (opcional, informativo) - KML Missing
```

### Fase 2: Documentação (Code Mode)
```
[ ] Atualizar EXEC_REPORT com evidências P0
[ ] Criar PASSA/FALHA checklist final
[ ] Registrar decisões de arquitetura tomadas
[ ] Gerar summary de riscos residuais
```

### Fase 3: Preparação Fase 2 Kickoff (Architect Mode)
```
[ ] Confirmar P0 PASS/FAIL definitivo
[ ] Validar que não há bloqueadores antes de Fase 2
[ ] Se itens FAIL persistem, escalar para product owner
```

---

## 📎 EVIDÊNCIAS RASTREÁVEIS (Para Auditoria)

### Documentos Referenciados:
1. **GOVERNANCE:** [`BIBLIOTECA/GOVERNANCE_POLITICA_OPERACOES.md:74-88`](BIBLIOTECA/GOVERNANCE_POLITICA_OPERACOES.md:74)
2. **GIS Delta:** [`Villa_Canabrava_Digital_World/data/processed/topology_report_v1.md`](Villa_Canabrava_Digital_World/data/processed/topology_report_v1.md)
3. **GIS Validation:** [`BIBLIOTECA/reports/DB_VALIDATION_REPORT.json`](BIBLIOTECA/reports/DB_VALIDATION_REPORT.json)
4. **RPC Error:** [`BIBLIOTECA/supabase/migrations/1770169200_optimize_search_catalogo.sql:16`](BIBLIOTECA/supabase/migrations/1770169200_optimize_search_catalogo.sql:16)
5. **Security Config:** [`BIBLIOTECA/supabase/config.toml:7-8`](BIBLIOTECA/supabase/config.toml:7)
6. **Git Ignore:** [`BIBLIOTECA/frontend/.gitignore:13`](BIBLIOTECA/frontend/.gitignore:13)

---

## ✅ ACEITE E PRÓXIMAS AÇÕES

**Este plano está pronto para:**
1. ✅ Revisão do Product Owner (decisões em P0.Security Webhook)
2. ✅ Atribuição ao Code Mode para execução técnica
3. ✅ Auditoria e rastreabilidade (cada ação tem evidência)

**Não proceder para Fase 2 Kickoff sem TODOS os P0 em PASS.**

---

**Plano Preparado:** Roo Agent (Architect Mode)  
**Data:** 6 Fevereiro 2026, 07:03 UTC-3  
**Status:** Aguardando confirmação e execução em Code Mode
