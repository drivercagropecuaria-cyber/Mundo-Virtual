# 🏗️ TAREFA 2.2: Biblioteca Digital Interface - Plano Detalhado

**Data:** 6 Fevereiro 2026, 06:10 UTC-3  
**Período Execução:** 14-15 Fevereiro (Semana 2)  
**Duração Estimada:** 8 horas  
**Status:** 🔲 PRONTO PARA EXECUÇÃO (planejamento concluído)

---

## 📊 CONTEXTO ATUAL

### Herança Tarefa 2.1 ✅ COMPLETADA
- 12 componentes React reutilizáveis prontos e validados
- 0 erros TypeScript, Lint, Build
- Build size: 425.96 kB (gzip: 124.85 kB)
- Componentes chave para Tarefa 2.2:
  - `Button`, `Card`, `Modal`, `Input`, `Dropdown`
  - `Pagination`, `Tabs`, `Badge`, `Alert`, `Spinner`
  - `Breadcrumbs`, `Avatar`

### Infraestrutura Base Pronta ✅
- React 19 + TypeScript 5.9 + Vite 7.2.4
- React Query v5 (state management)
- Supabase client configurado (`frontend/src/services/supabaseClient.ts`)
- useApi.ts com 11 hooks CRUD:
  - `useCatalogList()`, `useCatalogSearch()`, `useCatalogItem()`
  - `useCreateCatalogItem()`, `useUpdateCatalogItem()`, `useDeleteCatalogItem()`
  - `useCategories()`, `useTags()`, `useUserCollections()`, etc.

### Página Base Existente
- **BibliotecaDigital.tsx** (262 linhas) - 70% pronta:
  - ✅ 3 view types: grid, list, compact (estados + handlers)
  - ✅ SearchBar, FilterPanel, ItemCard, Pagination integrados
  - ✅ Modal para detalhe de item
  - ✅ QueryClient para invalidações
  - ❌ View type "map" não existe
  - ❌ Estilos CSS podem precisar ajustes responsivos

- **ItemCard.tsx** (151 linhas) - 100% pronta:
  - 3 variantes: grid, list, compact
  - Status colors, thumbnails, keyboard nav
  - onClick handlers
  
- **ItemDetail.tsx** - Precisa validação
- **SearchBar.tsx** - Precisa validação
- **FilterPanel.tsx** - Precisa validação

---

## 🎯 OBJETIVO TAREFA 2.2

Implementar interface completa da Biblioteca Digital com:

### 1️⃣ Três Modos de Visualização
```
Grid    → Cards em layout 3-4 colunas (desktop)
List    → Linhas com thumbnail, título, categoria
Map     → Visualização geoespacial com Leaflet (novo)
```

### 2️⃣ Integração Completa Supabase
- Listar itens paginados (useApi: useCatalogList)
- Buscar por termo (useApi: useCatalogSearch)
- Filtrar por categoria/tags (useApi: useCatalogList + filters)
- Ver detalhe completo (useApi: useCatalogItem)
- Excluir item (useApi: useDeleteCatalogItem)
- Atualizar coleções (useApi: useAddToCollection)

### 3️⃣ Responsividade 100%
- Desktop (1280px+): Grid 4 colunas
- Tablet (768px-1279px): Grid 2-3 colunas
- Mobile (<768px): Grid 1 coluna, list adaptado

### 4️⃣ UX Refinements
- Loading states com Spinner
- Empty state quando sem dados
- Paginação inteligente
- Modal overlay para detalhe
- Keyboard navigation (Enter, Escape)

---

## 🏗️ ARQUITETURA DA SOLUÇÃO

```
Frontend (React 19 + TS)
│
├── pages/
│   └── BibliotecaDigital.tsx ← Container principal
│       ├── SearchBar.tsx (busca + debounce)
│       ├── FilterPanel.tsx (categorias/tags)
│       ├── ViewModeToggle (grid/list/map)
│       │
│       ├── Views/
│       │   ├── GridView.tsx (novo)
│       │   ├── ListView.tsx (novo)
│       │   └── MapView.tsx (NOVO - com Leaflet)
│       │
│       ├── ItemCard.tsx (3 variantes)
│       ├── ItemDetail.tsx (modal)
│       └── Pagination.tsx
│
├── hooks/
│   └── useApi.ts (11 funções CRUD já prontas)
│
├── components/common/
│   └── [12 componentes] (Tarefa 2.1 ✅)
│
└── styles/
    └── BibliotecaDigital.module.css (responsivo)
```

