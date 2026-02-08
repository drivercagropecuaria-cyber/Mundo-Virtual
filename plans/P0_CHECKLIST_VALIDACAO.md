# ✅ CHECKLIST P0 - VALIDAÇÃO E FECHAMENTO
**Mundo Virtual Villa Canabrava - Semana 1, Fase 2**

---

## 📊 RESUMO DE STATUS

**Total de Critérios P0:** 6  
**PASS:** 1 ✅  
**FAIL:** 5 🔴  
**Bloqueador para Fase 2 Kickoff:** ❌ NÃO - Existem 5 bloqueadores críticos

---

## 🎯 CHECKLIST DETALHADO

### ✅ P0.GIS Delta (PASS)

- [x] Delta observado: -49.29% vs esperado <50%
- [x] Documentação: topology_report_v1.md
- [x] Governança: GOVERNANCE_POLITICA_OPERACOES.md:74-88
- [x] Justificativa: Sobreposições em KML é normal
- [x] Status Final: **PASS** ✅

---

### 🔴 P0.GIS Geometry (FAIL)

**Status Atual:**
- [ ] Validade: 98.86% (requerido: ≥99%)
- [ ] Geometrias inválidas: ~600 registros
- [ ] Recomendação: ST_MakeValid()
- [ ] Relatório: DB_VALIDATION_REPORT.json

**Ações para PASS:**
- [ ] Executar ST_MakeValid() em todas as geometrias
- [ ] Validar com ST_IsValid() em amostra
- [ ] Confirmar novo percentual ≥99%
- [ ] Gerar relatório atualizado
- [ ] Evidência em EXEC_REPORT

**Status Final:** 🔴 FAIL (aguardando execução SQL)

---

### 🔴 P0.GIS Bounds (CONFLITO)

**Status Atual:**
- [ ] Bounds em DB_VALIDATION_REPORT.json: lat -19.98 a -19.65, lon -48.65 a -48.05
- [ ] Contrato oficial: lat -17.44 a -17.31, lon -44.005 a -43.88
- [ ] Discrepância: ~200+ km de diferença

**Ações para PASS:**
- [ ] Verificar se DB_VALIDATION_REPORT.json é de outro dataset
- [ ] Validar bounds do GeoJSON oficial
- [ ] Atualizar relatório ou reconciliar dataset
- [ ] Documentar decisão em EXEC_REPORT

**Status Final:** 🔴 CONFLITO (decisão técnica necessária)

---

### 🔴 P0.Schema RPC (FAIL)

**Status Atual:**
- [x] Erro identificado: linha 16 referencia `catalog_itens` (tabela renomeada)
- [x] Tabela oficial: `catalogo` (migration 1770369100)
- [x] Função: search_catalogo()
- [x] Impacto: Erro de runtime "relation doesn't exist"

**Ações para PASS:**
- [ ] Editar migration 1770169200_optimize_search_catalogo.sql
- [ ] Linha 16: `FROM catalogo_itens ci` → `FROM catalogo ci`
- [ ] Testar função com query de busca
- [ ] Confirmar resultado sem erro
- [ ] Evidência em EXEC_REPORT

**Status Final:** 🔴 FAIL (correção SQL simples, não executada)

---

### 🔴 P0.Security Webhook (FAIL)

**Status Atual:**
- [x] Config: `verify_jwt = false` em cloudconvert-webhook
- [x] Token: opcional (sem obrigatoriedade)
- [x] Risco: Endpoint aceita requisições sem autenticação

**Ações para PASS:**
- [ ] Decisão de arquitetura: JWT obrigatório (Opção A) ou token custom (Opção B)?
- [ ] Se Opção A: Alterar config.toml `verify_jwt = false` → `verify_jwt = true`
- [ ] Se Opção B: Implementar validação de token em código da função
- [ ] Testar: requisição sem token deve falhar
- [ ] Evidência em EXEC_REPORT

**Status Final:** 🔴 FAIL (decisão de arquitetura necessária)

---

### 🔴 P0.Security .env.local (FAIL)

**Status Atual:**
- [x] Arquivo `.env.local` existe em repositório
- [x] .gitignore contém `*.local` mas pode estar commitado
- [x] Risco: Secrets no histórico do git

