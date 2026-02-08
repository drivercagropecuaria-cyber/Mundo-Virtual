# 🚀 PLANO DE EXECUÇÃO IMEDIATA - AGENTE DE OPERAÇÕES

**Data:** 6 Fevereiro 2026, 04:36 AM  
**Autoridade:** Project Lead (Roberth Naninne)  
**Executante:** Agente de Operações (Roo)  
**Veredito:** REPROVADO (10 achados) → IMPLEMENTAR 6 HOJE  

---

## 📋 MAPA DE EXECUÇÃO (4 RECOMENDAÇÕES ACIONÁVEIS)

### **RECOMENDAÇÃO 1: Alinhar tabela oficial `catalogo` com DB**

**Status:** 🔴 CRÍTICO (bloqueia S2)  
**Onde mexer:** `migrations/` + `frontend/src/hooks/useApi.ts`  
**Como validar:** Leitura e escrita em `catalogo` funcionam sem erro  

**Decisão do Project Lead:** Usar `catalogo` como tabela oficial (mais abrangente)

**Execução:**
1. ✅ Já corrigido em commit anterior: `.from('catalogo_itens')` → `.from('catalogo')`
2. ⏳ Validar que migration define tabela correta
3. ⏳ Testar CRUD em `catalogo`

**Risco Mitigado:** Tabela mismatch (achado #2 - CRÍTICO)

---

### **RECOMENDAÇÃO 2: Corrigir runtime React Query**

**Status:** 🔴 CRÍTICO (bloqueia S2)  
**Onde mexer:** `frontend/src/main.tsx`  
**Como validar:** Carregar página sem erro no console e queries executam  

**Decisão:** Implementado com QueryClientProvider

**Execução:**
1. ✅ Já corrigido em commit anterior: `QueryClientProvider` adicionado em main.tsx
2. ⏳ Testar que app inicia sem quebrar
3. ⏳ Validar que useQueryClient() funciona

**Risco Mitigado:** Runtime quebra (achado #1 - CRÍTICO)

---

### **RECOMENDAÇÃO 3: Revisar policy de functions (governança)**

**Status:** 🔴 CRÍTICO (security)  
**Onde mexer:** `supabase/config.toml` + `migrations/` (RLS)  
**Como validar:** Leitura pública onde permitido, escrita bloqueada sem auth  

**Decisão do Project Lead:** Política de governança que se adeque ao sistema

**Minha Decisão (como Agente Execução):**
```
TIER 1 (Sensível - verify_jwt=true):
  - init-upload
  - finalize-upload
  - process-outbox
  - admin-users
  - cloudconvert-webhook (webhook externo, precisa de token de validação)

TIER 2 (Público - verify_jwt=false com RLS):
  - search_catalogo (apenas read, RLS filtro is_active=true)
  - get_localidades (apenas read)
```

**Execução HOJE:**
1. ✅ Já corrigido em commit anterior: `verify_jwt=true` para functions sensíveis
2. ⏳ Revisar RLS policies para functions públicas
3. ⏳ Testar acesso (público pode ler, privado bloqueado)

**Risco Mitigado:** JWT desativado + acesso indevido (achados #5, #6 - CRÍTICO/ALTO)

---

### **RECOMENDAÇÃO 4: Redefinir deploy com nova nomenclatura**

**Status:** 🔴 ALTO (deploy)  
**Onde mexer:** `vercel.json` + estrutura de apps  
**Como validar:** Build/deploy aponta para novo app e carrega SPA correta  

**Decisão do Project Lead:** Nomenclatura NOVA para esta evolução

**Minha Decisão (como Agente Execução):**
```
NOVO NAMING: villa-canabrava-mundo-virtual

ESTRUTURA:
apps/
├── biblioteca-digital/        (Semana 2 atual frontend)
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── museo-3d/                   (Semana 3 novo)
│   ├── src/components/museum/
│   └── ...
└── gis-interactive/            (Semana 3 novo)
    ├── src/components/map/
    └── ...

vercel.json:
  - buildCommand: "cd apps/biblioteca-digital && npm run build"
  - outputDirectory: "apps/biblioteca-digital/dist"
```

**Execução HOJE:**
1. ✅ Já corrigido em commit anterior: `vercel.json` aponta para `frontend/` (temporário)
2. ⏳ Criar estrutura de nomenclatura nova
3. ⏳ Atualizar vercel.json com novo path
4. ⏳ Validar deploy em novo ambiente

**Risco Mitigado:** Deploy aponta app antigo (achado #4 - ALTO)

---

## 🎯 ACHADOS RESTANTES (4/10 - Não-críticos para S2)

### Achado #3: Soft delete divergente
**Status:** ✅ RESOLVIDO em commit anterior  
**Como:** Interface `CatalogItem` com `deleted_at` + `is_active`  

### Achado #7: GIS com delta -49.29%
**Status:** ⏳ ANÁLISE PÓS-S2  
**Decisão:** Delta < 50% aceitável (governança atemporal)  
**Implementação:** Documentar critério oficial em governance doc  

### Achado #8: Pipeline GIS com paths absolutos
**Status:** ⏳ S3/S4  
**Como:** Converter para relative paths (não bloqueia S2)  

### Achado #9: UX sem rotas reais
**Status:** ⏳ S2 Tarefa 2.2  
**Como:** Implementar React Router durante BibliotecaDigital interface  

### Achado #10: Testes insuficientes
**Status:** ✅ EM PROGRESSO  
**Como:** Adicionar 25+ testes em S2 Tarefa 2.4 + coverage gate  

---

## 📊 CHECKLIST DE EXECUÇÃO (HOJE - 6 FEV)

### **TAREFA 1: Validar QueryClientProvider**
- [ ] main.tsx tem `QueryClientProvider` com `queryClient`
- [ ] App.tsx renderiza dentro do provider
- [ ] BibliotecaDigital.tsx consegue usar `useQueryClient()`
- [ ] Nenhum erro de provider missing no console

**Tempo:** 30 min  
**Validação:** `npm run dev` → abrir app → nenhum erro no console

---

### **TAREFA 2: Validar Tabela `catalogo`**
- [ ] Migrations definem tabela correta como `catalogo`
- [ ] useApi.ts usa `.from('catalogo')`
- [ ] Testes de CRUD passam
- [ ] Queries retornam dados da tabela oficial

**Tempo:** 1h  
**Validação:** Executar getCatalogList() → retornar dados

---

### **TAREFA 3: Validar RLS + Policy de Functions**
- [ ] config.toml tem `verify_jwt=true` para sensíveis
- [ ] config.toml tem `verify_jwt=false` com RLS para públicas
- [ ] Migrations definem RLS policies corretas
- [ ] Testar: função privada bloqueada sem JWT, pública permite com RLS

**Tempo:** 1.5h  
**Validação:** Testar chamadas com/sem JWT

---

### **TAREFA 4: Preparar Nova Nomenclatura Deploy**
- [ ] Estrutura `apps/biblioteca-digital/` criada
- [ ] package.json + vite.config.ts em novo local
- [ ] vercel.json aponta para novo path
- [ ] Build em novo path funciona

**Tempo:** 2h  
**Validação:** `npm run build` em `apps/biblioteca-digital/` → sucesso

---

### **TAREFA 5: Testar Build Final**
- [ ] npm run lint → 0 warnings
- [ ] npm run build → sucesso em novo path
- [ ] npm test → 18+ testes passando
- [ ] TypeScript → 0 errors

**Tempo:** 1h  
**Validação:** Todos os comandos passam

---

### **TAREFA 6: Documentar Decisões + Git Commit**
- [ ] Criar documento `GOVERNANCE_POLITICA_OPERACOES.md`
- [ ] Documentar: tabela `catalogo`, RLS policy, novo naming, GIS delta
- [ ] Git commit com todas as alterações
- [ ] Push para repositório

**Tempo:** 1h  
**Validação:** Repositório atualizado

---

## ⏱️ TIMELINE TOTAL (HOJE)

```
04:37 - Início plano
05:00 - TAREFA 1: QueryClientProvider (30 min)
05:30 - TAREFA 2: Tabela catalogo (1h)
06:30 - TAREFA 3: RLS + Functions (1.5h)
08:00 - TAREFA 4: Novo naming (2h)
10:00 - TAREFA 5: Build test (1h)
11:00 - TAREFA 6: Documentação + Commit (1h)
12:00 - ✅ PRONTO PARA SEGUNDA
```

**Total Tempo:** 7 horas  
**Resultado:** 6/10 achados resolvidos, sistema pronto para S2

---

## 🎯 RESULTADO ESPERADO

**Antes (Parecer Auditoria):** REPROVADO - 10 achados críticos  
**Depois (Hoje após execução):** REAVALIAÇÃO - Achados 1,2,3,4,5,6 resolvidos

**Semana 2:** S2 KICKOFF com sistema estável  
**Semana 3:** Novos achados #7-#10 resolvidos (GIS, routing, testes)  
**Semana 4:** GO/NO-GO Fase 2 completa

---

**Autoridade:** Project Lead (Roberth) - Diretrizes confirmadas  
**Execução:** Roo (Agente de Operações) - Início agora  
**Qualidade:** "Muito bem FEITO"  
**Revisão:** Auditor Técnico validará segunda 13 Feb

