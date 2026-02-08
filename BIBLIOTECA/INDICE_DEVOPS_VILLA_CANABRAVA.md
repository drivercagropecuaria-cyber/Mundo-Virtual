# 📚 ÍNDICE DE REFERÊNCIA - Villa Canabrava DevOps
**Gerado:** 6 de Fevereiro de 2026  
**Versão:** 1.0  
**Status:** Completo

---

## 🗂️ ESTRUTURA DE DOCUMENTOS

```
DOCUMENTAÇÃO DEVOPS (4 arquivos)
├─ RUNBOOK_DEVOPS_VILLA_CANABRAVA.md
│  └─ Guia executável: Clone → Build → Deploy
│  └─ 5 fases, 17 minutos total
│  └─ Troubleshooting incluído
│
├─ RELATORIO_AUTOPSIA_DEVOPS_VILLA_CANABRAVA.md
│  └─ Auditoria técnica completa
│  └─ Matriz de maturidade (8.4/10)
│  └─ Riscos e mitigações
│
├─ SUMARIO_EXECUTIVO_DEVOPS_VILLA_CANABRAVA.md
│  └─ Resumo para stakeholders
│  └─ Checklist final
│  └─ Próximos passos
│
└─ INDICE_DEVOPS_VILLA_CANABRAVA.md (este arquivo)
   └─ Referência rápida
   └─ Quick links
```

---

## ⚡ QUICK START (5 PASSOS)

### 1️⃣ Clone
```bash
git clone https://github.com/drivercagropecuaria-cyber/Villa-Canabrava.git
cd Villa-Canabrava
```

### 2️⃣ Env Vars (Supabase)
```bash
cat > frontend/.env.local << 'EOF'
VITE_SUPABASE_URL=https://[seu-projeto].supabase.co
VITE_SUPABASE_ANON_KEY=eyJ0eXAi...
EOF
```

### 3️⃣ Build
```bash
cd frontend && npm ci && npm run build
```

### 4️⃣ Vercel Config
Adicionar em Vercel Dashboard → Environment Variables:
- `VITE_SUPABASE_URL` = [valor]
- `VITE_SUPABASE_ANON_KEY` = [valor]

### 5️⃣ Deploy
```bash
git push origin main  # Vercel faz deploy automático
```

---

## 🔍 MAPA TÉCNICO

### App Real
```
biblioteca-frontend (React 19 + Vite 7)
│
├─ Entry: frontend/src/main.tsx
├─ Component Root: frontend/src/App.tsx
├─ Pages: frontend/src/pages/BibliotecaDigital.tsx
├─ API Client: frontend/src/services/supabaseClient.ts
├─ State: Zustand + React Query
└─ Build Output: frontend/dist/
```

### Env Vars Requeridas
| Variável | Tipo | Arquivo |
|----------|------|---------|
| `VITE_SUPABASE_URL` | String (URL) | supabaseClient.ts:3 |
| `VITE_SUPABASE_ANON_KEY` | String (JWT) | supabaseClient.ts:4 |

### Arquivos Críticos
| Arquivo | Propósito | Status |
|---------|----------|--------|
| `frontend/package.json` | Dependencies | ✅ Completo |
| `frontend/vite.config.ts` | Build config | ✅ Pronto |
| `vercel.json` | Deploy config | ✅ Pronto |
| `.gitignore` | Secret protection | ✅ Seguro |
| `frontend/.env.example` | Template | ✅ Presente |

---

## 📝 TABELA DE REFERENCIAS

### Stack Identificado
```
Frontend:        React 19.2.0
Build Tool:      Vite 7.2.4
Language:        TypeScript 5.9.3
State:           Zustand 5.0.11 + React Query 5.90.20
Backend:         Supabase 2.95.2
HTTP:            Axios 1.13.4
Testing:         Vitest 4.0.18
Hosting:         Vercel Global CDN
```

### Security Headers (vercel.json)
```
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

### Build Commands
```bash
npm ci              # Clean install (CI/CD)
npm run dev         # Dev server
npm run build       # Production build
npm run lint        # Code quality
npm run test        # Unit tests
npm run preview     # Preview build local
```

---

## 🔐 SEGURANÇA EM 30 SEGUNDOS

### ✅ PROTEGIDO
- [ ] `.gitignore` contém `.env.local` ✅
- [ ] Nenhum secret hardcoded ✅
- [ ] Vite prefixo `VITE_` requerido ✅
- [ ] CSP headers configurados ✅
- [ ] HSTS forçado ✅

### ❌ NUNCA FAZER
- Commitar `.env.local` ❌
- Hardcode VITE_SUPABASE_KEY em código ❌
- Revelar key em logs públicos ❌
- Usar http (deve ser https) ❌

### 🔍 VALIDAÇÃO PRÉ-DEPLOY
```bash
# Verificar secrets não estão em git
git status | grep ".env"       # Deve estar vazio ✓

# Verificar env vars ausentes
grep -r "supabase.co" frontend/src/ | grep -v "import.meta"  # Vazio ✓