**Ações para PASS:**
- [ ] Remover arquivos `.env.local` de todos os diretórios
- [ ] Verificar se está no histórico git
- [ ] Se sim: executar `git filter-branch` para limpar
- [ ] Confirmar com `git log --all --full-history -- .env.local`
- [ ] Criar `.env.local.example` com estrutura (sem valores)
- [ ] Evidência em EXEC_REPORT

**Status Final:** 🔴 FAIL (remediação git necessária)

---

## 📋 MATRIX DE DEPENDÊNCIAS

```
P0.GIS Geometry → (bloqueado por ST_MakeValid)
P0.GIS Bounds → (bloqueado por reconciliação dataset)
P0.Schema RPC → (bloqueado por SQL update simples)
P0.Security Webhook → (bloqueado por decisão de arquitetura)
P0.Security .env → (bloqueado por cleanup git)
P0.GIS Delta → ✅ JÁ PASS (sem dependências)
```

**Ordem de Execução Recomendada:**
1. P0.Schema RPC (correção simples)
2. P0.Security .env (cleanup git)
3. P0.Security Webhook (decisão + implementação)
4. P0.GIS Geometry (SQL + validação)
5. P0.GIS Bounds (investigação + reconciliação)

---

## 🚀 DECISÕES NECESSÁRIAS DO PRODUCT OWNER

### Decisão 1: P0.GIS Bounds
**Pergunta:** O dataset no DB é o correto ou é legacy?
- [ ] Opção A: DB tem dataset correto, IGNORE DB_VALIDATION_REPORT.json (é de outro projeto)
- [ ] Opção B: DB tem dataset errado, GERAR novo relatório do GeoJSON oficial
- **Impacto:** Define se revalidamos ou descartamos relatório

### Decisão 2: P0.Security Webhook
**Pergunta:** Como autenticar o webhook cloudconvert?
- [ ] Opção A: `verify_jwt = true` (JWT obrigatório)
- [ ] Opção B: Token custom obrigatório em body/query (sem JWT)
- [ ] Opção C: Manter público (não recomendado)
- **Impacto:** Define security posture do webhook

---

## 📝 TEMPLATE PARA EXEC_REPORT P0 VALIDATION

```markdown
## P0 VALIDATION REPORT

### Critérios P0 - Status Final

| # | Critério | Status | Evidência | Ação |
|---|----------|--------|-----------|------|
| 1 | P0.GIS Delta | ✅ PASS | topology_report_v1.md (-49.29%) | Nenhuma |
| 2 | P0.GIS Geometry | 🔴 FAIL | DB_VALIDATION_REPORT.json (98.86%) | ST_MakeValid() |
| 3 | P0.GIS Bounds | 🔴 CONFLITO | Dataset bounds divergem | Reconciliar |
| 4 | P0.Schema RPC | 🔴 FAIL | 1770169200 linha 16 | Corrigir SQL |
| 5 | P0.Security Webhook | 🔴 FAIL | config.toml verify_jwt=false | Decisão + Config |
| 6 | P0.Security .env | 🔴 FAIL | .env.local versionado | Limpar git |

### Resultado: 1 PASS / 5 FAIL = NÃO LIBERADO PARA FASE 2

### Riscos Residuais
- Geometrias inválidas podem causar erros de spatial query
- Webhook sem autenticação expõe a função
- .env.local no git pode expor secrets

### Próximas Ações
1. Execução técnica das correções (Code Mode)
2. Revalidação e geração de novo relatório
3. Confirmação final antes de Fase 2 Kickoff
```

---

## ✅ APROVAÇÃO REQUERIDA

Para proceder para Code Mode:

- [ ] Revisor confirmou compreensão do plano
- [ ] Decisões de PO coletadas (GIS Bounds, Security Webhook)
- [ ] Prioridade de execução acordada
- [ ] Autorização para modificar migrations/config

---

**Plano de Validação:** Completo e Pronto para Execução  
**Data:** 6 Fevereiro 2026  
**Próximo Passo:** Confirmação e switch para Code Mode