---

## 📋 CHECKLIST DE EXECUÇÃO

### Fase 1: Validação (30 min)
- [ ] Ler BibliotecaDigital.tsx completo (até linha 262)
- [ ] Ler ItemDetail.tsx completo
- [ ] Ler SearchBar.tsx completo
- [ ] Ler FilterPanel.tsx completo
- [ ] Ler BibliotecaDigital.module.css completo
- [ ] Verificar imports dos componentes common (Button, Modal, etc.)

### Fase 2: Implementação View Modes (3 horas)
- [ ] Refatorar BibliotecaDigital.tsx para separar view rendering em sub-componentes
  - [ ] Extrair GridView.tsx do código atual
  - [ ] Extrair ListView.tsx do código atual
  - [ ] Criar MapView.tsx novo com Leaflet
- [ ] Instalar dependencies: `leaflet`, `react-leaflet` (se necessário)
- [ ] Implementar MapView.tsx:
  - [ ] Integração com Leaflet
  - [ ] Posicionamento de itens no mapa (coordenadas)
  - [ ] Popup/tooltip ao clicar
  - [ ] Responsividade map container

### Fase 3: Completar Componentes Auxiliares (2 horas)
- [ ] Validar/completar SearchBar.tsx
  - [ ] Debounce correto (300ms)
  - [ ] Integration com useCatalogSearch
  - [ ] Placeholder + UI
- [ ] Validar/completar FilterPanel.tsx
  - [ ] useCategories() integrado
  - [ ] useTags() integrado
  - [ ] Multi-select de tags
  - [ ] Reset filters
- [ ] Validar/completar ItemDetail.tsx
  - [ ] Display completo de dados
  - [ ] Actions: edit, delete, add to collection
  - [ ] Modal close handler
  - [ ] Integração useDeleteCatalogItem()

### Fase 4: Integração + Estilos (2 horas)
- [ ] Validar/completar BibliotecaDigital.module.css
  - [ ] Media queries: mobile, tablet, desktop
  - [ ] Grid layout responsivo
  - [ ] List view layout
  - [ ] Map container height + responsive
- [ ] Integrar todas as views em BibliotecaDigital.tsx
  - [ ] Conditional rendering por viewType
  - [ ] State management de seleção
  - [ ] Modal open/close
- [ ] Atualizar App.tsx se necessário (routing)
- [ ] Testar navegação entre view modes

### Fase 5: Validação Final (1 hora)
- [ ] `npm run lint` → 0 errors
- [ ] `npm run build` → 0 errors, successful build
- [ ] `npm run type-check` → 0 TypeScript errors
- [ ] Teste visual em 3 breakpoints (mobile 375px, tablet 768px, desktop 1280px)
- [ ] Teste funcional:
  - [ ] Busca funciona
  - [ ] Filtros funcionam
  - [ ] Grid → List → Map switching funciona
  - [ ] Paginação funciona
  - [ ] Click em item abre modal
  - [ ] Delete/add to collection funciona
  - [ ] Keyboard nav (Enter, Escape) funciona

---

## 🔧 DECISÕES DE IMPLEMENTAÇÃO

### Decisão 1: Estrutura de View Modes
**Opção Escolhida:** Separar GridView, ListView, MapView em componentes próprios (mais limpo e testável)
- Mantém BibliotecaDigital.tsx como orchestrator
- Cada view é responsável por seu próprio layout
- Facilita testes isolados em Tarefa 2.4

### Decisão 2: Biblioteca de Map
**Opção Escolhida:** Leaflet + react-leaflet (mais leve que Mapbox)
- Documentação excelente
- Integração React natural
- Performance boa para 252 pontos (GIS Semana 3)
- Licença MIT

### Decisão 3: Dados de Coordenadas
**Nota:** Tarefa 2.2 focará em interface sem GIS
- ItemCard pode ter placeholder para coords
- MapView mostrará itens com dados de location_lat/location_lng se existir
- GIS integration completa é Tarefa 3.2

### Decisão 4: Modal vs Page Detail
**Opção Escolhida:** Modal overlay (conforme design atual)
- Mantém contexto da lista visível
- UX melhor para quick detail view
- Page detail route pode ser adicionado em Tarefa 3.3

---

## 📚 DEPENDÊNCIAS A INSTALAR

```bash
npm install leaflet react-leaflet
npm install --save-dev @types/leaflet
```

**Verificar se já estão instaladas:**
```bash
npm ls leaflet react-leaflet
```

