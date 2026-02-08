# 🚀 RUNBOOK DevOps - Villa Canabrava
**Projeto:** Biblioteca Digital RC Agropecuária + Mundo Virtual Villa Canabrava  
**Versão:** 1.0 | **Status:** Pronto para Deploy  
**Data de Geração:** 2026-02-06  
**Executado por:** Agente DevOps/Full-Stack  

---

## 📋 ÍNDICE

1. [Autópsia do Repositório](#autópsia-do-repositório)
2. [Variáveis de Ambiente Requeridas](#variáveis-de-ambiente-requeridas)
3. [Sequência de Deploy](#sequência-de-deploy)
4. [Rastreabilidade de Segredos](#rastreabilidade-de-segredos)
5. [Checklist Pré-Deploy](#checklist-pré-deploy)
6. [Troubleshooting](#troubleshooting)

---

## 🔍 AUTÓPSIA DO REPOSITÓRIO

### App Real Identificado
- **Nome:** `biblioteca-frontend`
- **Localização:** `./frontend/`
- **Tipo:** Single Page Application (SPA)
- **Framework Principal:** React 19.2.0
- **Build Tool:** Vite 7.2.4
- **Linguagem:** TypeScript 5.9.3

### Stack Identificado

| Camada | Tecnologia | Versão | Propósito |
|--------|-----------|--------|----------|
| Frontend Framework | React | 19.2.0 | UI Components |
| Build Bundler | Vite | 7.2.4 | Build & Dev Server |
| Backend Database | Supabase | 2.95.2 | PostgreSQL + Auth |
| Data Fetching | @tanstack/react-query | 5.90.20 | Cache & Sync |
| HTTP Client | Axios | 1.13.4 | API Requests |
| State Management | Zustand | 5.0.11 | Global State |
| Hosting | Vercel | - | Edge Deployment |
| Testing | Vitest | 4.0.18 | Unit/Component Tests |
| Linting | ESLint | 9.39.1 | Code Quality |

### Estrutura de Diretórios

```
villa-canabrava/
├── frontend/                          # App React principal
│   ├── src/
│   │   ├── main.tsx                  # Entry point (React Query provider)
│   │   ├── App.tsx                   # Root component
│   │   ├── services/
│   │   │   └── supabaseClient.ts     # Supabase initialization
│   │   ├── hooks/
│   │   │   └── useApi.ts             # Custom data hooks
│   │   ├── components/
│   │   │   ├── common/               # Navbar, Modal, Spinner
│   │   │   ├── library/              # BibliotecaDigital components
│   │   │   └── map/                  # Geospatial components
│   │   ├── pages/
│   │   │   └── BibliotecaDigital.tsx # Main app page
│   │   └── __tests__/                # Unit tests
│   ├── vite.config.ts                # Vite build config
│   ├── vitest.config.ts              # Test runner config
│   ├── tsconfig.json                 # TypeScript config
│   ├── package.json                  # Dependencies
│   └── index.html                    # HTML entry
│
├── supabase/                         # Backend infrastructure
│   ├── config.toml                   # Local dev config
│   ├── migrations/                   # Database migrations (19+ files)
│   └── functions/                    # Edge functions (Deno)
│
├── vercel.json                       # Vercel deployment config
├── .gitignore                        # Git exclusions (secrets protected)
└── frontend/.env.example             # Environment template

```

### Dependências Críticas

**Production:**
```json
{
  "@supabase/supabase-js": "^2.95.2",
  "@tanstack/react-query": "^5.90.20",
  "axios": "^1.13.4",
  "react": "^19.2.0",
  "react-dom": "^19.2.0",
  "zustand": "^5.0.11"
}
```

**DevDependencies (compilação apenas):**
- TypeScript, Vite, Vitest, ESLint, testing-library

---

## 🔐 VARIÁVEIS DE AMBIENTE REQUERIDAS

### Arquivo: `frontend/.env.local` (nunca commitar!)

```env
# ========== SUPABASE CONFIGURATION ==========
VITE_SUPABASE_URL=https://[PROJECT_ID].supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGc....[base64_jwt_token]

# Validação no código:
# - supabaseClient.ts linha 3-8: Verifica ambos os valores
# - Erro se VITE_SUPABASE_URL ou VITE_SUPABASE_ANON_KEY estiverem vazios
```

### Origem das Credenciais

| Variável | Origem | Localização |
|----------|--------|-----------|
| `VITE_SUPABASE_URL` | Supabase Project Settings | Project → Settings → API → URL |
| `VITE_SUPABASE_ANON_KEY` | Supabase Project Settings | Project → Settings → API → anon key |

### Segurança de Secrets

✅ **Protegido:**
- `.env.local` está em `.gitignore`
- `frontend/.env.local` está em `.gitignore`
- Variáveis só carregadas no build/runtime
- Vite expõe via `import.meta.env` (seguro - requer prefixo `VITE_`)

❌ **NÃO fazer:**
- Commitar `.env.local` ou `.env.production`
- Incluir secrets em `frontend/.env.example`
- Hardcode URLs ou keys no código

---

## 🔄 SEQUÊNCIA DE DEPLOY

### FASE 1: Clone e Validação

```bash
# 1.1 Clone do repositório
git clone https://github.com/drivercagropecuaria-cyber/Villa-Canabrava.git
cd Villa-Canabrava

# 1.2 Validar estrutura (git hook)
ls -la frontend/package.json    # ✓ Deve existir
ls -la supabase/config.toml     # ✓ Deve existir
ls -la vercel.json              # ✓ Deve existir

# 1.3 Verificar que .env.local NÃO está tracked
git status | grep ".env.local"  # ✗ Não deve aparecer
```

### FASE 2: Configuração Supabase

```bash
# 2.1 Obter credenciais do usuário
# O usuário DEVE fornecer:
# - VITE_SUPABASE_URL (de Project Settings → API → URL)
# - VITE_SUPABASE_ANON_KEY (de Project Settings → API → anon key)

# 2.2 Criar arquivo .env.local (LOCAL APENAS - nunca commitar)
cat > frontend/.env.local << 'EOF'
VITE_SUPABASE_URL=[INSERIR_URL_DO_SUPABASE]
VITE_SUPABASE_ANON_KEY=[INSERIR_ANON_KEY_DO_SUPABASE]
EOF

# 2.3 Validar conexão
cd frontend
npm install
npm run dev  # Abre http://localhost:5173
# - Se carregar sem erros no console, ✓ Supabase conectado

# 2.4 Verificar logs
# DevTools (F12) → Console
# Procurar por: "Supabase connection error"
# ✓ Deve estar vazio (sem erros de conexão)
```

### FASE 3: Build Local

```bash
# 3.1 Compilar TypeScript + Vite
cd frontend
npm run build

# Esperado:
# - Arquivo: dist/index.html
# - Arquivo: dist/assets/index-[hash].js
# - Sem erros de compilação TypeScript

# 3.2 Verificar bundle
ls -lh dist/
# index.html         (< 5KB)
# assets/index-*.js  (< 500KB)

# 3.3 Teste local
npm run preview
# Abre http://localhost:4173
# Verificar: Layout carrega, sem console errors
```

### FASE 4: Preparação Vercel

```bash
# 4.1 Verificar configuração vercel.json
cat vercel.json
# Esperado: "framework": "vite", "buildCommand": "cd frontend && npm run build"

# 4.2 Configurar variáveis no Vercel Dashboard
# - Projeto: villa-canabrava
# - Settings → Environment Variables
# - Adicionar:
#   KEY: VITE_SUPABASE_URL
#   VALUE: [SUPABASE_URL]
#   SCOPE: Preview, Production
#
#   KEY: VITE_SUPABASE_ANON_KEY
#   VALUE: [SUPABASE_ANON_KEY]
#   SCOPE: Preview, Production

# 4.3 Verificar git remoto
git remote -v
# Deve conter: github.com/drivercagropecuaria-cyber/Villa-Canabrava.git
```

### FASE 5: Deploy Vercel

```bash
# 5.1 Deploy automático (via GitHub)
# - Push branch para GitHub
git add .
git commit -m "chore: deploy villa-canabrava"
git push origin main

# Vercel automaticamente:
# 1. Detecta push no GitHub
# 2. Clona repo
# 3. Executa: cd frontend && npm ci && npm run build
# 4. Publica dist/ em CDN global

# 5.2 Verificar deployment
# - Dashboard Vercel → villa-canabrava
# - Procurar por: "Deployment complete" ✓
# - Acessar: https://villa-canabrava.vercel.app

# 5.3 Validar produção
curl -I https://villa-canabrava.vercel.app
# HTTP/2 200
# Content-Type: text/html
# Strict-Transport-Security: max-age=31536000

# 5.4 Testar CSP headers
curl -I https://villa-canabrava.vercel.app | grep -i "content-security"
# Deve exibir: "Content-Security-Policy: default-src 'self'..."
```

---

## 📍 RASTREABILIDADE DE SEGREDOS

### Locais onde Secrets são Consumidos

| Arquivo | Linha | Uso | Status |
|---------|-------|-----|--------|
| `frontend/src/services/supabaseClient.ts` | 3-4 | Inicializa cliente Supabase | ✓ Validado |
| `frontend/src/services/supabaseClient.ts` | 6-8 | Erro se credenciais faltarem | ✓ Guard clause |

### Cadeia de Segredos no Pipeline

```
GitHub Secrets (protegido)
  ↓
Vercel Environment Variables (encriptado)
  ↓
Build Time: vercel.json invoca npm run build
  ↓
Vite substitui import.meta.env.VITE_* em tempo de build
  ↓
Resultado: supabaseClient.ts carrega valores
  ↓
Runtime: Conecta a Supabase com URL + KEY
```

### Verificação de Vazamento de Secrets

```bash
# Procurar por valores em código-fonte (deve estar vazio)
grep -r "supabase.co" frontend/src/ --include="*.tsx" --include="*.ts" \
  | grep -v "import.meta.env" | grep -v ".env"
# ✗ Resultado vazio = ✓ Seguro

grep -r "eyJhbGc" frontend/ --include="*.tsx" --include="*.ts"
# ✗ Resultado vazio = ✓ Seguro

# Verificar git history
git log --all --patch --source -- frontend/.env.local
# ✗ Deve retornar "No such file or directory"
```

---

## ✅ CHECKLIST PRÉ-DEPLOY

### Validação Local

- [ ] `npm install` executa sem erros
- [ ] `npm run lint` passa (0 erros)
- [ ] `npm run build` cria `frontend/dist/`
- [ ] `npm run test` passa (se houver testes)
- [ ] `npm run preview` carrega em http://localhost:4173
- [ ] Console (F12) está limpo (sem "Supabase connection error")
- [ ] Arquivo `.env.local` criado com credenciais reais
- [ ] Arquivo `.env.local` NÃO aparece em `git status`

### Validação Pré-Push

- [ ] `.gitignore` contém `frontend/.env.local`
- [ ] `.gitignore` contém `.env.local`
- [ ] Nenhum `console.log()` com secrets em código
- [ ] Vercel Dashboard → Environment Variables preenchidas
- [ ] Supabase Project está ativo e acessível

### Validação Pós-Deploy

- [ ] https://villa-canabrava.vercel.app carrega
- [ ] Página principal renderiza sem erros
- [ ] Console (F12) está limpo
- [ ] Network tab mostra conexão com Supabase API
- [ ] CSP headers estão presentes (F12 → Network → Headers)
- [ ] HSTS header presente (Strict-Transport-Security)

---

## 🔧 TROUBLESHOOTING

### Erro: "Supabase URL and anonymous key are required"

**Causa:** Variáveis de ambiente não carregadas  
**Solução:**

```bash
# 1. Verificar arquivo .env.local existe
test -f frontend/.env.local && echo "✓ Arquivo existe" || echo "✗ Arquivo missing"

# 2. Verificar conteúdo
cat frontend/.env.local
# Deve conter: VITE_SUPABASE_URL=https://...
# Deve conter: VITE_SUPABASE_ANON_KEY=eyJ...

# 3. Se em produção Vercel, verificar Settings
# - Vercel Dashboard → Projeto
# - Settings → Environment Variables
# - Confirmar VITE_SUPABASE_URL e VITE_SUPABASE_ANON_KEY

# 4. Redeployed
git commit --allow-empty -m "chore: rebuild"
git push origin main
```

### Erro: "Connection refused" ao conectar Supabase

**Causa:** URL incorreta ou Supabase project parado  
**Solução:**

```bash
# 1. Validar URL
echo "URL: $VITE_SUPABASE_URL"
# Esperado: https://[PROJECT_ID].supabase.co

# 2. Testar conectividade
curl -I https://[PROJECT_ID].supabase.co/rest/v1/
# Esperado: HTTP/2 401 Unauthorized (significa servidor ok)

# 3. No Supabase Dashboard
# - Projeto → Settings
# - Verificar Status: "Running" ✓
# - Se "Paused": clique em "Resume"

# 4. Verificar ANON_KEY válida
# - Vai para: Project → Settings → API
# - Copiar anon public key
# - Atualizar em vercel.json Environment Variables
```

### Erro: Build fail "Cannot find module '@supabase/supabase-js'"

**Causa:** npm ci não executou  
**Solução:**

```bash
# 1. Limpar cache
cd frontend
rm -rf node_modules package-lock.json

# 2. Reinstalar
npm ci

# 3. Verificar instalação
ls node_modules/@supabase/
# Deve listar: supabase-js

# 4. Tentar build novamente
npm run build
```

### Erro: "CSP header rejection" no console

**Causa:** Domínio Supabase não listado em Content-Security-Policy  
**Solução:**

```bash
# Verificar vercel.json possui supabase.co nos headers
grep "supabase" vercel.json
# Esperado: img-src 'self' data: blob: https://*.supabase.co

# Se faltando, adicionar em vercel.json:
# "connect-src": "'self' https://*.supabase.co"

# Push e Vercel redeploy
git push origin main
```

---

## 📞 CONTATO & ESCALAÇÃO

| Issue | Contato | Ação |
|-------|---------|------|
| GitHub clone falha | `@drivercagropecuaria-cyber` | Verificar repo público |
| Supabase credenciais | `[usuário]` | Obter URL + anon key em Project Settings |
| Vercel deploy falha | Vercel Dashboard → Deployments | Ver logs de build |
| Produção errors | F12 Console + Vercel Analytics | Verificar stack trace |

---

## 📊 RESUMO EXECUTIVO

| Fase | Status | Tempo | Responsável |
|------|--------|-------|-------------|
| 1. Clone | Manual | 2 min | DevOps |
| 2. Supabase Config | Manual | 5 min | DevOps + User |
| 3. Build Local | Automático | 3 min | npm run build |
| 4. Vercel Setup | Manual | 5 min | DevOps |
| 5. Deploy | Automático | 2 min | GitHub → Vercel |
| **TOTAL** | **Pronto** | **17 min** | **Híbrido** |

---

**🎯 Próximo Passo:** Execução da Fase 1 (Clone) conforme sequência acima.