# Testar build local
npm run build                  # Sem erros ✓
```

---

## 🚀 FASES DE DEPLOY

### Fase 1: Validação (2 min)
- Clone repositório
- Validar estrutura
- Verificar .gitignore

### Fase 2: Configuração Supabase (5 min)
- Obter URL + Anon Key
- Criar `.env.local`
- Testar conexão local

### Fase 3: Build (3 min)
- `npm install`
- `npm run build`
- Verificar `dist/` folder

### Fase 4: Vercel Setup (5 min)
- Adicionar env vars no Dashboard
- Verificar projeto ativo
- Confirmar GitHub integration

### Fase 5: Deploy (2 min)
- `git push origin main`
- Aguardar build (2-3 min)
- Validar em `villa-canabrava.vercel.app`

**Tempo Total: ~17 minutos**

---

## 🆘 TROUBLESHOOTING RÁPIDO

| Erro | Causa | Solução |
|------|-------|---------|
| "Supabase URL required" | Env var não carregada | Criar frontend/.env.local |
| "Connection refused" | Supabase offline | Check Project Settings |
| Build fail | Node modules corrompidos | `rm -rf node_modules && npm ci` |
| CSP blocking | Domínio não listado | Verificar vercel.json |
| 404 on deploy | Build output dir errado | Check vercel.json outputDirectory |

---

## 📞 MATRIZ DE CONTATO

### Documentos por Cenário

| Você precisa... | Leia este documento |
|-----------------|-------------------|
| Executar deploy | RUNBOOK_DEVOPS_VILLA_CANABRAVA.md |
| Entender arquitetura | RELATORIO_AUTOPSIA_DEVOPS_VILLA_CANABRAVA.md |
| Informar stakeholders | SUMARIO_EXECUTIVO_DEVOPS_VILLA_CANABRAVA.md |
| Referência rápida | INDICE_DEVOPS_VILLA_CANABRAVA.md (você está aqui) |

### Escalação

| Problema | Ação |
|----------|------|
| GitHub não conecta | Verificar permissões e URL HTTPS |
| Supabase credenciais | Obter em Project Settings → API |
| Vercel build falha | Checar logs no Vercel Dashboard |
| Secrets vazados | Rodar git log --all --patch -- .env.local |

---

## ✅ PRÉ-DEPLOY CHECKLIST (5 MIN)

```bash
# 1. Estrutura (30s)
[ ] ls -la frontend/package.json
[ ] ls -la vercel.json
[ ] ls -la frontend/.env.local

# 2. Git (30s)
[ ] git status | grep ".env"    # Deve estar vazio
[ ] git log frontend/.env.local  # Não deve existir

# 3. Env (1 min)
[ ] cat frontend/.env.local | grep VITE_SUPABASE_URL
[ ] cat frontend/.env.local | grep VITE_SUPABASE_ANON_KEY

# 4. Build (2 min)
[ ] cd frontend && npm run build
[ ] ls -la dist/index.html
[ ] npm run preview              # Sem console errors

# 5. Vercel (1 min)
[ ] Verificar Environment Variables no Dashboard
[ ] Confirmar projeto "villa-canabrava" ativo
```

---

## 📊 STATUS FINAL

| Critério | Score | Status |
|----------|-------|--------|
| Framework | 9/10 | ✅ Aprovado |
| Segurança | 9/10 | ✅ Aprovado |
| DevOps | 8/10 | ✅ Aprovado |
| Documentação | 9/10 | ✅ Aprovado |
| **MÉDIA** | **8.4/10** | **✅ PRONTO** |

---

## 🎯 PRÓXIMO PASSO

1. ✅ Você recebeu: RUNBOOK + RELATÓRIO + SUMÁRIO + ÍNDICE
2. 🔲 Próximo: Auditor externo revisa documentação (2-4h)
3. 🔲 Depois: Execute RUNBOOK Fase 1-5 (~17 min)
4. 🔲 Final: Validar https://villa-canabrava.vercel.app

---

## 📄 VERSIONING

| Data | Versão | Mudança |
|------|--------|---------|
| 2026-02-06 | 1.0 | Inicial - Autópsia + RUNBOOK completos |
| - | - | - |

---

## 🔗 LINKS RÁPIDOS

### Documentação
- [`RUNBOOK_DEVOPS_VILLA_CANABRAVA.md`](./RUNBOOK_DEVOPS_VILLA_CANABRAVA.md) - Executável
- [`RELATORIO_AUTOPSIA_DEVOPS_VILLA_CANABRAVA.md`](./RELATORIO_AUTOPSIA_DEVOPS_VILLA_CANABRAVA.md) - Auditoria
- [`SUMARIO_EXECUTIVO_DEVOPS_VILLA_CANABRAVA.md`](./SUMARIO_EXECUTIVO_DEVOPS_VILLA_CANABRAVA.md) - Executivos

### Projeto
- [GitHub](https://github.com/drivercagropecuaria-cyber/Villa-Canabrava) - Repositório
- [Vercel](https://villa-canabrava.vercel.app) - Deploy
- [Supabase](https://supabase.com) - Backend

---

**Fim do Índice**  
**Status:** ✅ Documentação Completa  
**Próxima Ação:** Execução do RUNBOOK  