---

## 📝 ARQUIVOS A CRIAR/MODIFICAR

### Novos Arquivos
- `frontend/src/components/library/GridView.tsx` (novo)
- `frontend/src/components/library/ListView.tsx` (novo)
- `frontend/src/components/library/MapView.tsx` (novo)
- `frontend/src/components/library/MapView.module.css` (novo)

### Arquivos a Modificar
- `frontend/src/pages/BibliotecaDigital.tsx` (refatorar + integração views)
- `frontend/src/pages/BibliotecaDigital.module.css` (adicionar responsive)
- `frontend/src/components/library/SearchBar.tsx` (validar + completar)
- `frontend/src/components/library/FilterPanel.tsx` (validar + completar)
- `frontend/src/components/library/ItemDetail.tsx` (validar + completar)
- `frontend/package.json` (adicionar Leaflet deps)

### Documentação
- `frontend/TAREFA_2_2_STATUS.md` (status final com screenshots)

---

## 🎨 ESPECIFICAÇÃO UI

### View Grid
- Cards em layout 3-4 colunas (desktop)
- Thumbnail 200x200px
- Título, categoria, status badge
- Hover effect: shadow + scale
- Click: abre modal

### View List
- Thumbnail 80x80px à esquerda
- Título, categoria, status inline
- Descrição truncada (150 chars)
- Full row clickable
- Separador between rows

### View Map
- Leaflet TileLayer (OpenStreetMap)
- Markers para cada item (com coordenadas)
- Circle radius proporcional a relevância/views
- Popup ao clicar com título + mini-thumbnail
- Zoom/pan controles
- Click marker: abre modal

### Pagination
- Smart navigation (ellipsis se >10 páginas)
- Atual página highlighted
- Click leva à página

### Modal Detail
- Card com imagem full-width
- Título, descrição completa, metadados
- Category badge, status badge, tags
- Buttons: delete (danger), add to collection (primary), close
- Escape key fecha

---

## ⚠️ RISCOS E MITIGAÇÕES

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Leaflet não instala | Bloqueia MapView | Fallback: usar div placeholder até Semana 3 |
| CSS responsivo não funciona | UX ruim mobile | Teste em 3 breakpoints, usar media queries |
| Modal não se integra bem | UX quebrada | Usar Modal.tsx (Tarefa 2.1) como base |
| Map dados não tem coords | MapView vazio | Mostrar apenas lista.length items no mapa |
| Performance com muitos items | Lento scroll | Usar virtualization se >1000 items (Tarefa 3.x) |

---

## ✅ CRITÉRIOS DE SUCESSO

1. **Funcionalidade:** 3 view modes funcionando sem erros
2. **Qualidade:** Lint 0, Build 0, TS 0
3. **Performance:** Build size < 450 kB gzip
4. **UX:** Responsivo em 3 breakpoints, modal funciona, filtros funcionam
5. **Documentação:** TAREFA_2_2_STATUS.md criado com evidências
6. **Git:** Commit + push com mensagem clara

---

## 🚀 PRÓXIMAS ETAPAS (Pós 2.2)

**Tarefa 2.3:** CRUD Supabase Integrado (15-18 Feb)
- Conectar create/update com backend
- Testar mutations com mock data
- Handle errors + toast notifications

**Tarefa 2.4:** Vitest Unit Tests (18-19 Feb)
- 25+ testes unitários
- Coverage gate
- Test SearchBar, FilterPanel, GridView, ListView, MapView

**Tarefa 2.5:** Consolidação (19 Feb)
- README_SEMANA2.md
- FASE_2_SEMANA_2_CONSOLIDACAO.json
- Go/no-go auditoria

---

## 📞 PERGUNTAS PARA VOCÊ RESPONDER (Opcional)

1. **MapView deve mostrar todos os 252 itens do acervo ou apenas itens com coordenadas?**
   - Recomendação: Apenas com coordenadas (completaremos em Tarefa 3.2)

2. **Modal detail precisa de modo "edit" ou apenas "view + delete"?**
   - Recomendação: View + delete por enquanto (edit em Tarefa 2.3)

3. **Há preferência de estilo para view mode buttons (icons vs text)?**
   - Recomendação: Icons (⬜ Grid, ☰ List, 🗺️ Map) conforme código atual

---

**STATUS:** ✅ PLANO APROVADO E PRONTO PARA EXECUÇÃO

Você aprova este plano? Alguma mudança desejada antes de prosseguir para implementação?
