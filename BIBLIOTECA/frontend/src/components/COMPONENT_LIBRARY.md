# 📚 Component Library - Biblioteca Reutilizável

Biblioteca de 12+ componentes React reutilizáveis, totalmente tipados com TypeScript e estilizados com CSS Modules.

## 📋 Índice de Componentes

### Componentes Base (Common)

1. **Button** - Botão com variantes (primary, secondary, danger)
2. **Badge** - Indicador de status (success, warning, danger, info)
3. **Card** - Container com header, body e footer
4. **Input** - Campo de texto com validação
5. **Spinner** - Indicador de carregamento
6. **Modal** - Janela modal com 3 tamanhos
7. **Dropdown** - Seletor com opções e busca
8. **Pagination** - Navegação de páginas
9. **Tabs** - Abas com conteúdo controlado
10. **Breadcrumbs** - Navegação hierárquica
11. **Avatar** - Imagem de perfil ou iniciais
12. **Alert** - Alerta/Toast com auto-close

---

## 🎯 Uso Dos Componentes

### Button

```typescript
import { Button } from '@/components/common';

// Variantes: primary (padrão), secondary, danger
<Button variant="primary" size="large">Clique aqui</Button>
<Button variant="secondary" disabled>Desabilitado</Button>
<Button variant="danger" loading>Deletando...</Button>

// Props
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'small' | 'medium' | 'large';
  loading?: boolean;
  onClick?: (e: React.MouseEvent) => void;
  children: React.ReactNode;
}
```

### Badge

```typescript
import { Badge } from '@/components/common';

// Variantes de cor
<Badge variant="success">Ativo</Badge>
<Badge variant="warning">Pendente</Badge>
<Badge variant="danger">Erro</Badge>
<Badge variant="info">Info</Badge>
```

### Card

```typescript
import { Card } from '@/components/common';

<Card
  header={<h2>Título do Card</h2>}
  footer={<button>Ação</button>}
  elevated
>
  Conteúdo principal aqui
</Card>
```

### Input

```typescript
import { Input } from '@/components/common';

<Input
  label="Email"
  type="email"
  placeholder="seu@email.com"
  required
  validate={(value) => {
    if (!value.includes('@')) return 'Email inválido';
  }}
/>

<Input type="search" placeholder="Pesquisar..." />
<Input type="password" label="Senha" />
```

### Spinner

```typescript
import { Spinner } from '@/components/common';

<Spinner size="medium" message="Carregando..." />
<Spinner size="small" />
<Spinner size="large" color="#ff0000" />
```

### Modal

```typescript
import { Modal } from '@/components/common';

const [isOpen, setIsOpen] = useState(false);

<Modal
  isOpen={isOpen}
  title="Confirmar Ação"
  size="medium" // small, medium, large
  onClose={() => setIsOpen(false)}
  footer={
    <>
      <button onClick={() => setIsOpen(false)}>Cancelar</button>
      <button>Confirmar</button>
    </>
  }
>
  Tem certeza que deseja continuar?
</Modal>
```

### Dropdown

```typescript
import { Dropdown } from '@/components/common';

<Dropdown
  label="Categoria"
  options={[
    { id: '1', label: 'Opção 1' },
    { id: '2', label: 'Opção 2' },
    { id: '3', label: 'Opção 3', disabled: true }
  ]}
  selectedId={selectedId}
  onChange={(id) => setSelectedId(id)}
  searchable
  placeholder="Selecione..."
/>
```

### Pagination

```typescript
import { Pagination } from '@/components/common';

<Pagination
  currentPage={1}
  totalPages={10}
  onPageChange={(page) => setCurrentPage(page)}
  maxPagesToShow={5}
/>
```

### Tabs

```typescript
import { Tabs } from '@/components/common';

<Tabs
  tabs={[
    {
      id: 'tab1',
      label: 'Visão Geral',
      content: <p>Conteúdo da aba 1</p>
    },
    {
      id: 'tab2',
      label: 'Detalhes',
      content: <p>Conteúdo da aba 2</p>
    }
  ]}
  onTabChange={(id) => console.log(id)}
/>
```

### Breadcrumbs

```typescript
import { Breadcrumbs } from '@/components/common';

<Breadcrumbs
  items={[
    { label: 'Home', href: '/' },
    { label: 'Biblioteca', href: '/biblioteca' },
    { label: 'Detalhes' }
  ]}
  separator="/"
/>
```

### Avatar

```typescript
import { Avatar } from '@/components/common';

// Com imagem
<Avatar
  src="https://example.com/avatar.jpg"
  name="João Silva"
  size="large"
  withBorder
/>

// Com iniciais (fallback)
<Avatar name="João Silva" size="medium" backgroundColor="#0066cc" />
```

### Alert

```typescript
import { Alert } from '@/components/common';

<Alert
  variant="success"
  title="Sucesso"
  message="Operação concluída com sucesso"
  closeable
  autoCloseDuration={3000}
  onClose={() => console.log('Fechado')}
/>

// Variantes: success, warning, danger, info
```

---

## 🎨 Recursos

- ✅ **TypeScript**: Tipos completos para cada componente
- ✅ **CSS Modules**: Estilos isolados e sem conflitos
- ✅ **Responsivo**: Adaptável para mobile
- ✅ **Acessibilidade**: ARIA labels e navegação por teclado
- ✅ **Motion Respecting**: Respeita `prefers-reduced-motion`
- ✅ **Dark Mode Ready**: Cores ajustáveis

---

## 📦 Estrutura de Arquivos

```
frontend/src/components/
├── common/
│   ├── Button.tsx
│   ├── Button.module.css
│   ├── Badge.tsx
│   ├── Badge.module.css
│   ├── Card.tsx
│   ├── Card.module.css
│   ├── Input.tsx
│   ├── Input.module.css
│   ├── Spinner.tsx
│   ├── Spinner.module.css
│   ├── Modal.tsx
│   ├── Modal.module.css
│   ├── Dropdown.tsx
│   ├── Dropdown.module.css
│   ├── Pagination.tsx
│   ├── Pagination.module.css
│   ├── Tabs.tsx
│   ├── Tabs.module.css
│   ├── Breadcrumbs.tsx
│   ├── Breadcrumbs.module.css
│   ├── Avatar.tsx
│   ├── Avatar.module.css
│   ├── Alert.tsx
│   ├── Alert.module.css
│   ├── index.ts
│   └── ... (componentes existentes)
├── library/
│   ├── ... (componentes específicos da biblioteca)
├── hooks/
│   └── ... (custom hooks)
└── styles/
    └── ... (estilos globais)
```

---

## 🔄 Integração

### Importação Centralizada

```typescript
// De qualquer arquivo do projeto
import { Button, Modal, Input, Spinner } from '@/components/common';
```

### Pronto para Tarefa 2.2

Todos os componentes estão:
- ✅ Implementados com TypeScript strict
- ✅ Estilizados com CSS Modules
- ✅ Documentados com JSDoc
- ✅ Props bem definidas
- ✅ Validação de lint (0 erros)
- ✅ Build passando (0 erros)

---

## 🚀 Stack Tecnológico

- React 19.2.0
- TypeScript 5.9.3
- Vite 7.2.4
- CSS Modules
- ESLint + TypeScript ESLint

---

Criado em: 6 de Fevereiro de 2026
Pronto para integração em Tarefa 2.2 (14 Feb)
